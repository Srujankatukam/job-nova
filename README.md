# JobNova - AI-Powered Job Board & Interview Coach
        
# ![JobNova AI Interview Assistant](frontend/public/images/RR.png)
 
## 🚀 Overview
      
**JobNova** is a next-generation job application platform that goes beyond simple listings. It combines a robust job search engine with an immersive **AI Mock Interview Coach**, creating a comprehensive career development ecosystem.
 
The centerpiece of JobNova is its **Real-Time Digital Human** integration. Using cutting-edge AI (Tavus Persona API) and low-latency streaming (LiveKit), candidates can practice interviews with a lifelike AI avatar that responds to both spoken and typed inputs in real-time, providing a safe and realistic environment to refine their skills.

## ✨ Key Features

### 🤖 AI Mock Interview Coach (The "Wow" Factor)
*   **Lifelike Avatar**: Interact with a hyper-realistic digital human that mimics human expressions and lip-syncing.
*   **Real-Time Conversation**: Talk to the avatar naturally with near-zero latency (<500ms).
*   **Hybrid Input**: Communicate via **Voice** (speech-to-speech) or **Text** (keyboard-to-speech).
*   **Intelligent Responses**: The avatar understands context and provides relevant, professional feedback.
*   **Visual Feedback**: Real-time indicators for connection quality and latency ensure a smooth experience.

### 💼 Smart Job Board
*   **Advanced Search**: Filter jobs by location, full-time/part-time, remote status, and tags.
*   **Personalized Recommendations**: Get job suggestions tailored to your profile (powered by simple matching logic).
*   **Rich Job Details**: Comprehensive view of requirements, benefits, and company culture.
*   **Company Profiles**: Detailed insights into hiring companies.

### 🎨 Modern & Responsive UI
*   **Glassmorphism Design**: Sleek, modern aesthetics with gradients and blurs.
*   **Mobile-First**: Fully responsive layout that looks great on desktop, tablet, and mobile.
*   **Smooth Animations**: Powered by Framer Motion for a polished user experience.

---

## 🛠️ Technical Architecture

JobNova is built with a modern, scalable tech stack designed for performance and real-time interaction.

### Frontend
*   **Framework**: [Next.js 16](https://nextjs.org/) (App Router)
*   **Language**: TypeScript
*   **Styling**: [Tailwind CSS 4](https://tailwindcss.com/)
*   **Real-Time Video**: [Daily.co](https://www.daily.co/) Client SDK
*   **Animations**: Framer Motion

### Backend
*   **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python)
*   **Real-Time Streaming**: [LiveKit](https://livekit.io/) Server SDK
*   **Validation**: Pydantic

### AI Services
*   **Avatar Generation**: [Tavus Persona API](https://tavus.io/)
*   **Streaming Infrastructure**: LiveKit

---

## 🚀 Getting Started

Follow these instructions to get a local copy up and running.

### Prerequisites
*   Node.js 18+ and npm
*   Python 3.12+ and pip
*   API Keys for **Tavus** and **LiveKit**

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/jobnova.git
cd jobnova
```

### 2. Backend Setup
The backend handles API requests, job data, and coordinates the AI session creation.

1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```

2.  Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4.  Configure Environment Variables:
    *   Copy `.env.example` to `.env`: `cp .env.example .env`
    *   Fill in your API keys in `.env`:
        ```env
        TAVUS_API_KEY=your_key
        TAVUS_PERSONA_ID=your_persona_id
        LIVEKIT_URL=your_url
        LIVEKIT_API_KEY=your_key
        LIVEKIT_API_SECRET=your_secret
        ```

5.  Run the server:
    ```bash
    python -m uvicorn app.main:app --reload
    ```
    *   API will act at: `http://localhost:8000`
    *   Docs at: `http://localhost:8000/docs`

### 3. Frontend Setup
The frontend provides the user interface and connects directly to the video streams.

1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```

2.  Install dependencies:
    ```bash
    npm install
    ```

3.  Run the development server:
    ```bash
    npm run dev
    ```

4.  Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 📖 Usage Guide

### Using the AI Interview Coach
1.  From the sidebar, click on **"AI Mock Interview"**.
2.  Click the **"Start Session"** button. The dashboard will initialize a secure room.
3.  Wait for the connection (usually < 3 seconds). You'll see "Live" status.
4.  **Speak** to the avatar or **Type** your questions in the text box.
5.  Receive instant, spoken feedback from the digital coach!

### Browsing Jobs
1.  Go to the **"Jobs"** tab.
2.  Use the search bar or filters to find roles.
3.  Click on any job card to view full details.

---

## 🔌 API Documentation

### Jobs
*   `GET /api/v1/jobs` - List all jobs with filters.
*   `GET /api/v1/jobs/{id}` - Get details for a specific job.
*   `GET /api/v1/jobs/recommendations` - Get recommended jobs.

### Avatar (AI)
*   `POST /api/v1/avatar/tavus/start` - Initialize a new AI session.
*   `POST /api/v1/avatar/tavus/send` - Send a text message to the avatar (handled via frontend usually).
*   `DELETE /api/v1/avatar/tavus/end/{id}` - End a session.

---

## 🌟 Unique Advantages

*   **Integrated Ecosystem**: Unlike standalone interview prep tools, JobNova integrates coaching directly into the job search flow.
*   **Hybrid Interaction Model**: Supports users who prefer typing *and* users who prefer speaking, making it versatile for different learning styles.
*   **Production-Ready Latency**: Engineered with LiveKit for sub-second responses, avoiding the "awkward pause" typical of many AI video tools.

---

## 🤝 Contributing

Contributions make the open-source community an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.


---

## Demo

Loom Link: https://www.loom.com/share/e19dcfa571b648a281d47cba98db517a

---
Architect and Developed by Srujankatukam❤️
