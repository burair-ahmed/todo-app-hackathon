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
  Loader2
} from 'lucide-react';

interface TaskListProps {
  onTaskUpdate?: (task: Task) => void;
  onTaskDelete?: (taskId: string) => void;
}

export default function TaskList({ onTaskUpdate, onTaskDelete }: TaskListProps) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const tasksData = await apiClient.getTasks();
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
        <p className="text-gray-400 font-bold text-sm">Your workspace is perfectly clear.</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <AnimatePresence mode="popLayout">
        {tasks.map((task) => (
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
                <div className="flex items-center space-x-2">
                  <h4 className={`text-lg font-black tracking-tight truncate transition-all duration-500
                                ${task.completed ? 'text-gray-400 line-through' : 'text-gray-900 group-hover:text-horizon-300'}`}>
                    {task.title}
                  </h4>
                  {task.completed && (
                    <span className="bg-horizon-50 text-horizon-300 text-[10px] font-black uppercase tracking-tighter px-2 py-0.5 rounded-full">
                      Archived
                    </span>
                  )}
                </div>
                {task.description && (
                  <p className={`text-sm font-medium mt-1 truncate max-w-sm
                              ${task.completed ? 'text-gray-300' : 'text-gray-500'}`}>
                    {task.description}
                  </p>
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
        ))}
      </AnimatePresence>
    </div>
  );
}