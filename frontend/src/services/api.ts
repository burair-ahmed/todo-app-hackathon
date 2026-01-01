import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds timeout
});

// Note: The auth token will be added directly in each API call using Better Auth session
// rather than using an interceptor, since the session is not globally available

export interface ChatRequest {
  conversation_id?: number;
  message: string;
}

export interface ChatResponse {
  conversation_id: number;
  response: string;
  tool_calls: Array<{
    name: string;
    result: {
      status: string;
      message: string;
      [key: string]: any;
    };
  }>;
}

export const chatApi = {
  /**
   * Send a message to the chat API
   */
  sendMessage: async (userId: string, request: ChatRequest, accessToken: string): Promise<ChatResponse> => {
    try {
      const response = await apiClient.post<ChatResponse>(
        `/api/${userId}/chat`,
        request,
        {
          headers: {
            'Authorization': `Bearer ${accessToken}`,
          }
        }
      );
      return response.data;
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  },

  /**
   * Get conversation history
   */
  getConversationHistory: async (userId: string, conversationId: number, accessToken: string) => {
    try {
      // This would be implemented when we have an endpoint for getting conversation history
      // For now, returning a placeholder
      return [];
    } catch (error) {
      console.error('Error getting conversation history:', error);
      throw error;
    }
  }
};

export default apiClient;