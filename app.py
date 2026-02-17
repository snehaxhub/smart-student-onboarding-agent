import streamlit as st
import time

# Basic Page Config
st.set_page_config(page_title="UMIT App", layout="wide")

# --- 1. INITIALIZE SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "Login"

# --- 2. CONDITIONAL NAVIGATION (Only show if logged in) ---
if st.session_state['logged_in']:
    st.sidebar.title("UMIT Navigation")
    
    page_options = ["Dashboard" , "AI Assistant"]
    
    # Ensure the sidebar index stays synced if we redirect manually
    try:
        current_index = page_options.index(st.session_state['current_page'])
    except ValueError:
        current_index = 0

    selected_page = st.sidebar.selectbox("Go to", page_options, index=current_index)

    # If the user clicks a different page in the sidebar, update state
    if selected_page != st.session_state['current_page']:
        st.session_state['current_page'] = selected_page
        st.rerun()

    st.sidebar.divider()
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['current_page'] = "Login"
        st.rerun()

# --- 3. PAGE LOGIC ---

# LOGIN PAGE (No sidebar visible here)
if not st.session_state['logged_in']:
    # Centering the login form slightly
    _, col_mid, _ = st.columns([1, 2, 1])
    
    with col_mid:
        st.title("UMIT Student Login")
        st.write("Please enter your credentials to access the portal.")
        
        app_id = st.text_input("Application ID")
        password = st.text_input("Password", type="password")
        
        if st.button("Login", use_container_width=True):
            if app_id and password: 
                st.session_state['logged_in'] = True
                st.session_state['student_id'] = app_id
                st.session_state['current_page'] = "Dashboard"
                st.rerun()
            else:
                st.error("Invalid Application ID or Password")

# DASHBOARD PAGE
elif st.session_state['current_page'] == "Dashboard":
    st.header(f"Student Profile: {st.session_state.get('student_id', 'User')}")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"*Student Name:* Pranali Gosavi")
        st.write(f"*Branch:* Computer Science Technology")
    with col2:
        st.info("*Onboarding Stage:* Pending Verification")
    
    st.divider()
    st.subheader("Document Upload")
    uploaded_file = st.file_uploader("Upload Admission Receipt")
    if uploaded_file and st.button("Submit Document"):
        st.success("Document submitted!")

# --- AI ASSISTANT PAGE ---
if st.session_state['current_page'] == "AI Assistant":
    st.title("💬 UMIT Support")
    st.caption("How can we help you today? Select an option or type your query.")

    # 1. Initialize Messages
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! I'm your UMIT Assistant. What can I help you with?"}
        ]

    # 2. Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 3. SWIGGY-STYLE QUICK REPLIES
    # We only show buttons if the LAST message was from the assistant
    if st.session_state.messages[-1]["role"] == "assistant":
        st.write("---")
        cols = st.columns(4) # Create 4 slots for buttons
        
        options = {
            "💳 Fee Status": "Check my fee payment status",
            "📅 Timetable": "Show my class schedule",
            "📄 Documents": "Check document verification status",
            "🙋 Admin Help": "Connect me to an admin"
        }

        # Logic for when a button is clicked
        for i, (label, query) in enumerate(options.items()):
            if cols[i % 4].button(label, key=f"btn_{label}"):
                # Add the choice to chat as a User message
                st.session_state.messages.append({"role": "user", "content": query})
                st.rerun()

    # 4. CHAT INPUT (For manual typing)
    if prompt := st.chat_input("Type your message here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

    # 5. ASSISTANT LOGIC (Process the user's last message)
    if st.session_state.messages[-1]["role"] == "user":
        user_text = st.session_state.messages[-1]["content"].lower()
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                time.sleep(1) # Simulated delay
                
                if "fee" in user_text:
                    response = "Your Semester 4 fees are *PAID*. No dues found."
                elif "timetable" in user_text:
                    response = "The timetable for Computer Science & Technology is being updated."
                elif "document" in user_text:
                    response = "Your 'Admission Receipt' is currently *Pending Review* by the registrar."
                else:
                    response = "I've noted your query. An admin will get back to you shortly."
                
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()