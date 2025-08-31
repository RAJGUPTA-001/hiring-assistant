






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

