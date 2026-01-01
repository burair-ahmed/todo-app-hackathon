import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
import { Task, TaskCreate, TaskUpdate, AuthResponse, LoginRequest, RegisterRequest, Tag } from '../types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    const baseUrl = API_BASE_URL.replace(/\/+$/, '');
    this.client = axios.create({
      baseURL: baseUrl,
      timeout: 100000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add request interceptor to include auth token
    this.client.interceptors.request.use(
      (config: any) => {
        const token = this.getToken();
        if (token) {
          config.headers = {
            ...config.headers,
            Authorization: `Bearer ${token}`,
          };
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Add response interceptor to handle auth errors
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        console.error("API Error Interceptor:", {
            status: error.response?.status,
            data: error.response?.data,
            headers: error.config?.headers
        });
        if (error.response?.status === 401) {
          // Clear token and redirect to login
          this.clearToken();
          // In a real app, you might want to redirect to login page
        }
        return Promise.reject(error);
      }
    );
  }

  private getToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('auth_token');
    }
    return null;
  }

  private setToken(token: string): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem('auth_token', token);
    }
  }

  private clearToken(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth_token');
    }
  }

  // Authentication methods
  async login(credentials: LoginRequest): Promise<AuthResponse> {
    const response = await this.client.post<AuthResponse>('/api/auth/login', credentials);
    this.setToken(response.data.access_token);
    return response.data;
  }

  async register(userData: RegisterRequest): Promise<AuthResponse> {
    const response = await this.client.post<AuthResponse>('/api/auth/register', userData);
    this.setToken(response.data.access_token);
    return response.data;
  }

  async logout(): Promise<void> {
    this.clearToken();
  }

  // Task methods
  async getTasks(params?: { 
    search?: string; 
    priority?: string; 
    completed?: boolean; 
    tag_id?: string;
    label?: string;
    sort_by?: string;
    order?: string;
  }): Promise<Task[]> {
    const response = await this.client.get<Task[]>('/api/tasks', { params });
    return response.data;
  }

  async createTask(taskData: TaskCreate): Promise<Task> {
    const response = await this.client.post<Task>('/api/tasks', taskData);
    return response.data;
  }

  async updateTask(taskId: string, taskData: TaskUpdate): Promise<Task> {
    const response = await this.client.put<Task>(`/api/tasks/${taskId}`, taskData);
    return response.data;
  }

  async deleteTask(taskId: string): Promise<void> {
    await this.client.delete(`/api/tasks/${taskId}`);
  }

  async toggleTaskCompletion(taskId: string): Promise<Task> {
    const response = await this.client.put<Task>(`/api/tasks/${taskId}/toggle`);
    return response.data;
  }

  // Tag methods
  async getTags(): Promise<Tag[]> {
    const response = await this.client.get<Tag[]>('/api/tags');
    return response.data;
  }

  async createTag(name: string): Promise<Tag> {
    const response = await this.client.post<Tag>('/api/tags', { name });
    return response.data;
  }

  async deleteTag(tagId: string): Promise<void> {
    await this.client.delete(`/api/tags/${tagId}`);
  }

  // Notification methods
  async getNotifications(skip = 0, limit = 20): Promise<any[]> {
    const response = await this.client.get<any[]>('/api/notifications', { params: { skip, limit } });
    return response.data;
  }

  async getUnreadNotificationsCount(): Promise<number> {
    const response = await this.client.get<number>('/api/notifications/unread-count');
    return response.data;
  }

  async markNotificationAsRead(notificationId: string): Promise<any> {
    const response = await this.client.post<any>(`/api/notifications/${notificationId}/read`);
    return response.data;
  }

  async markAllNotificationsAsRead(): Promise<void> {
    await this.client.post('/api/notifications/read-all');
  }

  // Check if user is authenticated
  isAuthenticated(): boolean {
    return this.getToken() !== null;
  }
}

export default new ApiClient();