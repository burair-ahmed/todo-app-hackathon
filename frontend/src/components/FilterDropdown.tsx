'use client';

import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown, Check } from 'lucide-react';

interface Option {
  label: string;
  value: any;
  icon?: React.ReactNode;
}

interface FilterDropdownProps {
  label: string;
  value: any;
  options: Option[];
  onChange: (value: any) => void;
  icon?: React.ReactNode;
  className?: string;
}

export default function FilterDropdown({
  label,
  value,
  options,
  onChange,
  icon,
  className = ""
}: FilterDropdownProps) {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const selectedOption = options.find(opt => opt.value === value);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className={`relative ${className}`} ref={dropdownRef}>
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className={`flex items-center space-x-2 px-4 py-2.5 rounded-2xl transition-all duration-300 border-2
                  ${isOpen || value !== '' 
                    ? 'bg-white border-horizon-100 shadow-glass text-horizon-900' 
                    : 'bg-gray-50 border-transparent text-gray-500 hover:bg-gray-100'}`}
      >
        <div className="flex items-center space-x-2">
          {icon && <div className="text-gray-400">{icon}</div>}
          <span className="text-[10px] font-black uppercase tracking-wider">
            {selectedOption ? selectedOption.label : label}
          </span>
        </div>
        <ChevronDown className={`w-3.5 h-3.5 transition-transform duration-300 ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 10, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 10, scale: 0.95 }}
            transition={{ type: 'spring', damping: 20, stiffness: 300 }}
            className="absolute top-full left-0 mt-2 w-56 bg-white rounded-[24px] shadow-glass ring-1 ring-gray-100 z-50 overflow-hidden py-2 px-1.5"
          >
            <div className="max-h-64 overflow-y-auto custom-scrollbar">
              {options.map((option) => (
                <button
                  key={String(option.value)}
                  onClick={() => {
                    onChange(option.value);
                    setIsOpen(false);
                  }}
                  className={`w-full flex items-center justify-between px-4 py-3 rounded-2xl text-left transition-all
                            ${value === option.value 
                              ? 'bg-horizon-50 text-horizon-900' 
                              : 'hover:bg-gray-50 text-gray-600'}`}
                >
                  <div className="flex items-center space-x-3">
                    {option.icon && <div>{option.icon}</div>}
                    <span className="text-xs font-bold leading-none">{option.label}</span>
                  </div>
                  {value === option.value && (
                    <Check className="w-3.5 h-3.5 text-horizon-300" />
                  )}
                </button>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
