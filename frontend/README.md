# Mental Health Tracker - Frontend

A modern, responsive React application for mental health tracking and AI-powered assessments.

## Features

- User authentication and profile management
- Mental health assessment with AI predictions
- Dashboard with progress tracking and visualizations
- Personalized recommendations and resources
- Doctor appointment booking
- Emergency alert system
- Responsive design for all devices

## Tech Stack

- **Framework**: React 19 with Vite
- **Routing**: React Router v6
- **Styling**: Bootstrap 5 + Custom CSS
- **HTTP Client**: Axios
- **Icons**: React Icons
- **State Management**: React Context API

## Getting Started

### Prerequisites

- Node.js 18+ and npm

### Installation

1. Install dependencies:

```bash
npm install
```

2. Configure environment variables:

```bash
cp .env.example .env
```

Edit `.env` and set your API base URL:

```
VITE_API_BASE_URL=http://localhost:5000
```

### Development

Start the development server:

```bash
npm run dev
```

The application will open at `http://localhost:3000`

### Build

Create a production build:

```bash
npm run build
```

Preview the production build:

```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/       # Reusable components
│   │   ├── common/       # Common UI components
│   │   ├── auth/         # Authentication components
│   │   ├── dashboard/    # Dashboard components
│   │   ├── assessment/   # Assessment components
│   │   ├── resources/    # Resource components
│   │   └── appointments/ # Appointment components
│   ├── pages/            # Page components
│   ├── context/          # React Context providers
│   ├── services/         # API services
│   ├── hooks/            # Custom React hooks
│   ├── utils/            # Utility functions
│   └── styles/           # Global styles
├── public/               # Static assets
└── .env                  # Environment variables
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Environment Variables

- `VITE_API_BASE_URL` - Backend API base URL
- `VITE_APP_NAME` - Application name
- `VITE_APP_VERSION` - Application version

## Contributing

Please follow the existing code structure and styling conventions.
