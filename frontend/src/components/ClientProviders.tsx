'use client';

import { ReactNode } from 'react';
import { AuthProvider } from '../services/auth-service';

export function ClientProviders({ children }: { children: ReactNode }) {
  return (
    <AuthProvider>
      <div className="relative min-h-screen">
        {children}
      </div>
    </AuthProvider>
  );
}
