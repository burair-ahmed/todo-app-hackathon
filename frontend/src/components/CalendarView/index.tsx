'use client';

import { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ChevronLeft, 
  ChevronRight, 
  Plus, 
  CheckCircle2, 
  Circle, 
  Calendar as CalendarIcon,
  ChevronDown
} from 'lucide-react';
import { Task } from '../../types';

interface CalendarViewProps {
  tasks: Task[];
  onAddTask: (date: Date) => void;
  onUpdateTask: (task: Task) => void;
}

export default function CalendarView({ tasks, onAddTask, onUpdateTask }: CalendarViewProps) {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [selectedDate, setSelectedDate] = useState<Date | null>(null);

  const monthNames = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];

  const daysInMonth = (month: number, year: number) => new Date(year, month + 1, 0).getDate();
  const firstDayOfMonth = (month: number, year: number) => new Date(year, month, 1).getDay();

  const calendarDays = useMemo(() => {
    const month = currentDate.getMonth();
    const year = currentDate.getFullYear();
    const days: Date[] = [];
    
    const prevMonthDays = firstDayOfMonth(month, year);
    const prevMonth = new Date(year, month, 0);
    for (let i = prevMonthDays - 1; i >= 0; i--) {
      days.push(new Date(year, month - 1, prevMonth.getDate() - i));
    }

    const totalDays = daysInMonth(month, year);
    for (let i = 1; i <= totalDays; i++) {
      days.push(new Date(year, month, i));
    }

    const remainingDays = 42 - days.length; // 6 rows of 7 days
    for (let i = 1; i <= remainingDays; i++) {
      days.push(new Date(year, month + 1, i));
    }

    return days;
  }, [currentDate]);

  const nextMonth = () => setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 1));
  const prevMonth = () => setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, 1));
  const goToToday = () => setCurrentDate(new Date());

  const getTasksForDate = (date: Date) => {
    return tasks.filter(task => {
      if (!task.due_date) return false;
      const d = new Date(task.due_date);
      return d.getDate() === date.getDate() && 
             d.getMonth() === date.getMonth() && 
             d.getFullYear() === date.getFullYear();
    });
  };

  return (
    <div className="flex flex-col h-full space-y-6">
      {/* Calendar Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2 bg-white rounded-2xl p-1 shadow-sm ring-1 ring-gray-100">
            <button 
              onClick={prevMonth}
              className="p-2 hover:bg-gray-50 rounded-xl text-gray-400 transition-all"
            >
              <ChevronLeft className="w-5 h-5" />
            </button>
            <div className="px-4 py-1">
              <h2 className="text-lg font-black text-gray-900 min-w-[140px] text-center">
                {monthNames[currentDate.getMonth()]} {currentDate.getFullYear()}
              </h2>
            </div>
            <button 
              onClick={nextMonth}
              className="p-2 hover:bg-gray-50 rounded-xl text-gray-400 transition-all"
            >
              <ChevronRight className="w-5 h-5" />
            </button>
          </div>
          <button 
            onClick={goToToday}
            className="px-6 py-3 bg-white hover:bg-gray-50 text-gray-900 rounded-2xl text-xs font-black uppercase tracking-widest transition-all shadow-sm ring-1 ring-gray-100"
          >
            Today
          </button>
        </div>

        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-2 text-[10px] font-black uppercase tracking-widest text-gray-400">
             <div className="flex items-center gap-1.5"><div className="w-2 h-2 rounded-full bg-horizon-300" /> Total</div>
             <div className="flex items-center gap-1.5"><div className="w-2 h-2 rounded-full bg-green-500" /> Done</div>
             <div className="flex items-center gap-1.5"><div className="w-2 h-2 rounded-full bg-red-400" /> Pending</div>
          </div>
        </div>
      </div>

      {/* Week Day Labels */}
      <div className="grid grid-cols-7 gap-4 px-2">
        {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
          <div key={day} className="text-center text-[10px] font-black uppercase tracking-[0.2em] text-gray-400">
            {day}
          </div>
        ))}
      </div>

      {/* Calendar Grid */}
      <div className="grid grid-cols-7 gap-4 flex-1">
        {calendarDays.map((date, idx) => {
          const isCurrentMonth = date.getMonth() === currentDate.getMonth();
          const isToday = date.toDateString() === new Date().toDateString();
          const dayTasks = getTasksForDate(date);
          const completed = dayTasks.filter(t => t.completed).length;
          const incomplete = dayTasks.length - completed;

          return (
            <motion.div
              layoutId={`date-${date.toISOString()}`}
              key={date.toISOString()}
              onClick={() => isCurrentMonth && setSelectedDate(date)}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: idx * 0.01 }}
              className={`relative h-48 p-5 rounded-[32px] transition-all duration-300 group
                         ${isCurrentMonth 
                           ? 'bg-white shadow-soft-float hover:scale-[1.02] hover:shadow-glass cursor-pointer' 
                           : 'bg-gray-50/30 ring-1 ring-gray-100/50 cursor-default'}
                         ${isToday && isCurrentMonth ? 'ring-2 ring-horizon-300 bg-horizon-50/20' : 'ring-1 ring-gray-100'}
                         ${selectedDate?.toDateString() === date.toDateString() && isCurrentMonth ? 'ring-2 ring-horizon-900 z-10' : ''}`}
            >
              {isCurrentMonth ? (
                <>
                  <div className="flex items-center justify-between mb-4">
                    <span className={`text-base font-black transition-colors ${isToday ? 'text-horizon-900' : 'text-gray-900'}`}>
                      {date.getDate()}
                    </span>
                    {dayTasks.length > 0 && (
                       <div className="w-2 h-2 rounded-full bg-horizon-300 animate-pulse" />
                    )}
                  </div>

                  {dayTasks.length > 0 ? (
                    <div className="space-y-3">
                       <div className="flex items-center justify-between text-[10px] font-black uppercase tracking-wider text-gray-400">
                          <span>Objectives</span>
                          <span className="text-gray-900">{dayTasks.length}</span>
                       </div>
                       <div className="w-full bg-gray-100 h-1.5 rounded-full overflow-hidden flex">
                          <div className="h-full bg-green-500" style={{ width: `${(completed / dayTasks.length) * 100}%` }} />
                          <div className="h-full bg-red-400" style={{ width: `${(incomplete / dayTasks.length) * 100}%` }} />
                       </div>
                       <div className="flex flex-wrap gap-2">
                          {completed > 0 && (
                            <div className="flex items-center gap-1 text-[10px] font-black text-green-600 bg-green-50 px-2 py-1 rounded-lg">
                              <CheckCircle2 className="w-3 h-3" /> {completed}
                            </div>
                          )}
                          {incomplete > 0 && (
                            <div className="flex items-center gap-1 text-[10px] font-black text-red-500 bg-red-50 px-2 py-1 rounded-lg">
                              <Circle className="w-3 h-3" /> {incomplete}
                            </div>
                          )}
                       </div>
                    </div>
                  ) : (
                    <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                       <div className="p-3 bg-gray-50 rounded-2xl">
                          <Plus className="w-6 h-6 text-gray-300" />
                       </div>
                    </div>
                  )}
                </>
              ) : null}
            </motion.div>
          );
        })}
      </div>

      {/* Date Detail Popover */}
      <AnimatePresence>
        {selectedDate && (
          <>
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setSelectedDate(null)}
              className="fixed inset-0 z-[110]"
            />
            <motion.div
              layoutId={`date-${selectedDate.toISOString()}`}
              className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-sm bg-white rounded-[40px] shadow-glass-xl z-[111] overflow-hidden flex flex-col"
            >
              <div className="p-8 bg-horizon-900 text-white relative">
                 <div className="flex justify-between items-start mb-6">
                    <div>
                       <h3 className="text-3xl font-black">
                          {selectedDate.getDate()} {monthNames[selectedDate.getMonth()]}
                       </h3>
                       <p className="text-horizon-200 font-bold text-sm tracking-widest uppercase mt-1">
                          {selectedDate.toLocaleDateString(undefined, { weekday: 'long' })}
                       </p>
                    </div>
                    <button 
                      onClick={() => {
                        onAddTask(selectedDate);
                        setSelectedDate(null);
                      }}
                      className="p-3 bg-white/10 hover:bg-white/20 rounded-2xl transition-all group"
                    >
                       <Plus className="w-6 h-6 transform group-hover:rotate-90 transition-transform" />
                    </button>
                 </div>

                 <div className="flex items-center space-x-6">
                    <div className="space-y-1">
                       <p className="text-[10px] font-black uppercase text-horizon-300 tracking-wider">Total</p>
                       <p className="text-xl font-black">{getTasksForDate(selectedDate).length}</p>
                    </div>
                    <div className="w-px h-8 bg-white/10" />
                    <div className="space-y-1">
                       <p className="text-[10px] font-black uppercase text-green-300 tracking-wider">Done</p>
                       <p className="text-xl font-black">{getTasksForDate(selectedDate).filter(t => t.completed).length}</p>
                    </div>
                    <div className="w-px h-8 bg-white/10" />
                    <div className="space-y-1">
                       <p className="text-[10px] font-black uppercase text-red-300 tracking-wider">Pending</p>
                       <p className="text-xl font-black">{getTasksForDate(selectedDate).filter(t => !t.completed).length}</p>
                    </div>
                 </div>
              </div>

              <div className="flex-1 p-8 overflow-y-auto max-h-[400px] space-y-4">
                 {getTasksForDate(selectedDate).length === 0 ? (
                    <div className="text-center py-10">
                       <p className="text-gray-400 font-bold">No objectives for this date.</p>
                    </div>
                 ) : (
                    getTasksForDate(selectedDate).map(task => (
                       <div key={task.id} className="flex items-center space-x-4 p-4 rounded-2xl bg-gray-50 border border-transparent hover:border-gray-100 transition-all group">
                          <button 
                            onClick={() => onUpdateTask({...task, completed: !task.completed})}
                            className={`w-6 h-6 rounded-lg flex items-center justify-center transition-all
                                      ${task.completed ? 'bg-horizon-900 text-white' : 'border-2 border-gray-200 bg-white'}`}
                          >
                             {task.completed && <CheckCircle2 className="w-4 h-4" />}
                          </button>
                          <div className="flex-1 min-w-0">
                             <p className={`text-sm font-black truncate ${task.completed ? 'line-through text-gray-400' : 'text-gray-900'}`}>
                                {task.title}
                             </p>
                             <div className="flex items-center space-x-2 mt-1">
                                <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded-md border
                                               ${task.priority === 'high' ? 'bg-red-50 text-red-500 border-red-100' :
                                                 task.priority === 'medium' ? 'bg-orange-50 text-orange-500 border-orange-100' :
                                                 'bg-blue-50 text-blue-500 border-blue-100'}`}>
                                   {task.priority}
                                </span>
                             </div>
                          </div>
                       </div>
                    ))
                 )}
              </div>
              
              <div className="p-8 pt-0">
                 <button 
                   onClick={() => setSelectedDate(null)}
                   className="w-full py-4 bg-gray-100 hover:bg-gray-200 text-gray-500 rounded-2xl font-black text-xs uppercase tracking-widest transition-all"
                 >
                    Close Portal
                 </button>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </div>
  );
}
