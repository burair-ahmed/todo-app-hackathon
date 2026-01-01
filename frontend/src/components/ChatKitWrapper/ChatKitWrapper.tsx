'use client';

import { ChatKit, useChatKit } from '@openai/chatkit-react';
import { useEffect } from 'react';
import { useAuth } from '../../services/auth-service';

// Import the web component styles and script
// In a real implementation, you might need to import '@openai/chatkit' 
// if it contains the side-effect to register the custom element
// @openai/chatkit is a type definition package, so no side-effect import is needed.
// The web component registration is likely handled by @openai/chatkit-react or specific setup if needed. 

interface ChatKitWrapperProps {
  userId: string;
}

const ChatKitWrapper = ({ userId }: ChatKitWrapperProps) => {
  const { token } = useAuth();
  const apiKey = process.env.NEXT_PUBLIC_CHATKIT_API_KEY;
  const workflowId = process.env.NEXT_PUBLIC_CHATKIT_WORKFLOW_ID;

  const { ref, control } = useChatKit({
    api: {
      url: `${process.env.NEXT_PUBLIC_API_URL}/api/chatkit`,
      domainKey: apiKey || '00000000-0000-0000-0000-000000000000', 
      fetch: (url, options) => {
        const headers = new Headers(options?.headers);
        if (token) {
          headers.set('Authorization', `Bearer ${token}`);
        }
        return fetch(url, {
          ...options,
          headers,
        });
      },
    },
    theme: 'light',
  });

  if (!apiKey || apiKey === 'your-openai-api-key-here' || apiKey.length < 5) {
    return (
      <div className="flex flex-col items-center justify-center h-full p-8 text-center">
        <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-4">
          <p className="text-yellow-700">
            <strong>ChatKit Configuration Incomplete:</strong> Please ensure <code>NEXT_PUBLIC_CHATKIT_API_KEY</code> is set in your environment variables.
          </p>
        </div>
        <p className="text-gray-600">
          When using the custom Gemini backend, you can use a dummy value for the API key in <code>frontend/.env.local</code>.
        </p>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full overflow-hidden">
      <script src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js" async />
      <ChatKit ref={ref} control={control} className="h-full" />
    </div>
  );
};

export default ChatKitWrapper;