<<<<<<< HEAD
# JobNova - Full-Stack AI Job Board with Real-Time Digital Human

A production-ready full-stack application featuring an AI-powered job board with personalized recommendations and real-time digital human interactions using Tavus Persona API and LiveKit.

## 🎯 Features

- **Job Board**: Browse and filter job listings with a modern, responsive UI
- **AI Recommendations**: Personalized job recommendations based on your profile
- **Real-Time Digital Human**: Interact with an AI avatar that speaks your text in real-time
- **Low-Latency Streaming**: Synchronized audio/video streaming using LiveKit
- **Responsive Design**: Fully responsive for desktop and mobile (H5)

## 🏗️ Architecture

```
Frontend (Next.js)          Backend (FastAPI)           External Services
┌─────────────┐            ┌──────────────┐            ┌──────────────┐
│  Job Board  │───────────▶│  REST APIs   │            │   Tavus API │
│   UI        │            │              │───────────▶│   Persona   │
└─────────────┘            └──────────────┘            └──────────────┘
┌─────────────┐            ┌──────────────┐            ┌──────────────┐
│  Avatar     │◀──WebSocket│  WebSocket   │            │   LiveKit    │
│  View       │            │  Server      │───────────▶│   Server     │
└─────────────┘            └──────────────┘            └──────────────┘
```

## 📋 Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.10+
- **Tavus API Key** (for avatar generation)
- **LiveKit Server** (for real-time streaming) - Can use demo setup

## 🚀 Quick Start

### 1. Clone and Setup

```bash
cd JOBNOVA
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your API keys:
# - TAVUS_API_KEY
# - TAVUS_PERSONA_ID
# - LIVEKIT_URL
# - LIVEKIT_API_KEY
# - LIVEKIT_API_SECRET

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
echo "NEXT_PUBLIC_WS_URL=ws://localhost:8000" >> .env.local
echo "NEXT_PUBLIC_LIVEKIT_URL=wss://your-livekit-server.com" >> .env.local

# Run development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 📁 Project Structure

```
JOBNOVA/
├── frontend/                 # Next.js App Router
│   ├── app/
│   │   ├── page.tsx          # Job Board page
│   │   ├── avatar/
│   │   │   └── page.tsx      # Avatar interaction page
│   │   └── layout.tsx
│   ├── components/
│   │   ├── JobCard.tsx
│   │   ├── JobFilters.tsx
│   │   ├── RecommendationSection.tsx
│   │   └── AvatarView.tsx
│   ├── lib/
│   │   ├── api.ts            # API client
│   │   ├── websocket.ts      # WebSocket client
│   │   └── types.ts          # TypeScript types
│   └── hooks/
│       └── useAvatar.ts      # Avatar interaction hook
│
├── backend/                  # FastAPI
│   ├── app/
│   │   ├── main.py           # FastAPI app entry
│   │   ├── routers/
│   │   │   ├── jobs.py       # Job board endpoints
│   │   │   └── avatar.py     # Avatar endpoints
│   │   ├── services/
│   │   │   ├── tavus_service.py
│   │   │   ├── livekit_service.py
│   │   │   └── job_service.py
│   │   ├── schemas/
│   │   │   ├── job.py
│   │   │   └── avatar.py
│   │   ├── config.py         # Environment config
│   │   └── websocket.py      # WebSocket handlers
│   └── requirements.txt
│
└── README.md
```

## 🔌 API Endpoints

### Job Board APIs

- `GET /api/jobs` - Get all jobs (with optional filters)
  - Query params: `search`, `location`, `type`, `tags`, `minSalary`, `maxSalary`
- `GET /api/jobs/{job_id}` - Get job by ID
- `GET /api/jobs/recommendations` - Get personalized recommendations
  - Query params: `limit` (default: 10)

### Avatar APIs

- `POST /api/avatar/generate` - Generate avatar from text
  - Body: `{ "text": "Your text here" }`
  - Returns: `{ "sessionId": "...", "status": "pending" }`
- `GET /api/avatar/status/{session_id}` - Get generation status
- `WS /ws/avatar/{session_id}` - WebSocket for real-time updates
- `POST /api/avatar/livekit/token` - Get LiveKit access token
  - Body: `{ "room_name": "...", "participant_name": "..." }`

## 🔧 Environment Variables

### Backend (.env)

```env
# API Configuration
API_V1_PREFIX=/api
PROJECT_NAME=JobNova API
VERSION=1.0.0

# CORS Origins
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Tavus API
TAVUS_API_KEY=your_tavus_api_key_here
TAVUS_API_URL=https://api.tavus.io
TAVUS_PERSONA_ID=your_persona_id_here

# LiveKit
LIVEKIT_URL=wss://your-livekit-server.com
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
NEXT_PUBLIC_LIVEKIT_URL=wss://your-livekit-server.com
```

## 🎨 UI Features

### Job Board Page
- **Responsive Grid Layout**: Adapts from 3 columns (desktop) to 1 column (mobile)
- **Advanced Filtering**: Search, location, job type, tags, salary range
- **Recommendations Section**: AI-powered personalized job suggestions
- **Smooth Animations**: Framer Motion micro-interactions
- **Mobile-Optimized**: Touch-friendly filters with bottom sheet modal

### Avatar Page
- **Real-Time Video Streaming**: LiveKit-powered synchronized audio/video
- **Text Input**: Convert text to speech with avatar lip-sync
- **Status Updates**: WebSocket-based real-time status notifications
- **Connection Management**: Automatic reconnection and error handling

## 🔄 System Flow

1. **User browses jobs** → Frontend calls `/api/jobs`
2. **User clicks "Try AI Avatar"** → Navigates to `/avatar`
3. **User enters text** → Frontend calls `/api/avatar/generate`
4. **Backend processes**:
   - Sends text to Tavus API
   - Creates LiveKit room
   - Streams generated video/audio
5. **Frontend receives**:
   - WebSocket status updates
   - LiveKit stream connection
   - Renders synchronized avatar video

## 🧪 Testing

### Backend
```bash
cd backend
# Run with auto-reload
uvicorn app.main:app --reload

# Test endpoints
curl http://localhost:8000/api/jobs
curl http://localhost:8000/health
```

### Frontend
```bash
cd frontend
npm run dev
# Open http://localhost:3000
```

## 📦 Dependencies

### Frontend
- **Next.js 16+** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Animation library
- **Axios** - HTTP client
- **LiveKit Client** - Real-time streaming

### Backend
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **LiveKit** - Real-time streaming SDK
- **httpx** - Async HTTP client

## 🚢 Deployment

### Backend
1. Set environment variables on your hosting platform
2. Install dependencies: `pip install -r requirements.txt`
3. Run with: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

### Frontend
1. Build: `npm run build`
2. Start: `npm start`
3. Or deploy to Vercel/Netlify with environment variables configured

## 🐛 Troubleshooting

### Backend won't start
- Check Python version: `python --version` (needs 3.10+)
- Verify virtual environment is activated
- Check `.env` file exists and has required keys

### Frontend can't connect to backend
- Verify `NEXT_PUBLIC_API_URL` in `.env.local`
- Check CORS settings in backend `config.py`
- Ensure backend is running on port 8000

### Avatar not generating
- Verify Tavus API key is set correctly
- Check backend logs for API errors
- Ensure WebSocket connection is established

### LiveKit connection fails
- Verify LiveKit server URL and credentials
- Check token generation endpoint
- Ensure LiveKit server is accessible

## 📝 Notes

- **Mock Mode**: If Tavus/LiveKit credentials are not set, the system will run in mock mode for development
- **WebSocket**: Uses native WebSocket for real-time updates
- **Responsive**: Mobile-first design with breakpoints at 768px (md) and 1024px (lg)

## 🤝 Contributing

This is a prototype/demo application. For production use:
- Add authentication/authorization
- Implement database for job storage
- Add proper error logging and monitoring
- Set up CI/CD pipeline
- Add comprehensive tests

## 📄 License

This project is a demonstration application.

---

Built with ❤️ using Next.js, FastAPI, Tavus, and LiveKit

=======
# JobNova
>>>>>>> ce8386bfee3108ccb649c6b48fae348263721398
