import streamlit as st
import numpy as np
import plotly.graph_objects as go
import random
import re
from datetime import datetime

# Page config
st.set_page_config(
    page_title="StudyMaster AI - Math & Physics Genius",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.stChatMessage {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 15px;
    padding: 15px;
    margin: 10px 0;
}
.math-equation {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    font-size: 1.2em;
}
.formula-box {
    background: #fff3cd;
    border-left: 4px solid #ffc107;
    padding: 12px;
    margin: 10px 0;
    border-radius: 5px;
}
</style>
""", unsafe_allow_html=True)

# Session state
if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "🎓 Welcome! Ask me any math or physics question!"}]
if 'points' not in st.session_state:
    st.session_state.points = 0

# AI Response Function
def get_response(question):
    q = question.lower()
    
    # Quadratic solver
    if "quadratic" in q or "solve" in q and "x²" in q:
        match = re.search(r'([\d\-]*)x²\s*([\+\-]\s*\d*)x\s*([\+\-]\s*\d*)', q.replace(' ', ''))
        if match:
            a = int(match.group(1)) if match.group(1) and match.group(1) not in ['', '+', '-'] else (1 if match.group(1) != '-' else -1)
            b = int(match.group(2).replace('+', '')) if match.group(2) else 0
            c = int(match.group(3).replace('+', '')) if match.group(3) else 0
            d = b**2 - 4*a*c
            if d >= 0:
                x1 = (-b + d**0.5)/(2*a)
                x2 = (-b - d**0.5)/(2*a)
                return f"**Solution:** x = {x1:.2f} or x = {x2:.2f}\n\n**Steps:**\n1. a={a}, b={b}, c={c}\n2. Discriminant = {d}\n3. x = [-{b} ± √{d}]/{2*a}"
        return "**Quadratic Formula:** x = [-b ± √(b² - 4ac)]/(2a)\n\nExample: x² + 5x + 6 = 0 → x = -2 or -3"
    
    # Derivatives
    elif "derivative" in q:
        return "**Derivative Power Rule:** d/dx[xⁿ] = n·xⁿ⁻¹\n\n**Example:** d/dx[x³] = 3x²\n\n**Common derivatives:**\n• sin(x) → cos(x)\n• cos(x) → -sin(x)\n• eˣ → eˣ"
    
    # Physics - Newton's Law
    elif "newton" in q or "force" in q:
        return "**Newton's Second Law:** F = ma\n\n**Example:** A 10kg mass at 2m/s² → F = 10 × 2 = 20N\n\n**Practice:** If F=50N and m=5kg, a = 10m/s²"
    
    # Physics - Kinematics
    elif "velocity" in q or "acceleration" in q:
        return "**Kinematics Equations:**\n• v = u + at\n• s = ut + ½at²\n• v² = u² + 2as\n\n**Example:** Car from rest, a=3m/s², t=5s → v = 15m/s"
    
    # Integrals
    elif "integral" in q or "integrate" in q:
        return "**Integration Power Rule:** ∫xⁿ dx = xⁿ⁺¹/(n+1) + C\n\n**Example:** ∫x² dx = x³/3 + C\n\n**Common integrals:**\n• ∫1/x dx = ln|x| + C\n• ∫eˣ dx = eˣ + C"
    
    # General
    else:
        return f"""**How to solve {question[:50]}...**

**Step-by-step method:**
1. Identify what's given and what's asked
2. Choose the right formula
3. Substitute values
4. Solve step by step
5. Check your answer

**💡 Need a specific problem?** Give me numbers and I'll solve it completely!"""

# Main UI
st.title("🎓 StudyMaster AI")
st.caption("Your personal Math & Physics tutor")

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/artificial-intelligence.png", width=80)
    st.metric("⭐ Your Points", st.session_state.points)
    if st.button("🎁 Daily Bonus"):
        st.session_state.points += 50
        st.success("+50 points!")
        st.rerun()
    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [st.session_state.messages[0]]
        st.rerun()

# Chat display
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask a math or physics question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Solving..."):
            response = get_response(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.session_state.points += 10