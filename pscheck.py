import re
import random
import string
import streamlit as st

# Persistent Storage for Passwords
if 'password_diary' not in st.session_state:
    st.session_state['password_diary'] = {}

# Check Password Strength
def check_password_strength(password):
    score = 0
    feedback = []

    # Length Check
    if len(password) >= 8:
        score += 2
    else:
        feedback.append("Password should be at least 8 characters long.")

    # Alphabet Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1.5
    else:
        feedback.append("Password should have at least one uppercase and one lowercase letter.")

    # Number Check
    if re.search(r"[0-9]", password):
        score += 1.5
    else:
        feedback.append("Password should have at least one number.")

    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1.5
    else:
        feedback.append("Password should have at least one special character.")

    return score, feedback

# Generate Strong Password
def generate_strong_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(length))

# Blacklist Common Passwords
common_passwords = ["password", "123456", "admin", "password123", "12345678"]

# Save Password
def save_password(account, password):
    st.session_state['password_diary'][account] = password

# Streamlit UI
st.set_page_config(page_title="🔐 Password Strength Meter", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
        body {
            background-color: #f8f9fa;
            color: #212529;
            font-family: Arial, sans-serif;
        }
        .stTitle {
            color: #343a40;
            text-align: center;
        }
        .stButton > button {
            background: linear-gradient(90deg, #4CAF50, #2c9c43);
            color: white;
            border-radius: 20px;
            padding: 12px 20px;
        }
        .stButton > button:hover {
            transform: scale(1.05);
        }
        .stTextInput, .stTextArea {
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🔐 Password Strength Meter")

# Navigation
page = st.sidebar.radio("Navigation", ["Home", "📒 Password Diary"])

# Home Page
if page == "Home":
    account_name = st.text_input("🟦 Enter Account Name:")
    password = st.text_input("🔒 Enter your Password:", type="password")

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Check Strength"):
            if password.lower() in common_passwords:
                st.error("❌ This password is too common. Please choose a more secure one.")
            elif password:
                score, feedback = check_password_strength(password)
                if score >= 6:
                    st.success("✅ Strong Password!")
                elif score >= 4:
                    st.warning("⚠️ Moderate Password - Consider adding more security features.")
                else:
                    st.error("❌ Weak Password - Improve it using the suggestions below.")
                    for tip in feedback:
                        st.write("-", tip)
            else:
                st.warning("Please enter a password to check.")

    with col2:
        if st.button("Generate Strong Password"):
            strong_password = generate_strong_password()
            st.write("🔑 Suggested Password:", strong_password)

    if account_name and password and st.button("Save Password"):
        save_password(account_name, password)
        st.success(f"✅ Password for {account_name} saved successfully!")

# Password Diary Page
elif page == "📒 Password Diary":
    st.header("📒 Saved Passwords")
    if st.session_state['password_diary']:
        for account, saved_password in st.session_state['password_diary'].items():
            st.write(f"**{account}**: `{saved_password}`")
    else:
        st.info("No passwords saved yet.")










