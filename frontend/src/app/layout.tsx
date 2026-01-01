import './globals.css';
import { ReactNode } from 'react';
import { ClientProviders } from '../components/ClientProviders';
import FloatingChatbot from '../components/FloatingChatbot/FloatingChatbot';

export const metadata = {
  title: 'Horizon Todo',
  description: 'Control your objectives with speed and style.',
};

export default function RootLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen selection:bg-horizon-200/30">
        <div className="bg-horizon-mesh" />
        <ClientProviders>
          {children}
          <FloatingChatbot />
        </ClientProviders>
      </body>
    </html>
  );
}