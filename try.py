# import streamlit as st
# import re

# # Validation patterns
# VALIDATION_PATTERNS = {
#     'email':      r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',
#     'phone':      r'^[\+]?[0-9]{10,15}$',
#     'first': r'^[A-Za-z]{1,50}$',
#     'last':  r'^[A-Za-z]{0,50}$',
#     'experience': r'^\d+(\.\d+)?$',
#     'location':   r'^[A-Za-z\s,.-]{1,100}$'
# }

# def validate_input(input_type, value):
#     """Validate input based on type"""
#     if not value or value.strip() == "":
#         return False, "This field is required."
    
#     pattern = VALIDATION_PATTERNS.get(input_type)
#     if pattern and not re.fullmatch(pattern, value.strip()):
#         if input_type == 'email':
#             return False, "Please enter a valid email address."
#         elif input_type == 'phone':
#             return False, "Please enter a valid phone number (10-15 digits)."
#         elif input_type == 'first':
#             return False, "Please enter your first name."
#         elif input_type == 'last':
#             return False, "Please enter your last name."
#         elif input_type == 'experience':
#             return False, "Please enter a valid number of years."
#         elif input_type == 'location':
#             return False, "Please enter a valid location."
    
#     return True, ""

# # Initialize session state for form data
# if 'form_data' not in st.session_state:
#     st.session_state.form_data = {}

# # Main form
# st.title("🤖 TalentScout - Candidate Registration")

# with st.form("candidate_form", clear_on_submit=False):
#     st.header("📝 Personal Information")
    
#     # Create two columns for better layout
#     col1, col2 = st.columns(2)
    
#     with col1:
#         first = st.text_input(
#             "First Name *", 
#             placeholder="Enter your first name",
#             help="Please provide your first name"
#         )
        
#         email = st.text_input(
#             "Email Address *", 
#             placeholder="your.email@example.com",
#             help="We'll use this to contact you"
#         )
        
#         phone = st.text_input(
#             "Phone Number *", 
#             placeholder="+1234567890",
#             help="Include country code if international"
#         )
#         desired_position  = st.text_input(
#             "Position applying for *", 
#             placeholder="",
#             help="Select your preferred role"
#         )
#     with col2:
#         last = st.text_input(
#             "Last Name *", 
#             placeholder="Enter your last name",
#             help="Please provide your last name"
#         )
#         experience = st.number_input(
#             "Years of Experience *", 
#             min_value=0.0, 
#             max_value=50.0, 
#             step=0.5,
#             format="%.1f"
#         )
        
#         location = st.text_input(
#             "Enter your location *",
#             placeholder="City, State/Country",
#             help="Where are you currently based?"
#         )
        
        
         
#     st.header("💻 Technical Skills")
    
#     # Tech stack input
#     tech_stack = st.text_area(
#         "Tech Stack *",
#         placeholder="Python, Django, React, PostgreSQL, Docker, AWS...",
#         help="List your technical skills separated by commas",
#         height=100
#     )
    
#     # Additional information
#     st.header("📋 Additional Information")
    
    
#     additional_notes = st.text_area(
#         "Additional Notes (Optional)",
#         placeholder="Any additional information you'd like to share...",
#         height=80
#     )
    
#     # Submit button
#     submitted = st.form_submit_button("🚀 Submit Application", type="primary")
    
#     # Form validation and processing
#     # Form validation…
#     if submitted:
#         errors = []    

#         # First Name
#         valid, msg = validate_input('first', first)
#         if not valid:
#             errors.append(msg)    

#         # Last Name
#         valid, msg = validate_input('last', last)
#         if not valid:
#             errors.append(msg)    

#         # Email Address
#         if not email:
#             errors.append("Email Address is required.")
#         else:
#             valid, msg = validate_input('email', email)
#             if not valid:
#                 errors.append(msg)    

#         # Phone Number
#         if not phone:
#             errors.append("Phone Number is required.")
#         else:
#             valid, msg = validate_input('phone', phone)
#             if not valid:
#                 errors.append(msg)    

#         # Location
#         valid, msg = validate_input('location', location)
#         if not valid:
#             errors.append(msg)    

#         # Desired Position
#         if not desired_position:
#             errors.append("Desired Position is required.")    

#         # Tech Stack
#         if not tech_stack:
#             errors.append("Tech Stack is required.")    

#         # Display errors or process form
#         if errors:
#             st.error("Please fix the following errors:")
#             for err in errors:
#                 st.write(f"• {err}")
#         else:
#             st.success("✅ Application submitted successfully!")
#             # …store and display data…    

            
#             # Display submitted data
#             st.subheader("📊 Your Submitted Information:")
            
#             col1, col2 = st.columns(2)
#             with col1:
#                 st.write(f"**Name:** {first } { last}")
#                 st.write(f"**Email:** {email}")
#                 st.write(f"**Experience:** {experience} years")
            
#             with col2:
#                 st.write(f"**Location:** {location}")
#                 st.write(f"**Phone:** {phone}")
#                 st.write(f"**Position:** {desired_position}")
            
#             st.write(f"**Tech Stack:** {tech_stack}")
#             if additional_notes:
#                 st.write(f"**Notes:** {additional_notes}")

# # Display stored data (if any)
# if st.session_state.form_data:
#     with st.expander("View Previously Submitted Data"):
#         st.json(st.session_state.form_data)
#































#  import streamlit as st
# import groq
# import re
# import json
# import os
# from datetime import datetime
# from dotenv import load_dotenv
# import pandas as pd
# from groq import Groq

# # Load environment variables
# load_dotenv()
# api_key = os.getenv("GROQ_API_KEY")
# try:
#     client = Groq(api_key=api_key)
# except Exception as e:
#     st.error(f"❌ Failed to initialize Groq client: {str(e)}")
#     client = None

# # Page configuration
# st.set_page_config(
#     page_title="TalentScout Hiring Assistant",
#     page_icon="🤖",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS for beautiful UI
# st.markdown("""
# <style>
#     .main-header {
#         background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
#         padding: 2rem;
#         border-radius: 10px;
#         color: white;
#         text-align: center;
#         margin-bottom: 2rem;
#     }
    
#     .chat-message {
#         padding: 1rem;
#         border-radius: 10px;
#         margin: 0.5rem 0;
#         border-left: 4px solid;
#     }
    
#     .user-message {
#         background-color: #e3f2fd;
#         border-left-color: #2196f3;
#         margin-left: 2rem;
#     }
    
#     .assistant-message {
#         background-color: #f3e5f5;
#         border-left-color: #9c27b0;
#         margin-right: 2rem;
#     }
    
#     .sidebar-info {
#         background-color: #f8f9fa;
#         padding: 1rem;
#         border-radius: 8px;
#         margin: 0.5rem 0;
#         border-left: 3px solid #007bff;
#         color: black;
#     }
    
#     .tech-stack-item {
#         background-color: #e8f5e8;
#         padding: 0.5rem;
#         border-radius: 5px;
#         margin: 0.25rem 0;
#         border-left: 3px solid #28a745;
#         color: black;
#     }
    
#     .stTextInput > div > div > input {
#         background-color: #ffffff;
#         border: 2px solid #e0e0e0;
#         border-radius: 8px;
#         padding: 0.75rem;
#     }
    
#     .stTextInput > div > div > input:focus {
#         border-color: #667eea;
#         box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
#     }
    
#     .stButton > button {
#         background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
#         color: white;
#         border: none;
#         border-radius: 8px;
#         padding: 0.75rem 1.5rem;
#         font-weight: bold;
#         transition: all 0.3s ease;
#     }
    
#     .stButton > button:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 4px 8px rgba(0,0,0,0.2);
#     }
    
#     .progress-container {
#         background-color: #f8f9fa;
#         border-radius: 10px;
#         padding: 1rem;
#         margin: 1rem 0;
#     }
    
#     .spinner-container {
#         display: flex;
#         justify-content: center;
#         align-items: center;
#         padding: 2rem;
#     }
# </style>
# """, unsafe_allow_html=True)


# # Validation patterns and function
# VALIDATION_PATTERNS = {
#     'email':      r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',
#     'phone':      r'^[\+]?[0-9]{10,15}$',
#     'first':      r'^[A-Za-z]{1,50}$',
#     'last':       r'^[A-Za-z]{0,50}$',
#     'experience': r'^\d+(\.\d+)?$',
#     'location':   r'^[A-Za-z\s,.-]{1,100}$'
# }

# def validate_input(input_type, value):
#     """Validate input based on type"""
#     if not value or value.strip() == "":
#         return False, "This field is required."
    
#     pattern = VALIDATION_PATTERNS.get(input_type)
#     if pattern and not re.fullmatch(pattern, value.strip()):
#         error_messages = {
#             'email': "Please enter a valid email address.",
#             'phone': "Please enter a valid phone number (10-15 digits).",
#             'first': "Please enter your first name (letters only).",
#             'last': "Please enter your last name (letters only).",
#             'experience': "Please enter a valid number of years.",
#             'location': "Please enter a valid location."
#         }
#         return False, error_messages.get(input_type, "Invalid input.")
#     return True, ""

# # Initialize session states
# if 'form_submitted' not in st.session_state:
#     st.session_state.form_submitted = False
# if 'form_data' not in st.session_state:
#     st.session_state.form_data = {}
# if 'greeted' not in st.session_state:
#     st.session_state.greeted = False


# def call_groq_llm(prompt, system_prompt=""):
#     """Call Groq LLM with spinner"""
#     with st.spinner("🤖 AI is thinking..."):
#         if client is None:
#             # Demo mode fallback
#             if "greeting" in prompt.lower():
#                 return "Hello! I'm TalentScout, your AI-powered hiring assistant. I'm here to help gather your information and assess your technical skills for potential opportunities. Let's get started!"
#             elif "technical questions" in prompt.lower():
#                 return "I'll generate some technical questions for you based on your skills."
#             elif "follow up" in prompt.lower() or "context" in prompt.lower():
#                 return "Thank you for your response! I'm here to help guide you through the hiring process."
#             else:
#                 return "Thank you for your response! I'm here to help guide you through the hiring process."

#         try:
#             messages = []
#             if system_prompt:
#                 messages.append({"role": "system", "content": system_prompt})
#             messages.append({"role": "user", "content": prompt})
#             response = client.chat.completions.create(
#                 model="openai/gpt-oss-20b",
#                 messages=messages,
#                 temperature=0.7,
#                 max_tokens=1000
#             )
#             return response.choices[0].message.content.strip()
#         except Exception as e:
#             st.warning(f"⚠️ LLM API Error: {str(e)}")
#             # Fallback responses
#             if "greeting" in prompt.lower():
#                 return "Hello! I'm TalentScout, your AI-powered hiring assistant. I'm here to help gather your information and assess your technical skills for potential opportunities. Let's get started!"
#             elif "technical questions" in prompt.lower():
#                 return "I'll generate some technical questions for you based on your skills."
#             elif "follow up" in prompt.lower() or "context" in prompt.lower():
#                 return "Thank you for your response! I'm here to help guide you through the hiring process."
#             else:
#                 return "Thank you for your response! I'm here to help guide you through the hiring process."

# def generate_greeting():
#     system_prompt = """You are TalentScout, an intelligent hiring assistant for a technology recruitment agency. 
#     You should be professional, friendly, and helpful. Keep responses concise and engaging."""
#     prompt = """Generate a warm, professional greeting for a candidate visiting our hiring assistant. 
#     Introduce yourself as TalentScout and explain that you'll help gather their information and assess their technical skills. 
#     Keep it under 100 words and make it welcoming."""
#     return call_groq_llm(prompt, system_prompt)


# def display_sidebar():
#     """Display user information in sidebar"""
#     st.sidebar.markdown("## 👤 Candidate Information")
#     if st.session_state.form_data:
#         for key, value in st.session_state.form_data.items():
#             if value:
#                 st.sidebar.markdown(f"""
#                 <div class="sidebar-info">
#                     <strong>{key.replace('_', ' ').title()}:</strong><br>
#                     {value}
#                 </div>
#                 """, unsafe_allow_html=True)

#     tech_stack = st.session_state.form_data.get('tech_stack', [])
#     if tech_stack:
#         st.sidebar.markdown("## 🛠️ Tech Stack")
#         for tech in tech_stack:
#             st.sidebar.markdown(f"""
#             <div class="tech-stack-item">
#                 {tech}
#             </div>
#             """, unsafe_allow_html=True)
    
#     # Progress indicator
#     phases = ['greeting', 'form', 'technical_questions', 'conclusion']
#     if st.session_state.form_submitted:
#         current_phase_index = phases.index('conclusion')
#     elif st.session_state.greeted:
#         current_phase_index = phases.index('form')
#     else:
#         current_phase_index = phases.index('greeting')
        
#     st.sidebar.markdown("## 📊 Progress")
#     progress = (current_phase_index + 1) / len(phases)
#     st.sidebar.progress(progress)
#     st.sidebar.markdown(f"**Phase:** {phases[current_phase_index].replace('_', ' ').title()}")


# def main():

#     st.markdown("""
#     <div class="main-header">
#         <h1>🤖 TalentScout Hiring Assistant</h1>
#         <p>Your AI-powered recruitment companion</p>
#     </div>
#     """, unsafe_allow_html=True)

#     display_sidebar()

#     # Step 1: Greeting (shown once)
#     if not st.session_state.greeted:
#         greeting = generate_greeting()
#         st.markdown(f"### {greeting}")
#         if st.button("Start Application"):
#             st.session_state.greeted = True
#             st.rerun()
#         return  # Do not show anything else until greeted

#     # Step 2: Candidate Form (show only if not yet submitted)
#     if not st.session_state.form_submitted:
#         with st.form("candidate_form", clear_on_submit=False):
#             st.header("📝 Personal Information")

#             col1, col2 = st.columns(2)
#             st.markdown("""
#                 <style>
#                 /* Change text color inside all text inputs */
#                 .stTextInput input {
#                     color: #1a73e8 !important;   /* Google blue */
                    
#                 }
#                 .stTextInput input::placeholder {
#                     color: #888 !important;   /* Gray placeholder */
#                     font-style: italic;
#                 </style>
#                 """, unsafe_allow_html=True)


#             with col1:
#                 first = st.text_input(
#                     "First Name *",
#                     placeholder="Enter your first name",
#                     help="Please provide your first name",
#                 )
#                 email = st.text_input(
#                     "Email Address *",
#                     placeholder="your.email@example.com",
#                     help="We'll use this to contact you",
#                 )
#                 phone = st.text_input(
#                     "Phone Number *",
#                     placeholder="+1234567890",
#                     help="Include country code if international",
#                 )
#                 desired_position = st.text_input(
#                     "Position applying for *",
#                     placeholder="",
#                     help="Select your preferred role",
#                 )

#             with col2:
#                 last = st.text_input(
#                     "Last Name *",
#                     placeholder="Enter your last name",
#                     help="Please provide your last name",
#                 )
#                 experience = st.number_input(
#                     "Years of Experience *",
#                     min_value=0.0,
#                     max_value=50.0,
#                     step=0.5,
#                     format="%.1f",
#                 )
#                 location = st.text_input(
#                     "Enter your location *",
#                     placeholder="City, State/Country",
#                     help="Where are you currently based?",
#                 )

#             st.header("💻 Technical Skills")

#             tech_stack = st.text_area(
#                 "Tech Stack *",
#                 placeholder="Python, Django, React, PostgreSQL, Docker, AWS...",
#                 help="List your technical skills separated by commas",
#                 height=100,
#             )

#             st.header("📋 Additional Information")

#             additional_notes = st.text_area(
#                 "Additional Notes (Optional)",
#                 placeholder="Any additional information you'd like to share...",
#                 height=80,
#             )

#             submitted = st.form_submit_button("🚀 Submit Application", type="primary")

#             if submitted:
#                 errors = []

#                 # Validate required fields
#                 for field_key, field_value in [
#                     ('first', first),
#                     ('last', last),
#                     ('email', email),
#                     ('phone', phone),
#                     ('experience', str(experience)),
#                     ('location', location),
#                 ]:
#                     valid, msg = validate_input(field_key, field_value)
#                     if not valid:
#                         errors.append(msg)

#                 if not desired_position:
#                     errors.append("Desired Position is required.")

#                 if not tech_stack:
#                     errors.append("Tech Stack is required.")

#                 if errors:
#                     st.error("Please fix the following errors:")
#                     for err in errors:
#                         st.write(f"• {err}")
#                 else:
#                     st.session_state.form_data = {
#                         'first_name': first,
#                         'last_name': last,
#                         'email': email,
#                         'phone': phone,
#                         'experience': experience,
#                         'location': location,
#                         'desired_position': desired_position,
#                         'tech_stack': [tech.strip() for tech in tech_stack.split(',')],
#                         'additional_notes': additional_notes,
#                     }
#                     st.session_state.form_submitted = True
#                     st.success("✅ Application submitted successfully!")
#                     st.rerun()
#         return

#     # Step 3: After form submission - show summary or next steps
    

#     if st.button("Restart Application"):
#         # Reset everything to start over
#         st.session_state.form_submitted = False
#         st.session_state.greeted = False
#         st.session_state.form_data = {}
#         st.rerun()


# if __name__ == "__main__":
#     main()













import streamlit as st
import groq
import re
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq

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
  /* (Your existing CSS here) */
</style>
""", unsafe_allow_html=True)

# ————————————————————————————————
# Validation patterns & helper
# ————————————————————————————————
VALIDATION_PATTERNS = {
    'email':      r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',
    'phone':      r'^[\+]?[0-9]{10,15}$',
    'first':      r'^[A-Za-z]{1,50}$',
    'last':       r'^[A-Za-z]{1,50}$',
    'experience': r'^\d+(\.\d+)?$',
    'location':   r'^[A-Za-z\s,.-]{1,100}$'
}

def validate(field, val):
    if not val or not val.strip():
        return False, "This field is required."
    pat = VALIDATION_PATTERNS.get(field)
    if pat and not re.fullmatch(pat, val.strip()):
        msgs = {
            'email':      "Please enter a valid email.",
            'phone':      "Please enter a valid phone number.",
            'first':      "First name must be letters only.",
            'last':       "Last name must be letters only.",
            'experience': "Enter a valid number of years.",
            'location':   "Enter a valid location."
        }
        return False, msgs.get(field, "Invalid input.")
    return True, ""

# ————————————————————————————————
# LLM helpers
# ————————————————————————————————
def call_groq(prompt, sys_prompt=""):
    with st.spinner("🤖 AI is thinking..."):
        if client is None:
            return "Hello! (demo mode response)"
        messages = []
        if sys_prompt:
            messages.append({"role":"system","content":sys_prompt})
        messages.append({"role":"user","content":prompt})
        resp = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        return resp.choices[0].message.content.strip()

def gen_questions(stack):
    sys_p = "You are an interviewer. Generate 3–5 technical questions for each tech."
    prompt = "Tech stack: " + ", ".join(stack) + "\n\nReturn JSON array of {technology, questions}."
    raw = call_groq(prompt, sys_p)
    print(raw)
    try:
        # Handle markdown code blocks
        json_start = raw.find('[')
        json_end = raw.rfind(']') + 1
        
        if json_start != -1 and json_end != -1:
            json_str = raw[json_start:json_end]
            return json.loads(json_str)
        else:
            raise ValueError("No JSON array found")
    except:
        # fallback simple
        return [{"technology":t,"questions":[f"What is {t}?",f"Explain a key concept in {t}.",f"Describe a challenge with {t}."]} for t in stack]

# ————————————————————————————————
# Session state initialization
# ————————————————————————————————
for k in ("greeted","form_done","questions","q_index","score","mark_list"):
    if k not in st.session_state:
        st.session_state[k] = False if k in ("greeted","form_done") else [] if k=="questions" else 0

# ————————————————————————————————
# Display sidebar
# ————————————————————————————————
def show_sidebar():
    st.sidebar.markdown("## 📊 Progress")
    steps = ["Greeting","Form","Interview","Conclusion"]
    idx = 0
    if st.session_state.form_done: idx = 2
    elif st.session_state.greeted: idx = 1
    st.sidebar.progress((idx+1)/len(steps))
    st.sidebar.markdown(f"**Step:** {steps[idx]}")

    data = st.session_state.get("form_data", {})
    if data:
        st.sidebar.markdown("## 👤 Candidate Info")
        for k,v in data.items():
            if k!="tech_stack":
                st.sidebar.write(f"**{k.replace('_',' ').title()}:** {v}")
        if data.get("tech_stack"):
            st.sidebar.markdown("## 🛠️ Tech Stack")
            for t in data["tech_stack"]:
                st.sidebar.write(f"- {t}")

# ————————————————————————————————
# Main application
# ————————————————————————————————
def main():
    st.markdown("<div class='main-header'><h1>🤖 TalentScout Hiring Assistant</h1></div>", unsafe_allow_html=True)
    show_sidebar()

    # 1. Greeting
    if not st.session_state.greeted:
        greeting = call_groq("greeting")
        st.markdown(f"### {greeting}")
        if st.button("Start Application"):
            st.session_state.greeted = True
            st.rerun()
        return

    # 2. Form
    if not st.session_state.form_done:
        with st.form("candidate_form", clear_on_submit=False):
            st.header("📝 Personal Information")
            c1,c2 = st.columns(2)
            with c1:
                first = st.text_input("First Name *")
                email = st.text_input("Email Address *")
                phone = st.text_input("Phone Number *")
                position = st.text_input("Desired Position *")
            with c2:
                last = st.text_input("Last Name *")
                experience = st.number_input("Years of Experience *",0.0,50.0,0.5)
                location = st.text_input("Location *")
            st.header("💻 Technical Skills")
            tech = st.text_area("Tech Stack * (comma-separated)")
            st.header("📋 Additional Notes")
            notes = st.text_area("Optional")
            submit = st.form_submit_button("Submit Application")
            if submit:
                errs = []
                for f,v in [("first",first),("last",last),("email",email),
                           ("phone",phone),("experience",str(experience)),
                           ("location",location)]:
                    ok,msg = validate(f,v)
                    if not ok: errs.append(msg)
                if not position: errs.append("Position is required.")
                if not tech.strip(): errs.append("Tech stack is required.")
                if errs:
                    st.error("Fix errors:")
                    for e in errs: st.write(f"• {e}")
                else:
                    st.session_state.form_data = {
                        "first_name":first, "last_name":last,
                        "email":email, "phone":phone,
                        "experience":experience,
                        "location":location,
                        "desired_position":position,
                        "tech_stack":[t.strip() for t in tech.split(",")],
                        "additional_notes":notes
                    }
                    st.session_state.form_done = True
                    st.success("✅ Application submitted!")
                    st.balloons()
                    st.rerun()
        return

    # 3. Interview questions
    if not st.session_state.questions:
        st.session_state.questions = gen_questions(st.session_state.form_data["tech_stack"])
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.session_state.mark_list = []

    # If all questions asked
    total_q = sum(len(q["questions"]) for q in st.session_state.questions)
    if st.session_state.q_index >= total_q:
        st.markdown("## Final Feedback")
        st.write(f"Your score: {st.session_state.score}/{total_q}")
        st.write("Thank you for your time! We will be in touch soon. 👋")
        return

    # Determine current tech & question
    cum = 0
    for item in st.session_state.questions:
        qs = item["questions"]
        if st.session_state.q_index < cum + len(qs):
            tech = item["technology"]
            qstr = qs[st.session_state.q_index - cum]
            break
        cum += len(qs)

    st.markdown(f"### {tech} Question:")
    st.write(qstr)
    answer = st.text_area("Your Answer", key=f"ans_{st.session_state.q_index}")
    if st.button("Submit Answer"):
        # Exit detection
        if any(w in answer.lower() for w in ["bye","exit","quit","end","stop","thank you","thanks"]):
            st.write("Thank you! Ending the interview. 👋")
            st.session_state.q_index = total_q  # force end
            st.rerun()
            return
        # Simple feedback (placeholder, could use LLM)
        good = len(answer.split()) >= 3  # naive check
        if good:
            st.success("Good answer! 👍")
            st.session_state.score += 1
            st.session_state.mark_list.append(1)
        else:
            st.warning("That could be more detailed. ⚠️")
            st.session_state.mark_list.append(0)
        st.session_state.q_index += 1
        st.rerun()

if __name__ == "__main__":
    main()
