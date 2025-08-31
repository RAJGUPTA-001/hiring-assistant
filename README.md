# 🤖 TalentScout Hiring Assistant

An intelligent AI-powered chatbot designed to assist in the initial screening of technology candidates for recruitment agencies. Built with Streamlit and powered by Groq's LLM, this application provides a seamless candidate experience while gathering essential information and conducting technical assessments.

## 🎯 Features

### Core Functionality
- **Intelligent Greeting**: Professional welcome message with clear purpose explanation
- **Information Gathering**: Collects essential candidate details with validation
- **Tech Stack Analysis**: Identifies and processes candidate's technical skills
- **Dynamic Technical Questions**: Generates 3-5 relevant questions per technology
- **Context-Aware Conversations**: Maintains conversation flow and context
- **Graceful Exit**: Handles conversation termination with appropriate farewells

### User Interface
- **Beautiful Modern UI**: Gradient backgrounds, custom styling, and responsive design
- **Interactive Sidebar**: Real-time display of candidate information and progress
- **Progress Tracking**: Visual progress indicator showing conversation phases
- **Input Validation**: Regex-based validation for all user inputs
- **Spinner Feedback**: Loading indicators during LLM processing

### Technical Features
- **Groq LLM Integration**: Fast and reliable language model responses
- **Session Management**: Persistent conversation state across interactions
- **Data Privacy**: Secure handling of candidate information
- **Error Handling**: Robust error management and fallback mechanisms
- **Modular Architecture**: Clean, maintainable code structure

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Groq API key

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd assignmentbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:8501`

## 📖 Usage Guide

### For Candidates

1. **Start the Conversation**
   - The chatbot will greet you and explain its purpose
   - Simply type your responses in the chat input

2. **Provide Information**
   - Share your personal details (name, email, phone, experience, position, location)
   - The system will automatically extract and validate your information

3. **Declare Your Tech Stack**
   - List the technologies you're proficient in
   - Examples: "Python, Django, PostgreSQL, Docker, AWS"

4. **Answer Technical Questions**
   - Respond to 3-5 questions per technology
   - Questions are tailored to your declared skills

5. **Complete the Assessment**
   - Review your information in the sidebar
   - End the conversation when ready

### For Recruiters

- **Real-time Monitoring**: Watch candidate progress in the sidebar
- **Information Validation**: All inputs are validated using regex patterns
- **Technical Assessment**: Automated question generation based on tech stack
- **Data Export**: Candidate information is structured for easy processing

## 🏗️ Technical Architecture

### Technology Stack
- **Frontend**: Streamlit (Python web framework)
- **LLM Provider**: Groq (llama3-8b-8192 model)
- **Styling**: Custom CSS with modern design patterns
- **Validation**: Regex patterns for input validation
- **State Management**: Streamlit session state

### Key Components

#### 1. Conversation Flow Management
```python
conversation_phases = [
    'greeting',
    'info_gathering', 
    'tech_stack',
    'technical_questions',
    'conclusion'
]
```

#### 2. Input Validation Patterns
```python
VALIDATION_PATTERNS = {
    'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    'phone': r'^[\+]?[1-9][\d]{0,15}$',
    'name': r'^[a-zA-Z\s]{2,50}$',
    'experience': r'^\d+(\.\d+)?$',
    'location': r'^[a-zA-Z\s,.-]{2,100}$'
}
```

#### 3. LLM Integration
- **Model**: llama3-8b-8192 (via Groq)
- **Temperature**: 0.7 (balanced creativity and consistency)
- **Max Tokens**: 1000 (sufficient for detailed responses)
- **System Prompts**: Context-aware prompts for different conversation phases

### Data Flow

1. **User Input** → **Validation** → **Information Extraction**
2. **Tech Stack Detection** → **Question Generation** → **Assessment**
3. **Response Processing** → **Context Update** → **UI Refresh**

## 🎨 UI/UX Design

### Design Principles
- **Accessibility**: High contrast colors and clear typography
- **Responsiveness**: Adapts to different screen sizes
- **Feedback**: Visual indicators for all user actions
- **Consistency**: Uniform styling across all components

### Color Scheme
- **Primary**: Gradient from #667eea to #764ba2
- **Success**: #28a745 (green)
- **Info**: #007bff (blue)
- **Background**: #f8f9fa (light gray)

### Interactive Elements
- **Hover Effects**: Button animations and transitions
- **Loading States**: Spinners during LLM processing
- **Progress Indicators**: Visual progress tracking
- **Sidebar Updates**: Real-time information display

## 🔒 Data Privacy & Security

### Privacy Measures
- **Local Storage**: All data stored in session state (cleared on page refresh)
- **No Persistent Storage**: No candidate data is permanently stored
- **Input Validation**: Prevents malicious input injection
- **Secure API Calls**: Environment variable protection for API keys

### Compliance
- **GDPR Ready**: No personal data retention
- **Transparent Processing**: Clear information about data usage
- **User Control**: Easy conversation termination

## 🧪 Testing & Validation

### Input Validation Tests
- Email format validation
- Phone number format validation
- Name length and character validation
- Experience number validation
- Location format validation

### Conversation Flow Tests
- Greeting phase completion
- Information gathering accuracy
- Tech stack detection
- Question generation quality
- Exit handling

## 🚀 Deployment

### Local Deployment
```bash
streamlit run app.py
```

### Cloud Deployment (Optional)
1. **Streamlit Cloud**
   - Connect your GitHub repository
   - Set environment variables
   - Deploy automatically

2. **Heroku**
   - Add `Procfile` and `setup.sh`
   - Configure buildpacks
   - Set environment variables

3. **AWS/GCP**
   - Containerize with Docker
   - Deploy to ECS/GKE
   - Configure load balancing

## 🔧 Configuration

### Environment Variables
```env
GROQ_API_KEY=your_api_key_here
```

### Customization Options
- **Model Selection**: Change Groq model in `app.py`
- **Question Count**: Modify questions per technology
- **UI Colors**: Update CSS variables
- **Validation Rules**: Adjust regex patterns

## 📊 Performance Optimization

### LLM Response Optimization
- **Caching**: Session state prevents redundant calls
- **Error Handling**: Graceful fallbacks for API failures
- **Timeout Management**: Prevents hanging requests

### UI Performance
- **Efficient Rendering**: Minimal re-renders
- **State Management**: Optimized session state usage
- **Memory Management**: Automatic cleanup on page refresh

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Standards
- **PEP 8**: Python code formatting
- **Docstrings**: Function documentation
- **Type Hints**: Where applicable
- **Error Handling**: Comprehensive exception management

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Groq**: For providing fast and reliable LLM services
- **Streamlit**: For the excellent web framework
- **Open Source Community**: For various libraries and tools

## 📞 Support

For questions or issues:
- Create an issue in the repository
- Contact the development team
- Check the documentation

---

**Built with ❤️ for modern recruitment**
#   h i r i n g - a s s i s t a n t 
 
 
