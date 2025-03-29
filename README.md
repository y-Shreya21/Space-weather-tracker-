# Space Weather Tracker Chatbot

Overview
The **Space Weather Tracker Chatbot** is a web-based chatbot application that provides real-time space weather updates. It interacts with users via a chat interface and fetches relevant space weather data.
 Features
- Real-time space weather updates
- Chat-based user interaction
- Historical chat storage in SQLite database
- API endpoints for chatbot responses and chat history retrieval
- Simple frontend UI with React.js

Tech Stack
- **Backend:** Flask, SQLite, Flask-CORS
- **Frontend:** React.js, Tailwind CSS, Axios, Recharts
- **Database:** SQLite

## Installation
### Backend Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/space-weather-chatbot.git
   cd space-weather-chatbot/backend
   ```
2. Install dependencies:
   ```sh
   pip install flask flask-cors sqlite3
   ```
3. Run the backend server:
   ```sh
   python app.py
   ```

### Frontend Setup
1. Navigate to the frontend folder:
   ```sh
   cd ../frontend
   ```
2. Install dependencies:
   ```sh
   npm install
   ```
3. Run the React development server:
   ```sh
   npm start
   ```

## API Endpoints
### Chat with Bot
- **Endpoint:** `POST /chat`
- **Description:** Sends a user message and receives a bot response.
- **Request Body:**
  ```json
  { "message": "Tell me about solar activity" }
  ```
- **Response:**
  ```json
  { "response": "Solar storm activity is currently moderate." }
  ```

### Get Chat History
- **Endpoint:** `GET /history`
- **Description:** Retrieves the last 20 chat messages from the database.
- **Response:**
  ```json
  {
    "history": [
      { "user": "What is the solar wind speed?", "bot": "Current speed is 450 km/s.", "timestamp": "2024-03-28 12:30:00" }
    ]
  }
  ```

## Future Improvements
- User authentication for personalized chat history
- Live space weather data from external APIs
- Voice-enabled chatbot


## Contributors
- First student  - Shreya yadav 
- Second Student - Priti Kumari



