'use client';

import { useState, useMemo, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../../services/auth-service';
import apiClient from '../../services/api-client';
import ProtectedRoute from '../../components/ProtectedRoute';
import TaskForm from '../../components/TaskForm';
import TaskList from '../../components/TaskList';
import FilterDropdown from '../../components/FilterDropdown';
import NotificationCenter from '../../components/NotificationCenter';
import CalendarView from '../../components/CalendarView';
import { Task, Tag } from '../../types';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  LayoutDashboard, 
  Plus, 
  Search, 
  LogOut, 
  User as UserIcon, 
  Calendar, 
  CheckCircle2, 
  Clock, 
  Zap,
  ChevronRight,
  TrendingUp,
  Settings,
  Filter,
  ArrowUpDown,
  Home,
  Briefcase,
  Layers,
  Flag,
  SortAsc,
  SortDesc
} from 'lucide-react';

export default function DashboardPage() {
  const { user, logout } = useAuth();
  const router = useRouter();
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [isAddingTask, setIsAddingTask] = useState(false);
  const [isSidebarExpanded, setIsSidebarExpanded] = useState(false);
  const [activeView, setActiveView] = useState<'dashboard' | 'schedule'>('dashboard');
  const [calendarSelectedDate, setCalendarSelectedDate] = useState<Date | undefined>(undefined);
  const [tasks, setTasks] = useState<Task[]>([]);
  
  // Phase II: Filter States
  const [searchQuery, setSearchQuery] = useState('');
  const [debouncedSearch, setDebouncedSearch] = useState('');
  const [filterPriority, setFilterPriority] = useState<string>('');
  const [filterTagId, setFilterTagId] = useState<string>('');
  const [filterCompleted, setFilterCompleted] = useState<boolean | undefined>(undefined);
  const [filterLabel, setFilterLabel] = useState<string>('');
  const [sortBy, setSortBy] = useState<string>('created_at');
  const [order, setOrder] = useState<'asc' | 'desc'>('desc');
  const [allTags, setAllTags] = useState<Tag[]>([]);

  useEffect(() => {
    fetchTags();
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearch(searchQuery);
    }, 500);
    return () => clearTimeout(timer);
  }, [searchQuery]);

  const fetchTags = async () => {
    try {
      const tags = await apiClient.getTags();
      setAllTags(tags);
    } catch (err) {
      console.error('Failed to fetch tags', err);
    }
  };

  const fetchTasks = async () => {
    try {
      const data = await apiClient.getTasks();
      setTasks(data);
    } catch (err) {
      console.error('Failed to fetch tasks', err);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, [refreshTrigger]);

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  const handleTaskCreated = (task: Task) => {
    setRefreshTrigger(prev => prev + 1);
    setIsAddingTask(false);
  };

  const handleTaskDone = () => setRefreshTrigger(prev => prev + 1);

  const handleUpdateTask = async (task: Task) => {
    try {
      await apiClient.updateTask(task.id as string, {
        completed: task.completed
      });
      setRefreshTrigger(prev => prev + 1);
    } catch (err) {
      console.error('Failed to update task', err);
    }
  };

  const handleCalendarAddTask = (date: Date) => {
    setCalendarSelectedDate(date);
    setIsAddingTask(true);
  };

  const filters = useMemo(() => ({
    search: debouncedSearch || undefined,
    priority: filterPriority || undefined,
    completed: filterCompleted,
    tag_id: filterTagId || undefined,
    label: filterLabel || undefined,
    sort_by: sortBy,
    order: order
  }), [debouncedSearch, filterPriority, filterCompleted, filterTagId, filterLabel, sortBy, order]);

  // Productivity Velocity Calculation
  const productivityStats = useMemo(() => {
    if (tasks.length === 0) return { velocity: 0, improvement: 0, message: "Add some tasks to see your velocity!" };
    
    const totalCount = tasks.length;
    const completedCount = tasks.filter(t => t.completed).length;
    const velocity = Math.round((completedCount / totalCount) * 100);
    
    const now = new Date();
    const oneWeekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
    const twoWeeksAgo = new Date(now.getTime() - 14 * 24 * 60 * 60 * 1000);
    
    const tasksThisWeek = tasks.filter(t => t.completed && t.completed_at && new Date(t.completed_at) >= oneWeekAgo).length;
    const tasksLastWeek = tasks.filter(t => t.completed && t.completed_at && new Date(t.completed_at) >= twoWeeksAgo && new Date(t.completed_at) < oneWeekAgo).length;
    
    let improvement = 0;
    let message = "";
    
    if (tasksLastWeek > 0) {
      improvement = Math.round(((tasksThisWeek - tasksLastWeek) / tasksLastWeek) * 100);
      if (improvement > 0) {
        message = `You're completing tasks ${improvement}% faster than last week. Keep it up!`;
      } else if (improvement < 0) {
        message = `You're ${Math.abs(improvement)}% behind last week's pace. You can do it!`;
      } else {
        message = `Maintaining a steady pace. Consistency is key!`;
      }
    } else if (tasksThisWeek > 0) {
      message = `Great start! You've completed ${tasksThisWeek} tasks this week.`;
    } else if (completedCount > 0) {
      message = `You've completed ${completedCount} tasks in total. Keep grinding!`;
    } else {
      message = `Start completing tasks to track your weekly progress!`;
    }
    
    return { velocity, improvement, message };
  }, [tasks]);

  // Animation Variants
  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.3
      }
    }
  };

  const item = {
    hidden: { opacity: 0, y: 20 },
    show: { 
      opacity: 1, 
      y: 0, 
      transition: { 
        duration: 0.6, 
        ease: [0.16, 1, 0.3, 1] as any
      } 
    }
  };

  return (
    <ProtectedRoute>
      <div className="flex min-h-screen bg-background-soft">
        {/* Sidebar - Desktop Only */}
        <aside className={`hidden lg:flex flex-col transition-all duration-300 bg-white border-r border-gray-100 py-8 sticky top-0 h-screen
                          ${isSidebarExpanded ? 'w-64 px-6 items-start' : 'w-24 px-0 items-center'}`}>
          <div className={`w-12 h-12 bg-horizon-900 rounded-2xl flex items-center justify-center text-white shadow-soft-float mb-8 ${isSidebarExpanded ? 'ml-0' : ''}`}>
            <Zap className="w-6 h-6 fill-current" />
          </div>
          
          <nav className="flex-1 flex flex-col space-y-4 w-full">
            <button 
              onClick={() => setActiveView('dashboard')}
              className={`flex items-center space-x-4 p-4 rounded-2xl transition-all shadow-sm w-full
                        ${activeView === 'dashboard' 
                          ? 'bg-horizon-50 text-horizon-300 shadow-sm' 
                          : 'text-gray-400 hover:bg-gray-50 hover:text-gray-600'}
                        ${!isSidebarExpanded && 'justify-center'}`}
            >
              <LayoutDashboard className="w-6 h-6 min-w-[24px]" />
              {isSidebarExpanded && <span className="font-black text-sm uppercase tracking-widest">Dashboard</span>}
            </button>
            <button 
              onClick={() => setActiveView('schedule')}
              className={`flex items-center space-x-4 p-4 rounded-2xl transition-all w-full
                        ${activeView === 'schedule' 
                          ? 'bg-horizon-50 text-horizon-300 shadow-sm' 
                          : 'text-gray-400 hover:bg-gray-50 hover:text-gray-600'}
                        ${!isSidebarExpanded && 'justify-center'}`}
            >
              <Calendar className="w-6 h-6 min-w-[24px]" />
              {isSidebarExpanded && <span className="font-black text-sm uppercase tracking-widest">Schedule</span>}
            </button>
            <button className={`flex items-center space-x-4 p-4 rounded-2xl text-gray-400 hover:bg-gray-50 hover:text-gray-600 transition-all w-full
                              ${!isSidebarExpanded && 'justify-center'}`}>
              <Settings className="w-6 h-6 min-w-[24px]" />
              {isSidebarExpanded && <span className="font-black text-sm uppercase tracking-widest">Settings</span>}
            </button>
            
            {/* Sidebar Toggle */}
            <button 
              onClick={() => setIsSidebarExpanded(!isSidebarExpanded)}
              className={`flex items-center space-x-4 p-4 rounded-2xl text-gray-400 hover:bg-horizon-50 hover:text-horizon-300 transition-all w-full
                              ${!isSidebarExpanded && 'justify-center'}`}
            >
              <div className={`transition-transform duration-500 ${isSidebarExpanded ? 'rotate-180' : ''}`}>
                <ChevronRight className="w-6 h-6 min-w-[24px]" />
              </div>
              {isSidebarExpanded && <span className="font-black text-sm uppercase tracking-widest">Collapse</span>}
            </button>
          </nav>

          <button 
            onClick={handleLogout}
            className={`flex items-center space-x-4 p-4 rounded-2xl text-gray-400 hover:bg-red-50 hover:text-red-500 transition-all mt-auto w-full
                        ${!isSidebarExpanded && 'justify-center'}`}
          >
            <LogOut className="w-6 h-6 min-w-[24px]" />
            {isSidebarExpanded && <span className="font-black text-sm uppercase tracking-widest">Sign Out</span>}
          </button>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-6 sm:p-10 lg:p-14 overflow-hidden">
          {/* Header Section */}
          <header className="flex flex-col md:flex-row justify-between items-start md:items-center mb-12 space-y-6 md:space-y-0">
            <div className="space-y-1">
              <h1 className="text-4xl font-black tracking-tight text-gray-900">
                Workspace <span className="text-horizon-gradient">Control</span>
              </h1>
              <p className="text-gray-500 font-bold tracking-tight">Welcome back, {user?.name || 'User'}.</p>
            </div>

            <div className="flex items-center space-x-4 w-full md:w-auto">
              <div className="relative flex-1 md:w-64">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input 
                  type="text" 
                  placeholder="Universal Search..." 
                  className="w-full pl-11 pr-4 py-3 bg-white border-none ring-1 ring-gray-100 rounded-2xl text-sm font-bold focus:ring-2 focus:ring-horizon-200 transition-all shadow-sm"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>
              
              <NotificationCenter />

              <button 
                onClick={() => setIsAddingTask(true)}
                className="bg-horizon-900 text-white p-3.5 rounded-2xl shadow-soft-float hover:scale-110 active:scale-95 transition-all"
              >
                <Plus className="w-6 h-6" />
              </button>
            </div>
          </header>

          {/* Bento Grid Layout */}
          {activeView === 'dashboard' ? (
            <motion.div 
              variants={container}
              initial="hidden"
              animate="show"
              className="grid grid-cols-1 md:grid-cols-12 gap-6"
            >
              {/* Main Task List - Large Column */}
              <motion.div variants={item} className="md:col-span-8 flex flex-col space-y-6">
                <div className="glass-surface p-8 rounded-[32px] flex-1">
                  <div className="flex flex-col space-y-6 mb-8">
                    <div className="flex justify-between items-center">
                      <div className="flex items-center space-x-3">
                        <div className="w-2 h-8 bg-horizon-300 rounded-full" />
                        <h2 className="text-2xl font-black">Active Objectives</h2>
                      </div>
                      <span className="text-xs font-black uppercase tracking-widest text-gray-400 bg-gray-50 px-3 py-1.5 rounded-full">
                        {new Date().toLocaleDateString(undefined, { month: 'long', day: 'numeric' })}
                      </span>
                    </div>

                    {/* Modernized Filters & Sorting Bar */}
                    <div className="flex flex-wrap items-center gap-3 pt-6 border-t border-gray-100">
                      <FilterDropdown
                        label="All Priorities"
                        icon={<Flag className="w-3.5 h-3.5" />}
                        value={filterPriority}
                        onChange={setFilterPriority}
                        options={[
                          { label: 'All Priorities', value: '' },
                          { label: 'High', value: 'high', icon: <div className="w-2 h-2 rounded-full bg-red-500" /> },
                          { label: 'Medium', value: 'medium', icon: <div className="w-2 h-2 rounded-full bg-orange-500" /> },
                          { label: 'Low', value: 'low', icon: <div className="w-2 h-2 rounded-full bg-blue-500" /> }
                        ]}
                      />

                      <FilterDropdown
                        label="All Tags"
                        icon={<Layers className="w-3.5 h-3.5" />}
                        value={filterTagId}
                        onChange={setFilterTagId}
                        options={[
                          { label: 'All Tags', value: '' },
                          ...allTags.map(tag => ({ label: tag.name, value: tag.id }))
                        ]}
                      />

                      <FilterDropdown
                        label="Context"
                        icon={<Home className="w-3.5 h-3.5" />}
                        value={filterLabel}
                        onChange={setFilterLabel}
                        options={[
                          { label: 'All Contexts', value: '' },
                          { label: 'Home', value: 'home', icon: <Home className="w-3 h-3 text-purple-500" /> },
                          { label: 'Work', value: 'work', icon: <Briefcase className="w-3 h-3 text-blue-500" /> }
                        ]}
                      />

                      <div className="flex items-center ml-auto space-x-2">
                        <FilterDropdown
                          label="Sort By"
                          icon={<ArrowUpDown className="w-3.5 h-3.5" />}
                          value={sortBy}
                          onChange={setSortBy}
                          options={[
                            { label: 'Recently Created', value: 'created_at' },
                            { label: 'Alphabetical', value: 'title' },
                            { label: 'Priority Level', value: 'priority' }
                          ]}
                        />
                        <button 
                          onClick={() => setOrder(order === 'asc' ? 'desc' : 'asc')}
                          className={`p-2.5 rounded-2xl transition-all shadow-sm border-2
                            ${order === 'desc' 
                              ? 'bg-horizon-900 text-white border-horizon-900 shadow-soft-float' 
                              : 'bg-white text-gray-400 border-gray-100 hover:border-gray-200'}`}
                        >
                          {order === 'desc' ? <SortDesc className="w-4 h-4" /> : <SortAsc className="w-4 h-4" />}
                        </button>
                      </div>
                    </div>
                  </div>
                  
                  <TaskList
                    key={`${refreshTrigger}-${JSON.stringify(filters)}`}
                    filters={filters}
                    onTaskUpdate={handleTaskDone}
                    onTaskDelete={handleTaskDone}
                  />
                </div>
              </motion.div>

              {/* Side Column - Sidebar widgets */}
              <motion.div variants={item} className="md:col-span-4 space-y-6">
                {/* Quick Profile Card */}
                <div className="glass-surface p-6 rounded-[32px] bg-white/40 border-none ring-1 ring-white/50">
                  <div className="flex items-center space-x-4">
                    <div className="w-14 h-14 bg-horizon-100 rounded-2xl flex items-center justify-center text-horizon-300 shadow-inner-glass">
                      <UserIcon className="w-6 h-6" />
                    </div>
                    <div>
                      <h3 className="font-black text-gray-900 leading-tight">{user?.name || 'User Profile'}</h3>
                      <p className="text-xs font-bold text-gray-400 uppercase tracking-widest">{user?.email}</p>
                    </div>
                  </div>
                </div>

                {/* Completion Stats */}
                <div className="glass-surface p-8 rounded-[32px] bg-horizon-900 text-white relative overflow-hidden group">
                  <div className="absolute top-0 right-0 p-4 opacity-20 group-hover:scale-110 transition-transform">
                    <TrendingUp className="w-20 h-20" />
                  </div>
                  <div className="relative z-10 space-y-6">
                    <div className="space-y-1">
                      <p className="text-xs font-black uppercase tracking-[0.2em] text-horizon-200">Productivity Velocity</p>
                      <h3 className="text-4xl font-black">{productivityStats.velocity}%</h3>
                    </div>
                    <div className="w-full bg-white/10 h-2 rounded-full overflow-hidden">
                      <motion.div 
                        initial={{ width: 0 }}
                        animate={{ width: `${productivityStats.velocity}%` }}
                        transition={{ duration: 1, ease: "easeOut" }}
                        className="bg-horizon-200 h-full rounded-full" 
                      />
                    </div>
                    <p className="text-sm font-bold text-white/60">{productivityStats.message}</p>
                  </div>
                </div>

                {/* Quick Info Box */}
                <div className="glass-surface p-8 rounded-[32px] bg-accent/10 border-none ring-1 ring-accent/20">
                  <div className="flex items-center space-x-3 mb-4">
                    <Clock className="w-5 h-5 text-accent" />
                    <h3 className="font-black text-gray-900">Current Focus</h3>
                  </div>
                  <p className="text-sm font-bold text-gray-600 leading-relaxed mb-6">
                    "Implement Phase II: Search, Filtering, and Sorting."
                  </p>
                  <button className="w-full py-4 bg-accent text-white rounded-2xl font-black text-sm flex items-center justify-center group shadow-soft-float">
                    View Detail <ChevronRight className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform" />
                  </button>
                </div>
              </motion.div>
            </motion.div>
          ) : (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="glass-surface p-10 rounded-[40px] h-[calc(100vh-280px)] overflow-y-auto scrollbar-hide"
            >
              <CalendarView 
                tasks={tasks} 
                onAddTask={handleCalendarAddTask} 
                onUpdateTask={handleUpdateTask}
              />
            </motion.div>
          )}
        </main>

        {/* Dynamic Task Sheet (Overlay/Modal) */}
        <AnimatePresence>
          {isAddingTask && (
            <>
              <motion.div 
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                onClick={() => setIsAddingTask(false)}
                className="fixed inset-0 bg-gray-900/40 backdrop-blur-sm z-[100]"
              />
              <motion.div 
                initial={{ x: '100%' }}
                animate={{ x: 0 }}
                exit={{ x: '100%' }}
                transition={{ type: 'spring', damping: 25, stiffness: 200 }}
                className="fixed top-0 right-0 h-full w-full max-w-md bg-white shadow-2xl z-[101] p-10 flex flex-col"
              >
                <div className="flex justify-between items-center mb-10">
                  <div className="space-y-1">
                    <h2 className="text-3xl font-black text-gray-900">Add <span className="text-horizon-gradient">Task</span></h2>
                    <p className="text-sm font-bold text-gray-400">Capture your next big objective.</p>
                  </div>
                  <button 
                    onClick={() => setIsAddingTask(false)}
                    className="p-3 bg-gray-50 text-gray-400 rounded-2xl hover:bg-red-50 hover:text-red-500 transition-all"
                  >
                    <Plus className="w-6 h-6 rotate-45" />
                  </button>
                </div>
                
                <div className="flex-1 overflow-y-auto pr-2 scrollbar-hide">
                  <TaskForm 
                    onTaskCreated={handleTaskCreated} 
                    onCancelEdit={() => setIsAddingTask(false)} 
                    initialDueDate={calendarSelectedDate}
                  />
                </div>
              </motion.div>
            </>
          )}
        </AnimatePresence>
      </div>
    </ProtectedRoute>
  );
}