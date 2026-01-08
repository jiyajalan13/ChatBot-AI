from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import logging
import re
import requests
from datetime import datetime
import threading
import time

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Weather API configuration
WEATHER_API_KEY = '4452bf5eefbb3eda168ea00a120b4622'
WEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Global variables for managing interruptions
active_sessions = {}
response_threads = {}

# Employee data
employees = [
    {
        "User Code": "VIPL2SP24054",
        "User FirstName": "Yuvarani",
        "User SurName": "Sitharaman",
        "User Email": "Yuvarani@zobble.com",
        "User MobileNumber": "7825849879",
        "Reporting Authority Name": "Viral",
        "Reporting Authority Email": "Viral@zobble.com",
        "Gender": "Female",
        "User Date Of Jog": "18/11/2024",
        "City": "Chennai",
        "Department": "Risk Management",
        "Title": "Manager",
        "Firm": "Ernst & Young LLP",
        "OFFICE": "Chennai - Tidel Park",
        "EmployeeStatus": "Joined"
    },
    {
        "User Code": "VIPL3MR25018",
        "User FirstName": "Kshitij",
        "User SurName": "Srivastava",
        "User Email": "Kshitij@zobble.com",
        "User MobileNumber": "8427867844",
        "Reporting Authority Name": "Romit",
        "Reporting Authority Email": "Romit@zobble.com",
        "Gender": "Male",
        "User Date Of Jog": "01/04/2025",
        "City": "Bengaluru",
        "Department": "Risk Management",
        "Title": "Senior Consultant",
        "Firm": "Ernst & Young LLP",
        "OFFICE": "UB City",
        "EmployeeStatus": "Joined"
    },
    {
        "User Code": "VIPL3OT24020",
        "User FirstName": "Deepali",
        "User SurName": "Sghvi",
        "User Email": "Deepali@zobble.com",
        "User MobileNumber": "7073111284",
        "Reporting Authority Name": "Viral",
        "Reporting Authority Email": "Viral@zobble.com",
        "Gender": "Female",
        "User Date Of Jog": "03/12/2024",
        "City": "Chennai",
        "Department": "Risk Management",
        "Title": "Consultant",
        "Firm": "Ernst & Young LLP",
        "OFFICE": "Chennai - Tidel Park",
        "EmployeeStatus": "Joined"
    }
]

class InterruptibleResponse:
    def __init__(self, session_id):
        self.session_id = session_id
        self.interrupted = False
        self.current_response = ""
    
    def interrupt(self):
        self.interrupted = True
        logging.info(f"Response interrupted for session {self.session_id}")
    
    def is_interrupted(self):
        return self.interrupted

def get_weather(city):
    """Get weather information for a city"""
    try:
        params = {
            'q': city,
            'appid': WEATHER_API_KEY,
            'units': 'metric'
        }
        response = requests.get(WEATHER_BASE_URL, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'city': data['name']
            }
    except Exception as e:
        logging.error(f"Weather API error: {e}")
    return None

def find_employee_by_name(name):
    """Find employee by name"""
    name_lower = name.lower()
    for emp in employees:
        first_name = emp["User FirstName"].lower()
        last_name = emp["User SurName"].lower()
        if name_lower in first_name or name_lower in last_name:
            return emp
    return None

def find_employee_by_code(code):
    """Find employee by code"""
    for emp in employees:
        if emp["User Code"].lower() == code.lower():
            return emp
    return None

def format_employee_info(emp, voice_friendly=False):
    """Format employee information - voice_friendly for speech synthesis"""
    if voice_friendly:
        return f"""Here's the information for {emp['User FirstName']} {emp['User SurName']}. 
        Email: {emp['User Email']}. 
        Mobile: {emp['User MobileNumber']}. 
        Employee Code: {emp['User Code']}. 
        Title: {emp['Title']} in {emp['Department']}. 
        Office: {emp['OFFICE']} in {emp['City']}. 
        Reports to: {emp['Reporting Authority Name']}. 
        Joined on: {emp['User Date Of Jog']}. 
        Status: {emp['EmployeeStatus']}."""
    else:
        return f"""👤 **{emp['User FirstName']} {emp['User SurName']}**

📧 Email: {emp['User Email']}
📱 Mobile: {emp['User MobileNumber']}
🆔 Code: {emp['User Code']}

🏢 **Work Details:**
• Title: {emp['Title']}
• Department: {emp['Department']}
• Office: {emp['OFFICE']}
• City: {emp['City']}

👥 **Manager:** {emp['Reporting Authority Name']}
📅 **Joined:** {emp['User Date Of Jog']}
🏷️ **Status:** {emp['EmployeeStatus']}"""

def send_streaming_response(session_id, response_text, voice_response):
    """Send response in chunks to simulate streaming and allow interruption"""
    if session_id not in active_sessions:
        return
    
    response_handler = active_sessions[session_id]
    
    # Split response into chunks for streaming effect
    chunks = response_text.split('\n')
    current_chunk = ""
    
    for i, chunk in enumerate(chunks):
        if response_handler.is_interrupted():
            socketio.emit('response_interrupted', {
                'message': '⚠️ Response interrupted by user'
            }, room=session_id)
            return
        
        current_chunk += chunk + '\n'
        
        # Send chunk every few lines or at the end
        if i % 2 == 0 or i == len(chunks) - 1:
            socketio.emit('streaming_response', {
                'chunk': current_chunk,
                'is_final': i == len(chunks) - 1,
                'voice_response': voice_response if i == len(chunks) - 1 else None
            }, room=session_id)
            current_chunk = ""
            time.sleep(0.5)  # Simulate processing time

def get_chatbot_response(message, session_id):
    """Generate chatbot response with interruption support"""
    try:
        if session_id not in active_sessions:
            return None
        
        response_handler = active_sessions[session_id]
        message_lower = message.lower().strip()
        
        # Check for interruption keywords
        if any(word in message_lower for word in ['stop', 'interrupt', 'cancel', 'nevermind', 'wait']):
            return {
                'response': "🛑 **Stopped!** What would you like to know instead?",
                'voice_response': "Stopped! What would you like to know instead?"
            }
        
        # Greetings
        if any(word in message_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
            return {
                'response': "Hello! 👋 I'm your HR Assistant. I can help you with:\n\n• Employee information\n• Weather updates\n• General queries\n\nTry asking about employees like 'Yuvarani', 'Kshitij', or 'Deepali'!\n\n💡 **Tip:** You can interrupt me anytime by saying 'stop' or asking a new question!",
                'voice_response': "Hello! I'm your HR Assistant. I can help you with employee information, weather updates, and general queries. You can interrupt me anytime by saying stop or asking a new question!"
            }
        
        # Weather queries
        if 'weather' in message_lower or 'temperature' in message_lower:
            cities = ['chennai', 'bangalore', 'bengaluru', 'mumbai', 'delhi']
            city_found = None
            for city in cities:
                if city in message_lower:
                    city_found = city
                    break
            
            if city_found:
                if city_found == 'bengaluru':
                    city_found = 'bangalore'
                weather_info = get_weather(city_found)
                if weather_info:
                    visual_response = f"🌤️ **Weather in {weather_info['city']}:**\n🌡️ Temperature: {weather_info['temperature']}°C\n☁️ Condition: {weather_info['description'].title()}\n💧 Humidity: {weather_info['humidity']}%"
                    voice_response = f"The weather in {weather_info['city']} is {weather_info['temperature']} degrees celsius with {weather_info['description']} and humidity at {weather_info['humidity']} percent."
                    return {
                        'response': visual_response,
                        'voice_response': voice_response
                    }
                else:
                    return {
                        'response': f"Sorry, couldn't fetch weather for {city_found}. Please try again.",
                        'voice_response': f"Sorry, I couldn't fetch weather information for {city_found}. Please try again."
                    }
            else:
                return {
                    'response': "Please specify a city for weather info. Example: 'Weather in Chennai'",
                    'voice_response': "Please specify a city for weather information. For example, weather in Chennai."
                }
        
        # Employee search by code
        if 'vipl' in message_lower:
            code_match = re.search(r'(vipl\w+)', message_lower, re.IGNORECASE)
            if code_match:
                code = code_match.group(1)
                emp = find_employee_by_code(code)
                if emp:
                    return {
                        'response': format_employee_info(emp),
                        'voice_response': format_employee_info(emp, voice_friendly=True)
                    }
                else:
                    return {
                        'response': f"❌ No employee found with code: {code.upper()}",
                        'voice_response': f"No employee found with code {code.upper()}"
                    }
        
        # Employee search by name
        employee_names = ['yuvarani', 'kshitij', 'deepali']
        for name in employee_names:
            if name in message_lower:
                emp = find_employee_by_name(name)
                if emp:
                    return {
                        'response': format_employee_info(emp),
                        'voice_response': format_employee_info(emp, voice_friendly=True)
                    }
        
        # Help
        if 'help' in message_lower:
            return {
                'response': """🤖 **I can help you with:**

🔍 **Employee Search:**
• "Find Yuvarani" or "Tell me about Kshitij"
• "Employee VIPL2SP24054"

🌤️ **Weather:**
• "Weather in Chennai"
• "Temperature in Bangalore"

🎤 **Voice Commands:**
• Click the microphone and speak naturally
• I'll respond with both text and voice

🛑 **Interruption:**
• Say "stop" or "interrupt" to cancel current response
• Ask a new question anytime to change topic

💡 **Tips:**
• Just mention an employee's name
• Ask for weather in any major city
• Type 'hello' to start over""",
                'voice_response': "I can help you with employee search, weather information, and general queries. You can search for employees by name like Yuvarani or Kshitij, or ask for weather in cities like Chennai or Bangalore. You can interrupt me anytime by saying stop!"
            }
        
        # Time/Date
        if 'time' in message_lower or 'date' in message_lower:
            now = datetime.now()
            formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
            return {
                'response': f"🕐 **Current Time:** {formatted_time}",
                'voice_response': f"The current date and time is {now.strftime('%B %d, %Y at %I:%M %p')}"
            }
        
        # Default response
        return {
            'response': """🤔 I'm not sure about that. Here's what I can help with:

• **Employee Info:** Try "Find Yuvarani" or "Tell me about Kshitij"
• **Weather:** Ask "Weather in Chennai"
• **Help:** Type "help" for more options

What would you like to know?""",
            'voice_response': "I'm not sure about that. I can help you find employee information, get weather updates, or answer general questions. Try asking about an employee like Yuvarani or Kshitij, or ask for weather in a city like Chennai."
        }
        
    except Exception as e:
        logging.error(f"Error in chatbot response: {e}")
        return {
            'response': "Sorry, I encountered an error. Please try again.",
            'voice_response': "Sorry, I encountered an error. Please try again."
        }

# WebSocket Events
@socketio.on('connect')
def handle_connect():
    session_id = request.sid
    active_sessions[session_id] = InterruptibleResponse(session_id)
    logging.info(f"Client connected: {session_id}")
    emit('connected', {'session_id': session_id})

@socketio.on('disconnect')
def handle_disconnect():
    session_id = request.sid
    if session_id in active_sessions:
        del active_sessions[session_id]
    if session_id in response_threads:
        del response_threads[session_id]
    logging.info(f"Client disconnected: {session_id}")

@socketio.on('send_message')
def handle_message(data):
    session_id = request.sid
    message = data.get('message', '').strip()
    
    if not message:
        emit('error', {'message': 'Please enter a message.'})
        return
    
    # Interrupt any ongoing response
    if session_id in active_sessions:
        active_sessions[session_id].interrupt()
    
    # Create new response handler
    active_sessions[session_id] = InterruptibleResponse(session_id)
    
    logging.info(f"User message from {session_id}: {message}")
    
    # Get response
    response_data = get_chatbot_response(message, session_id)
    
    if response_data:
        # Start streaming response in a separate thread
        def stream_response():
            send_streaming_response(
                session_id, 
                response_data['response'], 
                response_data['voice_response']
            )
        
        # Cancel any existing response thread for this session
        if session_id in response_threads:
            response_threads[session_id] = None
        
        # Start new response thread
        thread = threading.Thread(target=stream_response)
        response_threads[session_id] = thread
        thread.start()
    else:
        emit('error', {'message': 'Failed to generate response'})

@socketio.on('interrupt_response')
def handle_interrupt():
    session_id = request.sid
    if session_id in active_sessions:
        active_sessions[session_id].interrupt()
        emit('response_interrupted', {
            'message': '⚠️ Response interrupted by user'
        })
        logging.info(f"Response manually interrupted for session {session_id}")

@socketio.on('voice_interrupt')
def handle_voice_interrupt(data):
    """Handle voice-based interruption"""
    session_id = request.sid
    transcript = data.get('transcript', '').lower()
    
    # Check if the transcript contains interruption keywords
    interrupt_keywords = ['stop', 'interrupt', 'cancel', 'wait', 'hold on', 'pause']
    if any(keyword in transcript for keyword in interrupt_keywords):
        if session_id in active_sessions:
            active_sessions[session_id].interrupt()
            emit('response_interrupted', {
                'message': '⚠️ Voice interruption detected'
            })
            logging.info(f"Voice interruption detected for session {session_id}: {transcript}")

# Regular HTTP routes for backward compatibility
@app.route('/')
def index():
    """Serve the main page"""
    return render_template('chatbot.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle traditional HTTP chat requests (backward compatibility)"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'response': 'No data received'}), 400
        
        message = data.get('message', '').strip()
        if not message:
            return jsonify({'response': 'Please enter a message.'})
        
        logging.info(f"HTTP message: {message}")
        
        # Create a temporary session for HTTP requests
        temp_session_id = f"http_{int(time.time())}"
        active_sessions[temp_session_id] = InterruptibleResponse(temp_session_id)
        
        response_data = get_chatbot_response(message, temp_session_id)
        
        # Clean up temporary session
        if temp_session_id in active_sessions:
            del active_sessions[temp_session_id]
        
        # Handle both old format (string) and new format (dict)
        if isinstance(response_data, dict):
            response = response_data.get('response', response_data.get('voice_response', 'Sorry, no response available.'))
            voice_response = response_data.get('voice_response', response)
        else:
            response = response_data
            voice_response = response_data
        
        logging.info(f"HTTP response generated")
        
        return jsonify({
            'response': response,
            'voice_response': voice_response
        })
        
    except Exception as e:
        logging.error(f"HTTP chat error: {e}")
        return jsonify({'response': 'Sorry, something went wrong. Please try again.'}), 500

@app.route('/test')
def test():
    """Test endpoint"""
    return jsonify({
        'status': 'Server is running with WebSocket support!',
        'timestamp': datetime.now().isoformat(),
        'employees_count': len(employees),
        'active_sessions': len(active_sessions),
        'features': [
            'Voice Recognition', 
            'Text-to-Speech', 
            'Employee Search', 
            'Weather API',
            'WebSocket Support',
            'Response Interruption',
            'Streaming Responses'
        ]
    })

@app.route('/voice-test')
def voice_test():
    """Test voice capabilities"""
    return jsonify({
        'message': 'Voice test successful with interruption support!',
        'voice_response': 'Hello! This is a voice test. Your HR Assistant is ready to help you with employee information and weather updates. You can interrupt me anytime by saying stop.',
        'interruption_keywords': ['stop', 'interrupt', 'cancel', 'wait', 'hold on', 'pause']
    })

@app.route('/sessions')
def get_sessions():
    """Get active sessions info (for debugging)"""
    return jsonify({
        'active_sessions': len(active_sessions),
        'response_threads': len(response_threads),
        'session_ids': list(active_sessions.keys())
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Cleanup function for graceful shutdown
def cleanup_sessions():
    """Clean up all active sessions"""
    global active_sessions, response_threads
    
    for session_id in list(active_sessions.keys()):
        if session_id in active_sessions:
            active_sessions[session_id].interrupt()
    
    active_sessions.clear()
    response_threads.clear()
    logging.info("All sessions cleaned up")

if __name__ == '__main__':
    print("🚀 Starting Enhanced HR Assistant Chatbot with WebSocket Support...")
    print("📍 Open your browser and go to: http://localhost:5000")
    print("🧪 Test the server at: http://localhost:5000/test")
    print("🎤 Voice test at: http://localhost:5000/voice-test")
    print("📊 Active sessions: http://localhost:5000/sessions")
    print("\n🎯 New Features:")
    print("• Real-time WebSocket communication")
    print("• Response interruption support")
    print("• Streaming responses")
    print("• Voice-based interruption")
    print("• Session management")
    print("\n🎤 Voice Features:")
    print("• Click the microphone button to speak")
    print("• Automatic speech-to-text conversion")
    print("• Text-to-speech responses")
    print("• Say 'stop' or 'interrupt' to cancel responses")
    print("• Works with Chrome, Edge, Safari")
    print("\n🛑 Interruption Commands:")
    print("• 'stop', 'interrupt', 'cancel', 'wait', 'hold on', 'pause'")
    
    try:
        socketio.run(app, debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down server...")
        cleanup_sessions()
        print("✅ Server stopped gracefully")

