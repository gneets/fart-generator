# Fart Generator - Frontend

React + TypeScript + Vite frontend for the Fart Generator application.

## Setup

### 1. Install dependencies

```bash
npm install
```

### 2. Start development server

```bash
npm run dev
```

The app will be available at http://localhost:5173

## Development

### Build for production

```bash
npm run build
```

### Preview production build

```bash
npm run preview
```

### Lint

```bash
npm run lint
```

## Project Structure

```
frontend/
├── src/
│   ├── components/   # Reusable UI components
│   ├── pages/        # Page components
│   ├── services/     # API clients
│   ├── hooks/        # Custom React hooks
│   ├── stores/       # State management (Zustand)
│   ├── types/        # TypeScript type definitions
│   ├── utils/        # Helper functions
│   ├── App.tsx       # Main app component
│   ├── main.tsx      # Entry point
│   └── index.css     # Global styles
├── public/           # Static assets
└── index.html        # HTML template
```

## Tech Stack

- React 18
- TypeScript
- Vite
- Tailwind CSS
- Zustand (state management)
- Axios (HTTP client)
- React Router (routing)
