import streamlit as st
import groq
import re
import json
import os
import hashlib
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq
import time

# ————————————————————————————————
# Load API key and initialize Groq client
# ————————————————————————————————
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
try:
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"❌ Failed to initialize Groq client: {str(e)}")
    client = None

# ————————————————————————————————
# Page config and CSS
# ————————————————————————————————
st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
  /* Enhanced CSS for better UI */
  .main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 10px;
    margin-bottom: 2rem;
    text-align: center;
    color: white;
  }
  .stButton>button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 0.5rem 2rem;
    border-radius: 5px;
    font-weight: bold;
    transition: all 0.3s;
  }
  .stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
  }
  .info-card {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    margin: 1rem 0;
    border-left: 4px solid #667eea;
  }
  .tech-badge {
    display: inline-block;
    background: #e9ecef;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    margin: 0.25rem;
    font-size: 0.9rem;
  }
  .question-card {
    background: white;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin: 1rem 0;
  }
  .score-display {
    font-size: 2rem;
    font-weight: bold;
    color: #667eea;
    text-align: center;
    padding: 2rem;
  }
</style>
""", unsafe_allow_html=True)

# ————————————————————————————————
# Validation patterns & helper
# ————————————————————————————————
VALIDATION_PATTERNS = {
    'email':      r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',
    'phone':      r'^[\+]?[0-9]{10,15}$',
    'first':      r'^[A-Za-z\s]{1,50}$',
    'last':       r'^[A-Za-z\s]{1,50}$',
    'experience': r'^\d+(\.\d+)?$',
    'location':   r'^[A-Za-z\s,.-]{1,100}$'
}

def validate(field, val):
    if not val or not val.strip():
        return False, "This field is required."
    pat = VALIDATION_PATTERNS.get(field)
    if pat and not re.fullmatch(pat, val.strip()):
        msgs = {
            'email':      "Please enter a valid email address.",
            'phone':      "Please enter a valid phone number (10-15 digits).",
            'first':      "First name must contain only letters.",
            'last':       "Last name must contain only letters.",
            'experience': "Enter a valid number of years.",
            'location':   "Enter a valid location."
        }
        return False, msgs.get(field, "Invalid input.")
    return True, ""

# ————————————————————————————————
# Data Privacy & Security
# ————————————————————————————————
def anonymize_data(data):
    """Anonymize sensitive data for storage/logging"""
    anonymized = data.copy()
    if 'email' in anonymized:
        email = anonymized['email']
        parts = email.split('@')
        if len(parts) == 2:
            anonymized['email'] = parts[0][:3] + '***@' + parts[1]
    if 'phone' in anonymized:
        phone = str(anonymized['phone'])
        anonymized['phone'] = phone[:3] + '***' + phone[-2:]
    if 'last_name' in anonymized:
        anonymized['last_name'] = anonymized['last_name'][:1] + '***'
    return anonymized

def hash_sensitive_data(data):
    """Hash sensitive data for secure storage"""
    sensitive_fields = ['email', 'phone']
    hashed_data = data.copy()
    for field in sensitive_fields:
        if field in hashed_data:
            hashed_data[field + '_hash'] = hashlib.sha256(
                str(hashed_data[field]).encode()
            ).hexdigest()[:16]
    return hashed_data

# ————————————————————————————————
# LLM helpers with context management
# ————————————————————————————————
def call_groq(prompt, sys_prompt="", context=None):
    """Enhanced LLM call with context management and fallback"""
    with st.spinner("🤖 AI is thinking..."):
        if client is None:
            # Fallback response when no API
            return generate_fallback_response(prompt)
        
        messages = []
        
        # System prompt for consistent behavior
        if not sys_prompt:
            sys_prompt = """You are TalentScout's intelligent hiring assistant. 
            Your role is to professionally screen technology candidates.
            Stay focused on the hiring process and technical assessment.
            Be friendly but professional. Do not deviate from hiring-related topics."""
        
        messages.append({"role": "system", "content": sys_prompt})
        
        # Add context if provided
        if context:
            messages.append({"role": "system", "content": f"Context: {json.dumps(context)}"})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            resp = client.chat.completions.create(
                model="openai/gpt-oss-20b",  # Using available model
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            st.warning(f"⚠️ LLM Error: {str(e)}. Using fallback response.")
            return generate_fallback_response(prompt)

def generate_fallback_response(prompt):
    """Generate fallback responses when LLM is unavailable"""
    prompt_lower = prompt.lower()
    
    if "greeting" in prompt_lower or "hello" in prompt_lower:
        return "Welcome to TalentScout! I'm your AI hiring assistant. I'll help screen your technical skills and gather your information for our recruitment team. Let's begin your application!"
    elif "technical" in prompt_lower or "question" in prompt_lower:
        return "Let me assess your technical knowledge with some questions."
    elif any(word in prompt_lower for word in ["bye", "exit", "quit", "end"]):
        return "Thank you for your time! Your application has been recorded. Our recruitment team will review it and contact you soon."
    else:
        return "I understand. Let's continue with your application process."

def gen_questions(stack):
    """Generate technical questions with better error handling"""
    sys_p = """You are an expert technical interviewer. Generate 3-5 relevant technical questions 
    for each technology in the tech stack. Questions should assess practical knowledge and experience.
    Return ONLY a JSON array with format: [{"technology": "tech_name", "questions": ["q1", "q2", ...]}]"""
    
    prompt = f"Generate technical interview questions for these technologies: {', '.join(stack)}"
    
    try:
        raw = call_groq(prompt, sys_p)
        
        # Better JSON extraction
        json_match = re.search(r'\[.*\]', raw, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            parsed = json.loads(json_str)
            return parsed
    except Exception as e:
        st.warning(f"⚠️ Using fallback questions. Error: {str(e)}")
    
    # Enhanced fallback questions
    fallback_questions = {
        "python": [
            "What are decorators in Python and how do you use them?",
            "Explain the difference between list and tuple in Python.",
            "How does Python's garbage collection work?",
            "What is the GIL and how does it affect multithreading?"
        ],
        "javascript": [
            "Explain the difference between var, let, and const.",
            "What is closure in JavaScript?",
            "How does async/await work?",
            "Explain event bubbling and capturing."
        ],
        "java": [
            "What is the difference between abstract class and interface?",
            "Explain the concept of garbage collection in Java.",
            "What are the main principles of OOP?",
            "How does the JVM work?"
        ],
        "react": [
            "What are React Hooks and why are they useful?",
            "Explain the Virtual DOM concept.",
            "What is the difference between state and props?",
            "How do you optimize React application performance?"
        ],
        "default": [
            "Describe your experience with this technology.",
            "What best practices do you follow?",
            "What challenging problem have you solved using this?",
            "How do you stay updated with this technology?"
        ]
    }
    
    result = []
    for tech in stack:
        tech_lower = tech.lower().strip()
        questions = fallback_questions.get(tech_lower, fallback_questions["default"])
        result.append({
            "technology": tech,
            "questions": questions[:3]  # Limit to 3 questions
        })
    return result

def evaluate_answer(question, answer, technology):
    """Evaluate candidate's answer using LLM"""
    if not answer or len(answer.strip()) < 10:
        return False, "Answer is too brief. Please provide more detail."
    
    sys_prompt = """You are a technical interviewer evaluating answers. 
    Be fair but thorough. Consider partial knowledge positively.
    Return a JSON with: {"correct": true/false, "feedback": "brief feedback", "score": 0-10}"""
    
    prompt = f"""Technology: {technology}
    Question: {question}
    Candidate's Answer: {answer}
    
    Evaluate the answer's correctness and completeness."""
    
    try:
        response = call_groq(prompt, sys_prompt)
        # Try to parse JSON from response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            return result.get("correct", False), result.get("feedback", "Good effort!"), result.get("score",0)
    except:
        pass
    
    # Simple heuristic evaluation as fallback
    
    return False, "cant connect to llm"

# ————————————————————————————————
# Conversation Management
# ————————————————————————————————
def check_exit_intent(text):
    """Check if user wants to exit the conversation"""
    exit_keywords = ["bye", "exit", "quit", "end", "stop", "finish", 
                     "goodbye", "thanks bye", "thank you bye", "done"]
    return any(keyword in text.lower() for keyword in exit_keywords)

def handle_unexpected_input(input_text):
    """Handle unexpected or off-topic inputs"""
    off_topic_keywords = ["weather", "sports", "news", "joke", "story", 
                         "game", "movie", "song", "food", "travel"]
    
    if any(keyword in input_text.lower() for keyword in off_topic_keywords):
        return True, "I appreciate your interest, but let's stay focused on your job application. How can I help you with the hiring process?"
    return False, ""

# ————————————————————————————————
# Session state initialization
# ————————————————————————————————
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

for k in ("greeted", "form_done", "questions", "q_index", "score", 
          "mark_list", "detailed_feedback", "interview_complete"):
    if k not in st.session_state:
        if k in ("greeted", "form_done", "interview_complete"):
            st.session_state[k] = False
        elif k in ("questions", "mark_list", "detailed_feedback", "conversation_history"):
            st.session_state[k] = []
        else:
            st.session_state[k] = 0

# ————————————————————————————————
# Display sidebar with enhanced info
# ————————————————————————————————
def show_sidebar():
    st.sidebar.markdown("## 📊 Application Progress")
    
    # Progress tracking
    steps = ["👋 Greeting", "📝 Information Form", "💻 Technical Interview", "✅ Conclusion"]
    current_step = 0
    if st.session_state.interview_complete:
        current_step = 3
    elif st.session_state.form_done:
        current_step = 2
    elif st.session_state.greeted:
        current_step = 1
    
    progress = (current_step + 1) / len(steps)
    st.sidebar.progress(progress)
    st.sidebar.markdown(f"**Current Step:** {steps[current_step]}")
    
    # Time tracking
    if 'start_time' not in st.session_state:
        st.session_state.start_time = datetime.now()
    
    elapsed = datetime.now() - st.session_state.start_time
    st.sidebar.markdown(f"**Time Elapsed:** {elapsed.seconds // 60}m {elapsed.seconds % 60}s")
    
    # Candidate information display
    data = st.session_state.get("form_data", {})
    if data:
        st.sidebar.markdown("## 👤 Candidate Profile")
        
        # Anonymized display for privacy
        anonymized = anonymize_data(data)
        info_items = [
            ("Name", f"{data.get('first_name', '')} {anonymized.get('last_name', '')}"),
            ("Email", anonymized.get('email', '')),
            ("Phone", anonymized.get('phone', '')),
            ("Experience", f"{data.get('experience', 0)} years"),
            ("Location", data.get('location', '')),
            ("Position", data.get('desired_position', ''))
        ]
        
        for label, value in info_items:
            if value:
                st.sidebar.write(f"**{label}:** {value}")
        
        # Tech stack display
        if data.get("tech_stack"):
            st.sidebar.markdown("## 🛠️ Technical Skills")
            tech_html = "".join([f'<span class="tech-badge" style="color: black; background-colour: cyan">{t}</span>' 
                               for t in data["tech_stack"]])
            st.sidebar.markdown(tech_html, unsafe_allow_html=True)
    
    # Interview progress
    if st.session_state.questions and st.session_state.form_done:
        st.sidebar.markdown("## 📈 Interview Progress")
        total_q = sum(len(q["questions"]) for q in st.session_state.questions)
        answered = st.session_state.q_index
        st.sidebar.progress(answered / total_q if total_q > 0 else 0)
        st.sidebar.write(f"Questions: {answered}/{total_q}")
        
        if st.session_state.score > 0:
            st.sidebar.write(f"Current Score: {st.session_state.score}/{answered}")

# ————————————————————————————————
# Main application with enhanced features
# ————————————————————————————————
def main():
    st.markdown("""
    <div class='main-header'>
        <h1>🤖 TalentScout Hiring Assistant</h1>
        <p style='margin-top: 1rem; font-size: 1.1rem;'>
            Your intelligent companion for technical recruitment
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    show_sidebar()
    
    # 1. Enhanced Greeting Phase
    if not st.session_state.greeted:
        # Generate personalized greeting
        greeting_prompt = """Generate a warm, professional greeting for TalentScout hiring assistant. 
        Mention that you'll help with: 
        1) Collecting candidate information
        2) Assessing technical skills
        3) Conducting a brief technical interview
        Keep it friendly and encouraging."""
        
        greeting = call_groq(greeting_prompt)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
            <div class='info-card' style="color: #4A90E2;">
                <h3>Welcome to TalentScout! 👋</h3>
                <p>{greeting}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.info("""
            📌 **What to expect:**
            - Quick registration form (2-3 minutes)
            - Technical assessment based on your skills
            - Immediate feedback on your responses
            - Secure handling of your information
            """)
            
            if st.button("🚀 Start Your Application", use_container_width=True):
                st.session_state.greeted = True
                st.session_state.conversation_history.append({
                    "timestamp": datetime.now(),
                    "action": "Application started"
                })
                st.rerun()
        return
    
    # 2. Enhanced Information Form
    if not st.session_state.form_done:
        st.header("📝 Candidate Information Form")
        st.markdown("Please fill in all required fields marked with *")
        
        with st.form("candidate_form", clear_on_submit=False):
            # Personal Information Section
            st.subheader("👤 Personal Information")
            col1, col2 = st.columns(2)
            
            with col1:
                first = st.text_input("First Name *", placeholder="John")
                email = st.text_input("Email Address *", placeholder="john.doe@example.com")
                phone = st.text_input("Phone Number *", placeholder="+1234567890")
            
            with col2:
                last = st.text_input("Last Name *", placeholder="Doe")
                location = st.text_input("Current Location *", placeholder="City, Country")
                experience = st.number_input("Years of Experience *", 0.0, 50.0, 0.0, 0.5)
            
            # Professional Information
            st.subheader("💼 Professional Information")
            position = st.text_input("Desired Position *", 
                                    placeholder="e.g., Senior Full Stack Developer")
            
            # Technical Skills
            st.subheader("💻 Technical Skills")
            tech = st.text_area(
                "List Your Tech Stack * (comma-separated)",
                placeholder="e.g., Python, JavaScript, React, Django, PostgreSQL, Docker",
                help="Enter all technologies, frameworks, and tools you're proficient in"
            )
            
            # Additional Information
            st.subheader("📋 Additional Information")
           
            
            notes = st.text_area(
                "Additional Notes (Optional)",
                placeholder="Any additional information you'd like to share..."
            )
            
            # Privacy Notice
            st.info("""
            🔒 **Privacy Notice:** Your information is handled securely and in compliance 
            with data protection regulations. We only use it for recruitment purposes.
            """)
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                submit = st.form_submit_button("Submit Application", use_container_width=True)
            
            if submit:
                # Comprehensive validation
                errors = []
                
                # Validate each field
                validations = [
                    ("first", first, "First name"),
                    ("last", last, "Last name"),
                    ("email", email, "Email"),
                    ("phone", phone, "Phone number"),
                    ("location", location, "Location")
                ]
                
                for field_type, value, field_name in validations:
                    is_valid, error_msg = validate(field_type, value)
                    if not is_valid:
                        errors.append(f"{field_name}: {error_msg}")
                
                if not position or not position.strip():
                    errors.append("Desired position is required.")
                
                if not tech or not tech.strip():
                    errors.append("Tech stack is required.")
                
                if experience < 0:
                    errors.append("Years of experience must be non-negative.")
                
                # Display errors or proceed
                if errors:
                    st.error("❌ Please fix the following errors:")
                    for error in errors:
                        st.write(f"• {error}")
                else:
                    # Store form data with privacy measures
                    form_data = {
                        "first_name": first.strip(),
                        "last_name": last.strip(),
                        "email": email.strip(),
                        "phone": phone.strip(),
                        "experience": experience,
                        "location": location.strip(),
                        "desired_position": position.strip(),
                        "tech_stack": [t.strip() for t in tech.split(",") if t.strip()],
                        "additional_notes": notes,
                        "submission_time": datetime.now().isoformat()
                    }
                    
                    # Store both original and anonymized versions
                    st.session_state.form_data = form_data
                    st.session_state.anonymized_data = anonymize_data(form_data)
                    st.session_state.form_done = True
                    
                    st.success("✅ Application submitted successfully!")
                   
                    
                    # Log the action
                    st.session_state.conversation_history.append({
                        "timestamp": datetime.now(),
                        "action": "Form submitted",
                        "data": st.session_state.anonymized_data
                    })
                    
                    time.sleep(2)
                    st.rerun()
        return
    
    # 3. Technical Interview Phase
    if not st.session_state.questions:
        with st.spinner("🔄 Preparing technical questions based on your skills..."):
            st.session_state.questions = gen_questions(st.session_state.form_data["tech_stack"])
            st.session_state.q_index = 0
            st.session_state.score = 0
            st.session_state.mark_list = []
            st.session_state.detailed_feedback = []
    
    # Calculate total questions
    total_q = sum(len(q["questions"]) for q in st.session_state.questions)
    
    # Check if interview is complete
    if st.session_state.q_index >= total_q or st.session_state.interview_complete:
        st.markdown("## 🎯 Interview Complete!")
        
        # Calculate final score percentage
        score_percentage = (st.session_state.score / total_q * 100) if total_q > 0 else 0
        
        # Display score with visual feedback
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
            <div class='score-display'>
                Your Score: {st.session_state.score}/{total_q}
                <br>
                ({score_percentage:.1f}%)
            </div>
            """, unsafe_allow_html=True)
            
            # Performance feedback
            if score_percentage >= 80:
                st.success("🌟 Excellent performance! You've demonstrated strong technical knowledge.")
            elif score_percentage >= 60:
                st.info("👍 Good job! You show solid understanding of the technologies.")
            elif score_percentage >= 40:
                st.warning("📚 Fair performance. Consider strengthening some technical areas.")
            else:
                st.error("💪 Keep learning! There's room for improvement in your technical skills.")
        
        # Show detailed feedback
        if st.session_state.detailed_feedback:
            with st.expander("📊 Detailed Feedback"):
                for feedback in st.session_state.detailed_feedback:
                    st.write(f"**{feedback['technology']} - Question {feedback['question_num']}:**")
                    st.write(f"*{feedback['question']}*")
                    st.write(f"Your answer: {feedback['answer'][:100]}...")
                    st.write(f"Feedback: {feedback['feedback']}")
                    st.write("---")
        
        # Next steps
        st.markdown("""
        ### 📬 Next Steps
        
        Thank you for completing the technical assessment! Here's what happens next:
        
        1. **Review Process**: Our recruitment team will review your application within 2-3 business days
        2. **Follow-up**: If selected, you'll receive an email for the next round of interviews
        3. **Feedback**: We'll provide feedback on your technical assessment regardless of the outcome
        
        **Thank you for your interest in joining our team!** 🚀
        """)
        
        # Save conversation history
        st.session_state.conversation_history.append({
            "timestamp": datetime.now(),
            "action": "Interview completed",
            "score": f"{st.session_state.score}/{total_q}",
            "percentage": score_percentage
        })
        
        
        
        return
    
    # Display current question
    cumulative = 0
    current_tech = None
    current_question = None
    question_index_in_tech = 0
    
    for tech_item in st.session_state.questions:
        tech_questions = tech_item["questions"]
        if st.session_state.q_index < cumulative + len(tech_questions):
            current_tech = tech_item["technology"]
            question_index_in_tech = st.session_state.q_index - cumulative
            current_question = tech_questions[question_index_in_tech]
            break
        cumulative += len(tech_questions)
    
    # Question display
    st.markdown(f"""
    <div class='question-card' style="color: black; ">
        <h3>💻 {current_tech} - Question {question_index_in_tech + 1}</h3>
        <p style='font-size: 1.1rem; margin-top: 1rem;'>{current_question}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Answer input with character count
    answer = st.text_area(
        "Your Answer", 
        key=f"ans_{st.session_state.q_index}",
        height=150,
        placeholder="Type your answer here... (Minimum 10 words recommended)"
    )
    
    # Display character/word count
    if answer:
        word_count = len(answer.split())
        char_count = len(answer)
        st.caption(f"Words: {word_count} | Characters: {char_count}")
    
    # Question navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        submitted = st.button("Submit Answer", use_container_width=True)
    
    with col3:
        skip = st.button("Skip Question", use_container_width=True)
    
    if submitted and answer:
        # Check for exit intent
        if check_exit_intent(answer):
            st.warning("👋 Are you sure you want to end the interview?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Yes, end interview"):
                    st.session_state.interview_complete = True
                    st.rerun()
            with col2:
                if st.button("No, continue"):
                    st.rerun()
            return
        
        # Check for off-topic input
        is_off_topic, redirect_msg = handle_unexpected_input(answer)
        if is_off_topic:
            st.warning(redirect_msg)
            return
        
        # Evaluate answer
        is_correct, feedback ,score = evaluate_answer(current_question, answer, current_tech)
        
        # Store detailed feedback
        st.session_state.detailed_feedback.append({
            "technology": current_tech,
            "question_num": question_index_in_tech + 1,
            "question": current_question,
            "answer": answer,
            "feedback": feedback,
            "correct": is_correct,
            "score":score
        })
        
        if is_correct:
            st.success(f"✅ {feedback}")
            st.session_state.score += 1
            st.session_state.mark_list.append(1)
        else:
            st.warning(f"⚠️ {feedback}")
            st.session_state.mark_list.append(0)
        
        # Move to next question
        st.session_state.q_index += 1
        time.sleep(1.5)
        st.rerun()
    
    elif skip:
        st.info("Question skipped. Moving to next question...")
        st.session_state.mark_list.append(0)
        st.session_state.detailed_feedback.append({
            "technology": current_tech,
            "question_num": question_index_in_tech + 1,
            "question": current_question,
            "answer": "Skipped",
            "feedback": "Question was skipped",
            "correct": False
        })
        st.session_state.q_index += 1
        time.sleep(1)
        st.rerun()
    
    elif submitted and not answer:
        st.error("Please provide an answer before submitting.")
    
    # Progress indicator
    st.markdown("---")
    progress_text = f"Question {st.session_state.q_index + 1} of {total_q}"
    st.progress((st.session_state.q_index + 1) / total_q)
    st.caption(progress_text)

if __name__ == "__main__":
    main()