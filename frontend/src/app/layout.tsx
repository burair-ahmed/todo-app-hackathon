'use client';

import './globals.css';
import { AuthProvider } from '../services/auth-service';
import { ReactNode } from 'react';

export default function RootLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen selection:bg-horizon-200/30">
        <div className="bg-horizon-mesh" />
        <AuthProvider>
          <div className="relative min-h-screen">
            {children}
          </div>
        </AuthProvider>
      </body>
    </html>
  );
}