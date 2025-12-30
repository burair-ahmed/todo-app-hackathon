'use client';

import { useState, useEffect } from 'react';
import { Task } from '../../types';
import apiClient from '../../services/api-client';
import TaskForm from '../TaskForm';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  CheckCircle2, 
  Circle, 
  Trash2, 
  Edit3, 
  Clock, 
  MoreHorizontal,
  ChevronRight,
  Loader2,
  Home,
  Briefcase,
  Calendar,
  RotateCcw
} from 'lucide-react';

interface TaskListProps {
  onTaskUpdate?: (task: Task) => void;
  onTaskDelete?: (taskId: string) => void;
  filters?: {
    search?: string;
    priority?: string;
    completed?: boolean;
    tag_id?: string;
    sort_by?: string;
    order?: string;
  };
}

export default function TaskList({ onTaskUpdate, onTaskDelete, filters }: TaskListProps) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  useEffect(() => {
    fetchTasks();
  }, [filters]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const tasksData = await apiClient.getTasks(filters);
      setTasks(tasksData);
    } catch (err) {
      setError('Neural network failure while fetching data');
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleCompletion = async (task: Task) => {
    try {
      const updatedTask = await apiClient.toggleTaskCompletion(task.id);
      setTasks(tasks.map(t => t.id === task.id ? updatedTask : t));
      if (onTaskUpdate) onTaskUpdate(updatedTask);
    } catch (err) {
      console.error('Error toggling task completion:', err);
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    try {
      await apiClient.deleteTask(taskId);
      setTasks(tasks.filter(task => task.id !== taskId));
      if (onTaskDelete) onTaskDelete(taskId);
    } catch (err) {
      console.error('Error deleting task:', err);
    }
  };

  const handleTaskUpdated = (updatedTask: Task) => {
    setTasks(tasks.map(task => task.id === updatedTask.id ? updatedTask : task));
    setEditingTask(null);
    if (onTaskUpdate) onTaskUpdate(updatedTask);
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-24 space-y-4">
        <Loader2 className="w-10 h-10 text-horizon-300 animate-spin" />
        <p className="text-sm font-black text-gray-400 uppercase tracking-widest animate-pulse">Synchronizing Orbit...</p>
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-20 bg-gray-50/50 rounded-[28px] border-2 border-dashed border-gray-200">
        <div className="w-16 h-16 bg-white rounded-3xl flex items-center justify-center shadow-soft-float mb-6">
          <Clock className="w-8 h-8 text-gray-300" />
        </div>
        <h3 className="text-xl font-black text-gray-900 mb-2">Zero Objectives</h3>
        <p className="text-gray-400 font-bold text-sm">No tasks matches your current filters.</p>
      </div>
    );
  }

  const priorityColors = {
    low: 'bg-blue-50 text-blue-500 border-blue-100',
    medium: 'bg-orange-50 text-orange-500 border-orange-100',
    high: 'bg-red-50 text-red-500 border-red-100'
  };

  const groupTasksByDate = (tasks: Task[]) => {
    const groups: { [key: string]: Task[] } = {};
    const noDateTasks: Task[] = [];

    tasks.forEach(task => {
      if (!task.due_date) {
        noDateTasks.push(task);
        return;
      }

      const date = new Date(task.due_date);
      const today = new Date();
      const yesterday = new Date();
      yesterday.setDate(yesterday.getDate() - 1);
      const tomorrow = new Date();
      tomorrow.setDate(tomorrow.getDate() + 1);

      let key = date.toLocaleDateString([], { weekday: 'long', month: 'long', day: 'numeric' });

      if (date.toDateString() === today.toDateString()) key = "Today";
      else if (date.toDateString() === yesterday.toDateString()) key = "Yesterday";
      else if (date.toDateString() === tomorrow.toDateString()) key = "Tomorrow";

      if (!groups[key]) groups[key] = [];
      groups[key].push(task);
    });

    // Sort keys to ensure chronological order (Past -> Future -> No Date)
    // This is tricky with "Today"/"Yesterday" strings. 
    // Better strategy: Store timestamps as keys for sorting, then map to labels?
    // Simplified: Just put "Overdue/Yesterday", "Today", "Tomorrow", "Future", "No Date" order manually if possible.
    // Or just iterate standard keys.
    // For now, let's just rely on object insertion order or keep it simple. 
    // To properly sort, we should convert keys back or use a Map with custom sort logic.
    
    // Let's return an array of { title: string, tasks: Task[] } sorted by date.
    const sortedGroups: { title: string, tasks: Task[], date?: Date }[] = [];
    
    Object.keys(groups).forEach(key => {
       // We use the first task's date to sort
       sortedGroups.push({ title: key, tasks: groups[key], date: new Date(groups[key][0].due_date!) });
    });
    
    sortedGroups.sort((a, b) => (a.date && b.date) ? a.date.getTime() - b.date.getTime() : 0);
    
    if (noDateTasks.length > 0) {
        sortedGroups.push({ title: "No Deadline", tasks: noDateTasks });
    }
    
    return sortedGroups;
  };

  const taskGroups = groupTasksByDate(tasks);

  return (
    <div className="space-y-8">
      {taskGroups.map((group) => (
        <div key={group.title} className="space-y-4">
          <h3 className="text-sm font-black uppercase tracking-widest text-gray-400 pl-2 sticky top-0 bg-gray-50/95 backdrop-blur-sm z-10 py-2 rounded-lg">
            {group.title}
          </h3>
          <div className="space-y-3">
          <AnimatePresence mode="popLayout">
            {group.tasks.map((task) => {
              const isOverdue = task.due_date && new Date(task.due_date) < new Date() && !task.completed;
              const isLate = task.completed && task.due_date && task.completed_at && new Date(task.completed_at) > new Date(task.due_date);
              
              return (
              <motion.div
                key={task.id}
                layout
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95, transition: { duration: 0.2 } }}
                className={`group relative glass-surface p-5 sm:p-6 rounded-[28px] group 
                            ${task.completed ? 'bg-gray-50/50 opacity-60 grayscale' : 'hover:scale-[1.01]'} 
                            transition-all duration-300 ring-1 ring-white/50 border-none shadow-sm hover:shadow-glass hover:bg-white`}
              >
                <div className="flex items-center space-x-5">
                  {/* Custom Checkbox */}
                  <button
                    onClick={() => handleToggleCompletion(task)}
                    className={`flex-shrink-0 w-8 h-8 rounded-2xl flex items-center justify-center transition-all duration-500
                              ${task.completed 
                                ? 'bg-horizon-900 text-white shadow-soft-float scale-110' 
                                : 'bg-white border-2 border-gray-100 text-gray-300 hover:border-horizon-200 hover:text-horizon-200 shadow-sm'}`}
                  >
                    {task.completed ? <CheckCircle2 className="w-5 h-5" /> : <Circle className="w-5 h-5" />}
                  </button>
    
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center space-x-3">
                      <h4 className={`text-lg font-black tracking-tight truncate transition-all duration-500
                                    ${task.completed ? 'text-gray-400 line-through' : 'text-gray-900 group-hover:text-horizon-300'}`}>
                        {task.title}
                      </h4>
                      <div className="flex items-center space-x-2">
                        <span className={`px-2 py-0.5 rounded-full text-[9px] font-black uppercase tracking-wider border transition-all duration-500 ${priorityColors[task.priority]}`}>
                          {task.priority}
                        </span>
                        {task.label && (
                          <span className={`px-2 py-0.5 rounded-full text-[9px] font-black uppercase tracking-wider border flex items-center gap-1
                            ${task.label === 'home' 
                              ? 'bg-purple-50 text-purple-600 border-purple-100' 
                              : 'bg-blue-50 text-blue-600 border-blue-100'}`}>
                            {task.label === 'home' ? <Home className="w-3 h-3" /> : <Briefcase className="w-3 h-3" />}
                            {task.label}
                          </span>
                        )}
                        {task.completed && (
                          <span className="bg-green-50 text-green-600 text-[9px] font-black uppercase tracking-wider px-2 py-0.5 rounded-full border border-green-100">
                            Completed
                          </span>
                        )}
                        {isLate && (
                          <span className="bg-red-50 text-red-600 text-[9px] font-black uppercase tracking-wider px-2 py-0.5 rounded-full border border-red-100">
                            LATE
                          </span>
                        )}
                        {task.recurrence && task.recurrence !== 'none' && (
                          <span className="bg-horizon-50 text-horizon-600 text-[9px] font-black uppercase tracking-wider px-2 py-0.5 rounded-full border border-horizon-100 flex items-center gap-1">
                            <RotateCcw className="w-2.5 h-2.5" />
                            {task.recurrence}
                          </span>
                        )}
                      </div>
                    </div>
                    {(task.due_date || task.description) && (
                      <div className="mt-1 space-y-1">
                        {task.due_date && (
                          <div className={`flex items-center gap-1.5 text-[10px] font-bold ${isOverdue ? 'text-red-500 animate-pulse' : (task.completed ? 'text-gray-300' : 'text-horizon-500')}`}>
                            <Calendar className="w-3 h-3" />
                            <span>Due: {new Date(task.due_date).toLocaleString([], { dateStyle: 'medium', timeStyle: 'short' })}</span>
                            {isOverdue && <span>(Overdue)</span>}
                          </div>
                        )}
                        {task.description && (
                          <p className={`text-sm font-medium truncate max-w-sm
                                      ${task.completed ? 'text-gray-300' : 'text-gray-500'}`}>
                            {task.description}
                          </p>
                        )}
                      </div>
                    )}
                    {task.tags && task.tags.length > 0 && (
                      <div className="flex flex-wrap gap-2 mt-3">
                        {task.tags.map(tag => (
                          <span key={tag.id} className="inline-flex items-center px-2 py-0.5 rounded-lg bg-gray-50 text-gray-400 text-[10px] font-bold border border-gray-100">
                            #{tag.name}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
    
                  {/* Action Toolbar */}
                  <div className="flex items-center space-x-2 opacity-0 group-hover:opacity-100 transition-all duration-300">
                    <button 
                      onClick={() => setEditingTask(task)}
                      className="p-3 text-gray-400 hover:text-horizon-900 hover:bg-horizon-50 rounded-2xl transition-all"
                    >
                      <Edit3 className="w-4 h-4" />
                    </button>
                    <button 
                      onClick={() => handleDeleteTask(task.id)}
                      className="p-3 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-2xl transition-all"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
    
                  <div className="sm:hidden text-gray-400">
                    <MoreHorizontal className="w-5 h-5" />
                  </div>
                </div>
    
                {/* Editing Overlay (Inline) */}
                <AnimatePresence>
                  {editingTask?.id === task.id && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{ opacity: 0, height: 0 }}
                      className="mt-6 pt-6 border-t border-gray-100 overflow-hidden"
                    >
                      <TaskForm 
                        taskToEdit={editingTask} 
                        onTaskUpdated={handleTaskUpdated} 
                        onCancelEdit={() => setEditingTask(null)} 
                      />
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>
            )})}
          </AnimatePresence>
          </div>
        </div>
      ))}
    </div>
  );
}