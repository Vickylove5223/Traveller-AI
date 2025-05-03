import streamlit as st
import google.generativeai as genai
import os

# Configure the API key
api_key = "AIzaSyD3t4FR9qI3h-7cAzmT89Ogo8z-kcYNEwY"  # Replace with your actual API key or use os.environ
genai.configure(api_key=api_key)

# Set page configuration
st.set_page_config(
    page_title="Traveller - Your AI Travel Assistant",
    page_icon="🌎",
    layout="wide"
)

# Application title and description
st.title("🌎 Traveller - Your AI Travel Assistant")
st.markdown("""
Get personalized travel recommendations, itineraries, and answers to all your travel questions!
""")

# Initialize Gemini model
def get_gemini_response(question):
    try:
        # Make sure you're using the correct model name
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Prepare the conversation with travel focus
        travel_prompt = """
        You are an AI travel assistant for Traveller, a premium travel company. 
        Provide helpful, accurate, and engaging information about travel destinations, 
        itineraries, travel tips, local customs, and recommendations. 
        Always be polite, enthusiastic about travel, and provide specific details.
        """
        
        # Create a structured conversation
        response = model.generate_content([
            {"role": "user", "parts": [travel_prompt]},
            {"role": "model", "parts": ["I understand. I'll be your travel assistant providing helpful travel information."]},
            {"role": "user", "parts": [question]}
        ])
        
        return response.text
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Ask me anything about travel...")
if prompt:
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_gemini_response(prompt)
            st.markdown(response)
    
    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar with company info and travel categories
with st.sidebar:
    st.image("traveller.png", caption="Traveller", width=48)
    st.header("About Traveller")
    st.write("""
    Traveller is your premium travel planning partner. 
    We help you discover amazing destinations and create unforgettable experiences.
    """)

    
    # Add some travel categories
    st.subheader("Travel Plans")
    categories = ["Beach Getaways", "Mountain Adventures", "Cultural Experiences", 
                 "Family Trips", "Luxury Travel", "Budget Travel"]
    
    for category in categories:
        st.write(f"• {category}")

# Add a footer
st.markdown("---")
st.markdown("© 2025 Traveller - Your premium travel planning partner.")