import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
import { Task, TaskCreate, TaskUpdate, AuthResponse, LoginRequest, RegisterRequest } from '../types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 10000,
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
  async getTasks(): Promise<Task[]> {
    const response = await this.client.get<Task[]>('/api/tasks');
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

  // Check if user is authenticated
  isAuthenticated(): boolean {
    return this.getToken() !== null;
  }
}

export default new ApiClient();