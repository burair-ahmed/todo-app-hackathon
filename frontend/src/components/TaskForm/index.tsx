'use client';

import { useState, useEffect } from 'react';
import { Task, Priority, Tag } from '../../types';
import apiClient from '../../services/api-client';
import { motion } from 'framer-motion';
import { Save, X, Type, AlignLeft, Sparkles, Loader2, Flag, Hash, Plus, Home, Briefcase, Calendar, RotateCcw } from 'lucide-react';

interface TaskFormProps {
  onTaskCreated?: (task: Task) => void;
  onTaskUpdated?: (task: Task) => void;
  taskToEdit?: Task;
  onCancelEdit?: () => void;
}

export default function TaskForm({ onTaskCreated, onTaskUpdated, taskToEdit, onCancelEdit }: TaskFormProps) {
  const [title, setTitle] = useState(taskToEdit?.title || '');
  const [description, setDescription] = useState(taskToEdit?.description || '');
  const [priority, setPriority] = useState<Priority>(taskToEdit?.priority || 'medium');
  const [label, setLabel] = useState<'home' | 'work' | undefined>(taskToEdit?.label);
  const [selectedTagIds, setSelectedTagIds] = useState<string[]>(taskToEdit?.tags.map(t => t.id) || []);
  const [allTags, setAllTags] = useState<Tag[]>([]);
  const [newTagName, setNewTagName] = useState('');
  const [dueDate, setDueDate] = useState(taskToEdit?.due_date ? new Date(taskToEdit.due_date).toISOString().slice(0, 16) : '');
  const [recurrence, setRecurrence] = useState<string>(taskToEdit?.recurrence || 'none');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchTags();
  }, []);

  const fetchTags = async () => {
    try {
      const tags = await apiClient.getTags();
      setAllTags(tags);
    } catch (err) {
      console.error('Failed to fetch tags', err);
    }
  };

  const handleCreateTag = async () => {
    if (!newTagName.trim()) return;
    try {
      const tag = await apiClient.createTag(newTagName.trim());
      setAllTags([...allTags, tag]);
      setSelectedTagIds([...selectedTagIds, tag.id]);
      setNewTagName('');
    } catch (err) {
      console.error('Failed to create tag', err);
    }
  };

  const toggleTag = (tagId: string) => {
    setSelectedTagIds(prev => 
      prev.includes(tagId) ? prev.filter(id => id !== tagId) : [...prev, tagId]
    );
  };

  const isEditing = !!taskToEdit;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) {
      setError('Title is mandatory');
      return;
    }
    setError(null);
    setLoading(true);

    try {
      if (isEditing && taskToEdit) {
        const updatedTask = await apiClient.updateTask(taskToEdit.id, {
          title: title || undefined,
          description: description || undefined,
          priority,
          label,
          due_date: dueDate || undefined,
          recurrence: recurrence as any,
          tag_ids: selectedTagIds
        });
        if (onTaskUpdated) onTaskUpdated(updatedTask);
      } else {
        const newTask = await apiClient.createTask({ 
          title, 
          description, 
          priority, 
          label,
          due_date: dueDate || undefined,
          recurrence: recurrence as any,
          tag_ids: selectedTagIds 
        });
        if (onTaskCreated) onTaskCreated(newTask);
        setTitle('');
        setDescription('');
        setPriority('medium');
        setLabel(undefined);
        setDueDate('');
        setRecurrence('none');
        setSelectedTagIds([]);
      }
    } catch (err) {
      setError('Neural encryption failed during sync');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-8 animate-in fade-in duration-700">
      {error && (
        <div className="bg-red-50 border border-red-100 text-red-600 px-6 py-4 rounded-2xl font-bold text-sm tracking-tight">
          {error}
        </div>
      )}

      <div className="space-y-6">
        {/* Title Input */}
        <div className="space-y-3">
          <label className="flex items-center space-x-2 text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2">
            <Type className="w-3 h-3" />
            <span>Task Title</span>
          </label>
          <div className="relative">
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="input-horizon"
              placeholder="E.g. Design System Upgrade 2.0"
            />
          </div>
        </div>

        <div className="grid grid-cols-1 gap-6">
            {/* Priority Selection */}
            <div className="space-y-3">
              <label className="flex items-center space-x-2 text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2">
                <Flag className="w-3 h-3" />
                <span>Priority</span>
              </label>
              <div className="grid grid-cols-3 gap-2">
                {(['low', 'medium', 'high'] as Priority[]).map((p) => (
                  <button
                    key={p}
                    type="button"
                    onClick={() => setPriority(p)}
                    className={`p-3 rounded-2xl border-2 transition-all font-black text-[10px] uppercase tracking-wider ${
                      priority === p 
                        ? 'border-horizon-400 bg-horizon-50 text-horizon-600' 
                        : 'border-transparent bg-gray-50 text-gray-400 hover:bg-gray-100'
                    }`}
                  >
                    {p}
                  </button>
                ))}
              </div>
            </div>

            {/* Label Selection */}
            <div className="space-y-3">
              <label className="flex items-center space-x-2 text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2">
                <Briefcase className="w-3 h-3" />
                <span>Context</span>
              </label>
              <div className="grid grid-cols-2 gap-2">
                  <button
                    type="button"
                    onClick={() => setLabel(label === 'work' ? undefined : 'work')}
                    className={`p-3 rounded-2xl border-2 transition-all font-bold text-xs flex items-center justify-center space-x-2 ${
                      label === 'work'
                        ? 'border-blue-400 bg-blue-50 text-blue-600' 
                        : 'border-transparent bg-gray-50 text-gray-400 hover:bg-gray-100'
                    }`}
                  >
                    <Briefcase className="w-4 h-4" />
                    <span>WORK</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => setLabel(label === 'home' ? undefined : 'home')}
                    className={`p-3 rounded-2xl border-2 transition-all font-bold text-xs flex items-center justify-center space-x-2 ${
                      label === 'home'
                        ? 'border-purple-400 bg-purple-50 text-purple-600' 
                        : 'border-transparent bg-gray-50 text-gray-400 hover:bg-gray-100'
                    }`}
                  >
                    <Home className="w-4 h-4" />
                    <span>HOME</span>
                  </button>
              </div>
            </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Due Date Input */}
            <div className="space-y-3">
              <label className="flex items-center space-x-2 text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2">
                <Calendar className="w-3 h-3 text-horizon-300" />
                <span>Deadline Horizon</span>
              </label>
              <div className="relative group">
                <input
                  type="datetime-local"
                  value={dueDate}
                  onChange={(e) => setDueDate(e.target.value)}
                  className="input-horizon w-full pr-12 appearance-none cursor-pointer text-gray-700 font-bold"
                  style={{ colorScheme: 'light' }}
                  onClick={(e) => (e.target as HTMLInputElement).showPicker()}
                />
                <div 
                  className="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-horizon-200 group-hover:text-horizon-400 transition-colors"
                >
                   <Calendar className="w-5 h-5" />
                </div>
                <style jsx>{`
                  input[type="datetime-local"]::-webkit-calendar-picker-indicator {
                    display: none;
                    -webkit-appearance: none;
                  }
                `}</style>
              </div>
            </div>

            {/* Recurrence Selection */}
            <div className="space-y-3">
              <label className="flex items-center space-x-2 text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2">
                <RotateCcw className="w-3 h-3 text-horizon-300" />
                <span>Repeat Frequency</span>
              </label>
              <div className="relative group">
                <select
                  value={recurrence}
                  onChange={(e) => setRecurrence(e.target.value)}
                  className="input-horizon w-full appearance-none cursor-pointer pr-12 text-sm font-bold text-gray-700"
                >
                  <option value="none">Discrete Task (No Repeat)</option>
                  <option value="daily">Daily Loop</option>
                  <option value="weekly">Weekly Cycle</option>
                  <option value="monthly">Monthly Phase</option>
                </select>
                <div className="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-horizon-200 group-hover:text-horizon-400 transition-colors">
                  <RotateCcw className="w-5 h-5" />
                </div>
              </div>
            </div>
        </div>

        {/* Description Input */}
        <div className="space-y-3">
          <label className="flex items-center space-x-2 text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2">
            <AlignLeft className="w-3 h-3" />
            <span>Description</span>
          </label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={5}
            className="input-horizon resize-none min-h-[120px]"
            placeholder="Provide architectural details..."
          />
        </div>

        {/* Tags Selection */}
        <div className="space-y-3">
          <label className="flex items-center space-x-2 text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2">
            <Hash className="w-3 h-3" />
            <span>Tags</span>
          </label>
          <div className="flex flex-wrap gap-2 mb-4">
            {allTags.map(tag => (
              <button
                key={tag.id}
                type="button"
                onClick={() => toggleTag(tag.id)}
                className={`px-3 py-1.5 rounded-xl text-[10px] font-bold transition-all ${
                  selectedTagIds.includes(tag.id)
                    ? 'bg-horizon-500 text-white'
                    : 'bg-gray-50 text-gray-400 hover:bg-gray-100'
                }`}
              >
                {tag.name}
              </button>
            ))}
          </div>
          <div className="flex space-x-2">
            <input
              type="text"
              value={newTagName}
              onChange={(e) => setNewTagName(e.target.value)}
              className="input-horizon flex-1"
              placeholder="Add new tag..."
              onKeyDown={(e) => e.key === 'Enter' && (e.preventDefault(), handleCreateTag())}
            />
            <button
              type="button"
              onClick={handleCreateTag}
              className="p-5 bg-horizon-50 text-horizon-500 rounded-3xl hover:bg-horizon-100 transition-all"
            >
              <Plus className="w-6 h-6" />
            </button>
          </div>
        </div>
      </div>

      <div className="flex items-center space-x-4">
        <button
          type="submit"
          disabled={loading}
          className="btn-horizon flex-1 flex items-center justify-center space-x-3 group"
        >
          {loading ? (
            <Loader2 className="w-6 h-6 animate-spin" />
          ) : (
            <>
              {isEditing ? <Save className="w-5 h-5" /> : <Sparkles className="w-5 h-5" />}
              <span>{isEditing ? 'Update Task' : 'Add Task'}</span>
            </>
          )}
        </button>

        {onCancelEdit && (
          <button
            type="button"
            onClick={onCancelEdit}
            className="p-5 bg-gray-50 text-gray-400 rounded-3xl hover:bg-red-50 hover:text-red-500 transition-all"
          >
            <X className="w-6 h-6" />
          </button>
        )}
      </div>
    </form>
  );
}