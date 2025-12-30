// Type definitions for the Todo Full-Stack Application

export interface User {
  id: string;
  email: string;
  name?: string;
  created_at: string;
  updated_at: string;
}

export type Priority = 'low' | 'medium' | 'high';
export type Recurrence = 'none' | 'daily' | 'weekly' | 'monthly';

export interface Tag {
  id: string;
  name: string;
  user_id: string;
}

export interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority: Priority;
  label?: 'home' | 'work';
  due_date?: string;
  recurrence: Recurrence;
  tags: Tag[];
  user_id: string;
  created_at: string;
  updated_at: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
  priority?: Priority;
  label?: 'home' | 'work';
  due_date?: string;
  recurrence?: Recurrence;
  tag_ids?: string[];
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  completed?: boolean;
  priority?: Priority;
  label?: 'home' | 'work';
  due_date?: string;
  recurrence?: Recurrence;
  tag_ids?: string[];
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  name: string;
}