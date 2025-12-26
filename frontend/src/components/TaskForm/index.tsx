'use client';

import { useState } from 'react';
import { Task } from '../../types';
import apiClient from '../../services/api-client';
import { motion } from 'framer-motion';
import { Save, X, Type, AlignLeft, Sparkles, Loader2 } from 'lucide-react';

interface TaskFormProps {
  onTaskCreated?: (task: Task) => void;
  onTaskUpdated?: (task: Task) => void;
  taskToEdit?: Task;
  onCancelEdit?: () => void;
}

export default function TaskForm({ onTaskCreated, onTaskUpdated, taskToEdit, onCancelEdit }: TaskFormProps) {
  const [title, setTitle] = useState(taskToEdit?.title || '');
  const [description, setDescription] = useState(taskToEdit?.description || '');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

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
        });
        if (onTaskUpdated) onTaskUpdated(updatedTask);
      } else {
        const newTask = await apiClient.createTask({ title, description });
        if (onTaskCreated) onTaskCreated(newTask);
        setTitle('');
        setDescription('');
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
            <span>Objective Title</span>
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

        {/* Description Input */}
        <div className="space-y-3">
          <label className="flex items-center space-x-2 text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2">
            <AlignLeft className="w-3 h-3" />
            <span>Contextual Intel</span>
          </label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={5}
            className="input-horizon resize-none min-h-[160px]"
            placeholder="Provide architectural details or relevant context for this objective..."
          />
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
              {isEditing ? <Save className="w-5 h-5" /> : <Sparkles className="w-5 h-5 drop-shadow-[0_0_8px_rgba(255,255,255,0.5)]" />}
              <span>{isEditing ? 'Sync Objective' : 'Initialize Objective'}</span>
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