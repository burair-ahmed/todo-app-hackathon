# CLAUDE.md (Frontend)

## Build and Development
- **Install Dependencies**: `npm install`
- **Run Dev Server**: `npm run dev`
- **Build Project**: `npm run build`
- **Linting**: `npm run lint`

## Project Structure
- `src/app`: Next.js App Router pages and layouts.
- `src/components`: Reusable UI components.
- `src/services`: API client and authentication context.
- `src/types`: TypeScript interfaces and enums.

## New Components (Phase III: AI Chatbot)
- `src/app/chat/page.tsx`: Chatbot page with authentication integration
- `src/components/ChatKitWrapper/ChatKitWrapper.tsx`: ChatKit UI integration component
- `src/services/api.ts`: Updated API service with chat functionality
- `src/services/auth.ts`: Updated authentication service for Better Auth integration

## Coding Style
- **Components**: Use functional components with TypeScript and `'use client'` where interactive.
- **Styling**: Use Tailwind CSS for layouts and custom CSS (`globals.css`) for complex meshes/gradients.
- **Animations**: Use Framer Motion for premium-feel transitions.
- **Icons**: Use `lucide-react` for all iconography.
- **API**: Use the centralized `api-client.ts` (Axios) for all backend communication.
- **Naming**: PascalCase for components, camelCase for variables/functions, kebab-case for files.
- **AI Integration**: Secure JWT token handling with Better Auth session integration.
