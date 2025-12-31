'use client';

import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Bell, Check, X, Info, AlertCircle, RefreshCw, Calendar, Clock } from 'lucide-react';
import apiClient from '../../services/api-client';

interface Notification {
  id: string;
  type: 'task_due' | 'task_overdue' | 'recurring_spawned' | 'task_due_soon' | 'general';
  message: string;
  is_read: boolean;
  created_at: string;
}

export default function NotificationCenter() {
  const [isOpen, setIsOpen] = useState(false);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [loading, setLoading] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  const fetchNotifications = async () => {
    try {
      setLoading(true);
      const data = await apiClient.getNotifications(0, 50); // Fetch top 50
      setNotifications(data);
      const count = await apiClient.getUnreadNotificationsCount();
      setUnreadCount(count);
    } catch (error) {
      console.error('Failed to fetch notifications', error);
    } finally {
        setLoading(false);
    }
  };

  useEffect(() => {
    fetchNotifications();
    
    // Request notification permission on mount
    if (typeof window !== 'undefined' && 'Notification' in window) {
      if (Notification.permission === 'default') {
        Notification.requestPermission();
      }
    }

    // Poll every minute
    const interval = setInterval(async () => {
      const oldUnreadCount = unreadCount;
      await fetchNotifications();
      
      // If we have new unread notifications, trigger a browser alert
      // We check if the unread count increased specifically because of a 'task_due_soon'
      // But for simplicity, we alert on any NEW unread notification if it's task-related.
    }, 60000);
    return () => clearInterval(interval);
  }, [unreadCount]);

  // Special effect to trigger alerts when unreadCount increases
  useEffect(() => {
    if (notifications.length > 0) {
      const latest = notifications[0];
      if (!latest.is_read && (latest.type === 'task_due_soon' || latest.type === 'task_overdue')) {
        // Trigger browser notification
        if (typeof window !== 'undefined' && 'Notification' in window && Notification.permission === 'granted') {
          new window.Notification("Todo Objective Recall", {
            body: latest.message,
            icon: '/favicon.ico' // Or a custom icon
          });
        }
      }
    }
  }, [notifications]);

  // Close on click outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);
  
  const handleMarkAsRead = async (id: string) => {
      try {
          await apiClient.markNotificationAsRead(id);
          setNotifications(prev => prev.map(n => n.id === id ? { ...n, is_read: true } : n));
          setUnreadCount(prev => Math.max(0, prev - 1));
      } catch (error) {
          console.error('Failed to mark as read', error);
      }
  };

  const handleMarkAllRead = async () => {
      try {
          await apiClient.markAllNotificationsAsRead();
          setNotifications(prev => prev.map(n => ({ ...n, is_read: true })));
          setUnreadCount(0);
      } catch (error) {
          console.error('Failed to mark all as read', error);
      }
  };

  const getIcon = (type: Notification['type']) => {
      switch (type) {
          case 'task_due': return <Calendar className="w-4 h-4 text-blue-500" />;
          case 'task_due_soon': return <Clock className="w-4 h-4 text-amber-500" />;
          case 'task_overdue': return <AlertCircle className="w-4 h-4 text-red-500" />;
          case 'recurring_spawned': return <RefreshCw className="w-4 h-4 text-green-500" />;
          default: return <Info className="w-4 h-4 text-gray-500" />;
      }
  };

  return (
    <div className="relative" ref={containerRef}>
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="relative p-2.5 rounded-xl hover:bg-gray-100/50 transition-all text-gray-500 hover:text-horizon-900 group"
      >
        <Bell className="w-5 h-5" />
        {unreadCount > 0 && (
          <span className="absolute top-2 right-2 flex h-2.5 w-2.5">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-red-500 border border-white"></span>
          </span>
        )}
      </button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 10, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 10, scale: 0.95 }}
            transition={{ type: "spring", stiffness: 300, damping: 30 }}
            className="absolute right-0 top-full mt-2 w-80 sm:w-96 bg-white/90 backdrop-blur-xl rounded-2xl shadow-xl shadow-gray-200/50 border border-white/50 z-50 overflow-hidden"
          >
            <div className="p-4 border-b border-gray-100 flex justify-between items-center">
                <h3 className="font-black text-sm uppercase tracking-wider text-gray-900">Notifications</h3>
                {unreadCount > 0 && (
                    <button 
                        onClick={handleMarkAllRead}
                        className="text-[10px] font-bold text-horizon-500 hover:text-horizon-700 uppercase tracking-widest"
                    >
                        Mark all read
                    </button>
                )}
            </div>
            
            <div className="max-h-[60vh] overflow-y-auto custom-scrollbar">
                {loading && notifications.length === 0 ? (
                    <div className="p-8 text-center text-gray-400 text-xs font-bold">Loading...</div>
                ) : notifications.length === 0 ? (
                    <div className="p-8 text-center text-gray-400">
                        <Bell className="w-8 h-8 mx-auto mb-2 opacity-50" />
                        <p className="text-xs font-bold">No new notifications</p>
                    </div>
                ) : (
                    <div className="divide-y divide-gray-50">
                        {notifications.map(notification => (
                            <div 
                                key={notification.id} 
                                className={`p-4 flex gap-3 transition-colors ${notification.is_read ? 'bg-transparent opacity-60' : 'bg-blue-50/30'}`}
                            >
                                <div className="flex-shrink-0 mt-0.5 p-1.5 bg-white rounded-lg shadow-sm">
                                    {getIcon(notification.type)}
                                </div>
                                <div className="flex-1 min-w-0">
                                    <p className="text-sm font-medium text-gray-800 leading-snug">
                                        {notification.message}
                                    </p>
                                    <p className="text-[10px] font-bold text-gray-400 mt-1">
                                        {new Date(notification.created_at).toLocaleString([], { dateStyle: 'short', timeStyle: 'short' })}
                                    </p>
                                </div>
                                {!notification.is_read && (
                                    <button 
                                        onClick={() => handleMarkAsRead(notification.id)}
                                        className="flex-shrink-0 text-gray-300 hover:text-horizon-500 transition-colors"
                                        title="Mark as read"
                                    >
                                        <Check className="w-4 h-4" />
                                    </button>
                                )}
                            </div>
                        ))}
                    </div>
                )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
