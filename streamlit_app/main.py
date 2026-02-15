import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

QUERY_API_URL = f"{BACKEND_URL}/query"
ADD_DATA_API_URL = f"{BACKEND_URL}/add_data"


# Simulated admin credentials (for simplicity; use secure methods in production)
ADMIN_CREDENTIALS = {"username": "admin", "password": "admin123"}

# Manage session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Sidebar navigation
page = st.sidebar.selectbox("Navigation", ["Chatbot", "Admin"])

# Admin Login Page
def admin_login():
    st.title("Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == ADMIN_CREDENTIALS["username"] and password == ADMIN_CREDENTIALS["password"]:
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
            st.experimental_rerun()  # Redirect to admin page
        else:
            st.error("Invalid credentials.")

# Admin Page (File Upload)
def admin_page():
    st.title("Admin - Upload Files")
    st.write("Only admins can upload files to enhance the bot's knowledge base.")
    
    # File upload section
    uploaded_file = st.file_uploader("Choose a file (PDF, Text, Image)", type=["pdf", "txt", "jpg", "png"])
    if st.button("Upload"):
        if uploaded_file is not None:
            with st.spinner("Uploading file..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                    response = requests.post(ADD_DATA_API_URL, files=files)
                    if response.status_code == 200:
                        st.success(f"File '{uploaded_file.name}' uploaded successfully!")
                    else:
                        st.error(f"Failed to upload file: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"An error occurred while uploading the file: {e}")
        else:
            st.warning("Please select a file to upload.")

    # Logout button
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun()


# Chatbot Page
def chatbot_page():
    st.title("Chatbot")
    st.write("Ask your questions and get answers powered by RAG!")

    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Input box for user query
    user_query = st.text_input("Enter your question:")

    if st.button("Submit"):
        if user_query:
            # Add user query to chat history
            st.session_state.messages.append({"role": "user", "content": user_query})

            # Display spinner during API call
            with st.spinner("Fetching response..."):
                try:
                    response = requests.post(QUERY_API_URL, json={"query": user_query})
                    if response.status_code == 200:
                        bot_response = response.json().get("response", "Sorry, I couldn't generate a response.")
                    else:
                        bot_response = f"Error: {response.status_code} - {response.text}"
                except Exception as e:
                    bot_response = f"An error occurred: {e}"

            # Add bot response to chat history
            st.session_state.messages.append({"role": "bot", "content": bot_response})

    # Display chat history
    st.subheader("Chat History")
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.write(f"**You:** {msg['content']}")
        else:
            st.write(f"**Bot:** {msg['content']}")

# Main App Logic
if page == "Admin":
    if st.session_state.logged_in:
        admin_page()
    else:
        admin_login()
elif page == "Chatbot":
    chatbot_page()
