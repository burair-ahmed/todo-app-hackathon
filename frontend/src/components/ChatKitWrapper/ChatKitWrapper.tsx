'use client';

import { ChatKit, useChatKit } from '@openai/chatkit-react';
import { useEffect, useState } from 'react';
import { useAuth } from '../../services/auth-service';

// Import the web component styles and script
// In a real implementation, you might need to import '@openai/chatkit' 
// if it contains the side-effect to register the custom element
// @openai/chatkit is a type definition package, so no side-effect import is needed.
// The web component registration is likely handled by @openai/chatkit-react or specific setup if needed. 

interface ChatKitWrapperProps {
  userId: string;
}

interface ChatKitInnerProps {
  userId: string;
  token: string | null;
  apiKey: string;
  initialThreadId?: string;
}

const ChatKitInner = ({ userId, token, apiKey, initialThreadId }: ChatKitInnerProps) => {
  // Use 'any' cast to access threadId if types don't expose it explicitly yet
  const chat : any = useChatKit({
    api: {
      url: `${process.env.NEXT_PUBLIC_API_URL}/api/chatkit`,
      domainKey: apiKey, 
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
    // Pass threadId if available
    ...(initialThreadId ? { threadId: initialThreadId } : {}),
  });

  const { ref, control } = chat;

  // Persist threadId when it changes/is created
  useEffect(() => {
    if (chat.threadId) {
      console.log('Persisting threadId:', chat.threadId);
      localStorage.setItem('chatkit_thread_id', chat.threadId);
    } else if (chat.thread?.id) {
       console.log('Persisting threadId (fallback):', chat.thread.id);
       localStorage.setItem('chatkit_thread_id', chat.thread.id);
    }
  }, [chat.threadId, chat.thread]);

  return (
    <div className="flex flex-col h-full overflow-hidden relative">
      <script src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js" async />
      {/* <div className="absolute top-0 right-0 p-1 bg-gray-100 text-xs text-gray-400 z-10 opacity-50 hover:opacity-100">
        Thread: {chat.threadId || chat.thread?.id || 'New'}
      </div> */}
      <ChatKit ref={ref} control={control} className="h-full" />
    </div>
  );
};

const ChatKitWrapper = ({ userId }: ChatKitWrapperProps) => {
  const { token } = useAuth();
  const apiKey = process.env.NEXT_PUBLIC_CHATKIT_API_KEY;

  // State to hold threadId loaded from localStorage
  const [threadId, setThreadId] = useState<string | undefined>(undefined);
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    const stored = localStorage.getItem('chatkit_thread_id');
    if (stored) {
      setThreadId(stored);
    }
    setIsLoaded(true);
  }, []);

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

  if (!isLoaded) {
      return <div className="flex items-center justify-center h-full">Loading chat settings...</div>;
  }

  return <ChatKitInner userId={userId} token={token} apiKey={apiKey} initialThreadId={threadId} />;
};

export default ChatKitWrapper;