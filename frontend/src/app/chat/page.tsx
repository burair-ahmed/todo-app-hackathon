'use client';

import { useAuth } from '../../services/auth-service';
import ProtectedRoute from '../../components/ProtectedRoute';
import ChatKitWrapper from '../../components/ChatKitWrapper/ChatKitWrapper';

const ChatPage = () => {
  const { user, loading } = useAuth();
  
  const userId = user?.id;

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-lg">Loading...</div>
      </div>
    );
  }

  if (!userId) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-lg">Unable to determine user ID. Please try logging in again.</div>
      </div>
    );
  }

  return (
    <ProtectedRoute>
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold mb-6 text-center">AI Task Assistant</h1>
          <p className="text-center text-gray-600 mb-8">
            Chat with our AI assistant to manage your tasks using natural language.
          </p>

          <div className="border rounded-lg shadow-lg h-[600px] flex flex-col">
            <ChatKitWrapper userId={userId} />
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
};

export default ChatPage;