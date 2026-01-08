# 🤖 ChatBot AI - HR Assistant

An intelligent, voice-enabled HR chatbot built with Flask and WebSocket support. This chatbot can help you with employee information lookup, real-time weather updates, and provides an interactive conversational experience with voice recognition and text-to-speech capabilities.

## ✨ Features

### 🎯 Core Functionality
- **Employee Information Management**: Search employees by name or employee code
- **Real-time Weather Updates**: Get current weather information for major cities
- **Voice Recognition**: Speak your queries using the built-in microphone feature
- **Text-to-Speech**: Listen to responses with voice synthesis
- **Response Interruption**: Stop or interrupt ongoing responses by saying "stop" or typing a new query
- **Streaming Responses**: Real-time, chunk-based response delivery for better UX

### 🔌 Technical Features
- **WebSocket Support**: Real-time bidirectional communication
- **Session Management**: Individual session tracking for multiple users
- **Thread-based Processing**: Efficient handling of concurrent requests
- **Error Handling**: Comprehensive error management and logging
- **REST API**: HTTP endpoints for backward compatibility

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- pip (Python package manager)
- Modern web browser (Chrome, Edge, or Safari recommended for voice features)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/jiyajalan13/ChatBot-AI.git
   cd ChatBot-AI
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**
   - **Windows:**
     ```bash
     .venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

The chatbot uses OpenWeatherMap API for weather information. The API key is already configured in the code, but you can replace it with your own:

1. Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)
2. Replace the `WEATHER_API_KEY` in `chatbot.py`:
   ```python
   WEATHER_API_KEY = 'your-api-key-here'
   ```

## 🎮 Usage

### Running the Application

1. **Start the server:**
   ```bash
   python chatbot.py
   ```

2. **Access the application:**
   - Main Interface: `http://localhost:5000`
   - Test Endpoint: `http://localhost:5000/test`
   - Voice Test: `http://localhost:5000/voice-test`
   - Active Sessions: `http://localhost:5000/sessions`

### Example Queries

#### 👥 Employee Search
- "Find Yuvarani"
- "Tell me about Kshitij"
- "Employee VIPL2SP24054"
- "Show me details for Deepali"

#### 🌤️ Weather Information
- "Weather in Chennai"
- "Temperature in Bangalore"
- "What's the weather like in Mumbai?"

#### 🎤 Voice Commands
- Click the microphone icon and speak naturally
- Say "stop" or "interrupt" to cancel ongoing responses
- The bot will respond with both text and voice

#### ℹ️ General Commands
- "hello" - Get greeting and introduction
- "help" - View all available commands
- "time" or "date" - Get current date and time

## 📁 Project Structure

```
ChatBot-AI/
├── chatbot.py              # Main Flask application with WebSocket support
├── chatbot1.py             # Alternative/simplified version
├── requirements.txt        # Python dependencies
├── chtabot.css            # Styling for the chatbot interface
├── employeeeServices.js   # Client-side services and logic
├── templates/
│   ├── chatbot.html       # Main chatbot interface
│   └── chat.html          # Alternative chat interface
├── .gitignore             # Git ignore file
└── README.md              # This file
```

## 🛠️ Technology Stack

### Backend
- **Flask**: Web framework
- **Flask-SocketIO**: WebSocket support for real-time communication
- **Requests**: HTTP library for API calls
- **Threading**: Concurrent request handling

### Frontend
- **HTML5**: Structure
- **CSS3**: Styling
- **JavaScript**: Client-side logic
- **Web Speech API**: Voice recognition and synthesis
- **Socket.IO Client**: WebSocket communication

### APIs & Services
- **OpenWeatherMap API**: Weather information
- **Web Speech API**: Voice features

## 🎯 Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main chatbot interface |
| `/chat` | POST | HTTP chat endpoint (REST) |
| `/test` | GET | Server status and features |
| `/voice-test` | GET | Test voice capabilities |
| `/sessions` | GET | View active sessions (debugging) |

## 🔌 WebSocket Events

### Client → Server
- `connect`: Establish connection
- `disconnect`: Close connection
- `send_message`: Send a chat message
- `interrupt_response`: Manually interrupt response
- `voice_interrupt`: Voice-based interruption

### Server → Client
- `connected`: Connection confirmation
- `streaming_response`: Chunked response delivery
- `response_interrupted`: Response interruption notification
- `error`: Error messages

## 🛑 Interruption System

The chatbot supports intelligent response interruption:

### Interruption Keywords
- "stop"
- "interrupt"
- "cancel"
- "wait"
- "hold on"
- "pause"

### How It Works
1. Speak or type an interruption keyword
2. The current response stops immediately
3. You can ask a new question
4. The bot acknowledges the interruption

## 👥 Employee Database

The chatbot includes sample employee data for demonstration:
- Yuvarani Sitharaman (VIPL2SP24054)
- Kshitij Srivastava (VIPL3MR25018)
- Deepali Sghvi (VIPL3OT24020)

**Note**: Replace this with your actual employee database in production.

## 🔐 Security Considerations

⚠️ **Important**: This is a demonstration project. Before deploying to production:

1. Replace the hardcoded `SECRET_KEY` in `chatbot.py`
2. Use environment variables for sensitive data (API keys, secrets)
3. Implement proper authentication and authorization
4. Use HTTPS in production
5. Sanitize user inputs
6. Implement rate limiting
7. Use a proper database instead of hardcoded employee data

## 📊 Dependencies

Main dependencies (see `requirements.txt` for complete list):
- Flask==3.1.1
- requests==2.32.3
- transformers==4.52.3
- torch==2.7.0
- numpy==2.2.6

## 🐛 Troubleshooting

### Voice not working
- Ensure you're using HTTPS or localhost
- Check browser permissions for microphone
- Use Chrome, Edge, or Safari (better Web Speech API support)

### Weather API not responding
- Check your internet connection
- Verify the API key is valid
- Ensure the city name is spelled correctly

### WebSocket connection issues
- Check if port 5000 is available
- Disable browser extensions that might block WebSockets
- Check firewall settings

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

**Jiya Jalan**
- GitHub: [@jiyajalan13](https://github.com/jiyajalan13)

## 🙏 Acknowledgments

- OpenWeatherMap for weather API
- Flask and Flask-SocketIO communities
- Web Speech API documentation
- All contributors and users

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Made with ❤️ using Flask and WebSocket technology**
