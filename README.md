# 🤖 TalentScout Hiring Assistant
#Live at https://hiring-assistant-tkcl.onrender.com  

An intelligent AI-powered hiring assistant chatbot designed to streamline the technical recruitment process for technology positions. Built with Streamlit and powered by Large Language Models (LLMs).

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Prompt Engineering](#prompt-engineering)
- [Data Privacy](#data-privacy)
- [Troubleshooting](#troubleshooting)
-

## 🎯 Overview

TalentScout is a sophisticated hiring assistant that automates the initial screening of technical candidates. It conducts intelligent conversations, gathers candidate information, generates role-specific technical questions based on declared tech stacks, and provides immediate feedback while maintaining context throughout the interaction.

### Key Capabilities
- **Automated Screening**: Reduces manual effort in initial candidate assessment
- **Adaptive Questioning**: Generates questions tailored to each candidate's tech stack
- **Real-time Evaluation**: Provides immediate feedback on technical responses
- **Context Management**: Maintains conversation flow and remembers previous interactions
- **Privacy-First Design**: Implements data anonymization and secure handling practices

## ✨ Features

### Core Functionality
1. **Professional Greeting System**
   - Warm, personalized welcome messages
   - Clear explanation of the assessment process
   - Sets professional tone for the interaction

2. **Comprehensive Information Gathering**
   - Personal details (name, contact information)
   - Professional information (experience, desired position)
   - Technical skills and tech stack declaration
   - Availability and additional notes

3. **Dynamic Technical Assessment**
   - Auto-generates 3-5 questions per technology
   - Questions tailored to candidate's declared expertise
   - Covers practical knowledge and real-world scenarios

4. **Intelligent Response Evaluation**
   - LLM-powered answer assessment
   - Contextual feedback generation
   - Scoring system with detailed explanations

5. **Context & Conversation Management**
   - Maintains conversation history
   - Handles off-topic inputs gracefully
   - Recognizes exit intents
   - Implements fallback mechanisms

### Enhanced Features
- **Data Privacy Protection**: Anonymization of sensitive information
- **Progress Tracking**: Visual progress indicators and time tracking
- **Comprehensive Validation**: Input validation with helpful error messages
- **Responsive UI**: Modern, intuitive interface with smooth animations
- **Detailed Feedback**: Performance summary with actionable insights
- **Error Handling**: Robust fallback mechanisms for API failures

## 🛠️ Tech Stack

### Core Technologies
- **Python 3.8+**: Primary programming language
- **Streamlit**: Web application framework
- **Groq API**: LLM integration (supports multiple models)
- **python-dotenv**: Environment variable management

### LLM Models Supported
- Llama 3.1 70B Versatile (primary)
- GPT-4 compatible models
- Fallback to local responses when API unavailable

### Libraries & Dependencies
```
streamlit>=1.28.0
groq>=0.9.0
python-dotenv>=1.0.0
```

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git (for cloning repository)
- Groq API key (free tier available)

### Step 1: Clone the Repository
```bash
git clone https://github.com/RAJGUPTA-001/hiring-assistant.git
cd hiring-assistant
```
### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set Up Environment Variables
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### Step 4: Run the Application
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## ⚙️ Configuration

### Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Your Groq API key for LLM access | Yes |
| `DEBUG_MODE` | Enable debug logging (true/false) | No |
| `MAX_RETRIES` | Maximum API retry attempts | No |

### Customization Options
You can customize various aspects in the code:
- Question generation prompts
- Validation patterns
- UI styling (CSS)
- Fallback responses
- Scoring thresholds

## 💻 Usage

### For Candidates

1. **Start Application**
   - Click "Start Your Application" on the welcome screen
   
2. **Fill Information Form**
   - Enter personal and professional details
   - List your technical skills (comma-separated)
   - Review privacy notice
   
3. **Technical Assessment**
   - Answer generated questions based on your tech stack
   - Skip questions if needed
   - Receive immediate feedback
   
4. **Review Results**
   - View your overall score
   - Read detailed feedback
   - Understand next steps

### For Recruiters

1. **Access Candidate Data**
   - View anonymized candidate information in sidebar
   - Track progress in real-time
   - Review technical responses
   


### Conversation Commands
- Type "exit", "bye", or "quit" to end the interview
- Use "skip" button to move to next question
- Refresh page to start new session





### Data Flow
1. **User Input** → Validation → Processing
2. **LLM Request** → Response Generation → Formatting
3. **Answer Evaluation** → Scoring → Feedback
4. **Data Storage** → Anonymization → Session State

### State Management
- Uses Streamlit session state for persistence
- Maintains conversation history
- Tracks progress and scores
- Stores anonymized candidate data

## 🧠 Prompt Engineering

### System Prompts
The application uses carefully crafted system prompts to ensure:
- Consistent professional tone
- Focused hiring-related responses
- Technical accuracy in questions
- Fair evaluation criteria

### Key Prompt Strategies

1. **Role Definition**
```python
"You are TalentScout's intelligent hiring assistant..."
```

2. **Structured Output**
```python
"Return ONLY a JSON array with format: [...]"
```

3. **Context Injection**
```python
"Context: {candidate_info}, Generate questions for: {tech_stack}"
```

### Prompt Optimization Tips
- Be specific about output format
- Include examples when possible
- Set clear boundaries for responses
- Handle edge cases explicitly





## 📚 API Documentation

### LLM Integration

#### Function: `call_groq(prompt, sys_prompt, context)`
Sends requests to Groq API for response generation.

**Parameters:**
- `prompt` (str): User prompt
- `sys_prompt` (str): System instructions
- `context` (dict): Additional context

**Returns:**
- `str`: Generated response

**Example:**
```python
response = call_groq(
    prompt="Generate greeting",
    sys_prompt="You are a friendly interviewer",
    context={"role": "Senior Developer"}
)
```

### Validation Functions

#### Function: `validate(field, value)`
Validates user input based on field type.

**Parameters:**
- `field` (str): Field type (email, phone, etc.)
- `value` (str): Input value

**Returns:**
- `tuple`: (is_valid, error_message)

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**
   - Ensure `.env` file exists
   - Verify API key is valid
   - Check for typos in variable name

2. **No Questions Generated**
   - Check internet connection
   - Verify tech stack format
   - Review API rate limits

3. **Session State Lost**
   - Don't refresh during assessment
   - Complete forms before navigation
   - Check browser compatibility






## 🙏 Acknowledgments

- Streamlit team for the amazing framework
- Groq for providing LLM API access
- Open source community for inspiration



---

**Built with ❤️ by the TalentScout Team**
