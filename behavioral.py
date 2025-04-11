"""
Science Explorer Bot - A Streamlit app for elementary school science fair projects
Provides guided support for scientific exploration and project development.

Run `pip install streamlit agno` to install dependencies.
"""

import streamlit as st
import os
import datetime
from typing import List, Optional

from agno.agent import Agent
from agno.models.groq import Groq

# Set page configuration
st.set_page_config(
    page_title="Science Explorer Bot 🔬",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for kid-friendly aesthetics
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stApp {
        background-image: linear-gradient(to bottom right, #c9f5ff, #e8f8ff);
    }
    .css-18e3th9 {
        padding-top: 2rem;
    }
    .sidebar-content {
        padding: 1rem;
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 1rem;
        border: 3px solid #4dabf7;
    }
    h1, h2, h3 {
        color: #1e88e5;
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }
    .stButton button {
        background-color: #4dabf7;
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.8rem;
        transition: all 0.3s ease;
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }
    .stButton button:hover {
        background-color: #3a8bd8;
        transform: translateY(-2px);
    }
    .kid-mode {
        background-color: #ffeb3b;
        padding: 10px;
        border-radius: 10px;
        border: 3px dashed #ff9800;
        margin-bottom: 15px;
    }
    .parent-mode {
        background-color: #bbdefb;
        padding: 10px;
        border-radius: 10px;
        border: 3px dashed #1976d2;
        margin-bottom: 15px;
    }
    footer {
        font-size: 0.8rem;
        text-align: center;
        color: #666;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

class ScienceExplorerBot:
    def __init__(self, is_kid_mode=True):
        # Set mode (kid or parent)
        self.is_kid_mode = is_kid_mode
        
        # Initialize agent with Groq model and built-in memory
        self.agent = Agent(
            model=Groq(
                id="llama-3.1-8b-instant",
                api_key='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'
            ),
            description="An educational science guide for elementary school science fair projects.",
            instructions=self._get_instructions(),
            add_history_to_messages=True,
            markdown=True,  # Enable markdown formatting
        )
    
    def _get_instructions(self) -> List[str]:
        """Define the behavior and guardrails for the Science Explorer bot."""
        if self.is_kid_mode:
            return [
                "You are Professor Atom, a friendly and encouraging science explorer who helps elementary school kids (ages 6-10) with science fair projects for Hackett Elementary.",
                
                "COMMUNICATION STYLE:",
                "- Use simple, clear language appropriate for 3rd graders (8-9 year olds)",
                "- Be enthusiastic, encouraging, and playful with lots of fun emoji (🔬 🧪 🌈 🦄 🚀 🧠 💥)",
                "- Use short paragraphs and sentences",
                "- Ask lots of questions to guide children's thinking rather than giving answers",
                "- Express excitement about their ideas and discoveries",
                "- Make science sound fun and magical while still being accurate",
                "- Use examples that kids can relate to",
                "- Keep responses relatively brief (150-250 words maximum)",
                
                "CONTENT APPROACH:",
                "- NEVER give direct answers to science questions - instead ask guiding questions",
                "- Guide students through the scientific method: question, hypothesis, experiment, observation, conclusion",
                "- Suggest simple experiments with household materials",
                "- Emphasize safety at all times and mention parental supervision for any experiments",
                "- Focus on hands-on learning and observation skills",
                "- Use the Socratic method - ask questions that lead to discovery",
                "- Encourage critical thinking appropriate for elementary students",
                "- Relate scientific concepts to everyday experiences",
                "- Celebrate small discoveries and encourage persistence",
                
                "GUARDRAILS:",
                "- Keep all suggestions safe for elementary students",
                "- Avoid potentially dangerous experiments (chemicals, fire, electricity)",
                "- No suggestions that could damage household items or create big messes",
                "- Keep concepts at an elementary school level",
                "- Be mindful of limited attention spans",
                "- Always suggest parental supervision for any experiments",
                
                "Remember to be playful, use lots of emoji, and guide through questions rather than giving answers!"
            ]
        else:
            # Parent mode instructions
            return [
                "You are Dr. Morgan, a knowledgeable science education specialist helping parents support their elementary school children with science fair projects for Hackett Elementary.",
                
                "COMMUNICATION STYLE:",
                "- Use clear, direct language appropriate for parents",
                "- Include occasional emoji to keep tone friendly (🔬 📝 📊)",
                "- Be practical, organized, and strategic in your guidance",
                "- Provide more detailed explanations than you would for children",
                "- Balance enthusiasm with realistic expectations",
                "- Include specific, actionable advice",
                "- Keep responses moderate in length (250-400 words)",
                
                "CONTENT APPROACH:",
                "- Provide age-appropriate science fair project ideas",
                "- Explain how to guide children through the scientific method without doing the work for them",
                "- Offer strategies to support learning while encouraging independence",
                "- Suggest ways to manage time, materials, and expectations",
                "- Provide tips on presentation, documentation, and display creation",
                "- Include practical advice on how to handle common challenges",
                "- Include examples of questions parents can ask to stimulate thinking",
                "- Suggest how to talk about scientific concepts at an age-appropriate level",
                "- Focus on creating learning experiences rather than perfect projects",
                
                "GUARDRAILS:",
                "- Emphasize safety and supervision requirements",
                "- Suggest alternatives to potentially dangerous materials",
                "- Provide realistic time estimates for project completion",
                "- Don't suggest overly complex projects inappropriate for elementary students",
                "- Balance educational value with fun and engagement",
                "- Remind parents that the process is more important than the final product",
                "- Emphasize that parents should guide but not do the work",
                
                "Remember to provide practical support while encouraging the child's ownership of their project."
            ]
    
    def run(self, prompt: str):
        """Get a response from the agent using the run method."""
        return self.agent.run(prompt)
    
    def switch_mode(self):
        """Switch between kid and parent modes."""
        self.is_kid_mode = not self.is_kid_mode
        # Reinitialize the agent with new instructions
        self.agent = Agent(
            model=Groq(
                id="llama-3.1-8b-instant",
                api_key='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'
            ),
            description="An educational science guide for elementary school science fair projects.",
            instructions=self._get_instructions(),
            add_history_to_messages=True,
            markdown=True,
        )
        return self.is_kid_mode

def get_science_fair_suggestions(is_kid_mode):
    """Return a list of suggested science fair topics for quick prompts."""
    if is_kid_mode:
        return [
            "🌱 Plants and sunlight",
            "🧲 Magnets are cool!",
            "🌈 Rainbow colors",
            "🦋 Bug habitats",
            "💧 Water experiments",
            "🚗 Ramps and cars",
            "🍎 Food science",
            "🧼 Soap and bubbles",
            "🌪️ Weather fun",
            "🔋 Simple machines",
            "🦷 Tooth experiments",
            "🧠 Five senses"
        ]
    else:
        return [
            "📋 Science fair timeline",
            "📝 Project documentation",
            "🏆 Judging criteria",
            "🧪 Safe experiments",
            "📊 Data visualization",
            "📣 Presentation tips",
            "🛒 Budget-friendly ideas",
            "❓ Scientific method",
            "📚 Research sources",
            "🧮 Age-appropriate math",
            "🖼️ Display board tips",
            "📱 Technology integration"
        ]

def initialize_chat_history():
    """Initialize session state variables for chat history."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "suggestion_clicked" not in st.session_state:
        st.session_state.suggestion_clicked = None
    if "is_kid_mode" not in st.session_state:
        st.session_state.is_kid_mode = True

def main():
    # Initialize chat history and session state
    initialize_chat_history()
    
    # Initialize bot if not already done
    if 'bot' not in st.session_state:
        st.session_state.bot = ScienceExplorerBot(is_kid_mode=st.session_state.is_kid_mode)
    
    # App title and description
    if st.session_state.is_kid_mode:
        st.title("🔬 Science Explorer Bot for Kids! 🚀")
        st.markdown("""
        > Hey there, science explorer! I'm Professor Atom and I'm here to help you create an AMAZING science fair project! Let's discover cool stuff together! 🌈✨
        """)
        mode_container = st.empty()
        with mode_container.container():
            st.markdown("""
            <div class='kid-mode'>
            <h3>👦👧 KID MODE ACTIVE! 👦👧</h3>
            <p>I'll help you explore science and find a great project!</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.title("🔬 Science Fair Parent Support")
        st.markdown("""
        > Welcome to the parent guide for Hackett Elementary School science fair projects. This resource will help you support your child's learning journey while letting them take ownership of their project.
        """)
        mode_container = st.empty()
        with mode_container.container():
            st.markdown("""
            <div class='parent-mode'>
            <h3>👨‍👩‍👧‍👦 PARENT MODE ACTIVE 👨‍👩‍👧‍👦</h3>
            <p>Guidance for supporting your child's science fair journey.</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Sidebar with information and controls
    with st.sidebar:
        if st.session_state.is_kid_mode:
            st.image("https://img.icons8.com/cute-clipart/64/000000/test-tube.png", width=100)
        else:
            st.image("https://img.icons8.com/color/64/000000/microscope.png", width=100)
        
        st.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)
        
        # Mode switch
        st.subheader("👨‍👩‍👧‍👦 Choose Your Mode 👦👧")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Kid Mode" if not st.session_state.is_kid_mode else "✓ Kid Mode", 
                        disabled=st.session_state.is_kid_mode):
                st.session_state.is_kid_mode = True
                st.session_state.bot.switch_mode()
                st.rerun()
        with col2:
            if st.button("Parent Mode" if st.session_state.is_kid_mode else "✓ Parent Mode", 
                        disabled=not st.session_state.is_kid_mode):
                st.session_state.is_kid_mode = False
                st.session_state.bot.switch_mode()
                st.rerun()
        
        # Dynamic content based on mode
        if st.session_state.is_kid_mode:
            st.header("Meet Professor Atom! 🧪")
            st.markdown("""
            Hi there, young scientist! 👋
            
            I'm here to help you:
            - 🔎 Find a cool science question
            - 🤔 Make a guess (that's a hypothesis!)
            - 🧪 Test your ideas with experiments
            - 📝 Record what happens
            - 🎯 Figure out what it all means
            
            I won't give you the answers - that's YOUR job as a scientist! But I'll help you discover them yourself! 🚀
            """)
        else:
            st.header("Parent Resource Center 📚")
            st.markdown("""
            Welcome to the parent support section. Here you'll find:
            
            - 📅 Timeline management tips
            - 🧠 Age-appropriate guidance
            - 🔍 How to ask guiding questions
            - 📊 Documentation strategies
            - 🏆 Science fair preparation help
            
            Our goal is to help you support your child's learning journey while fostering independence and scientific thinking.
            """)
        
        # Session controls
        st.subheader("Session")
        if st.button("🔄 Start Over", key="new_session"):
            st.session_state.messages = []
            # Create a new agent instance to clear memory
            st.session_state.bot = ScienceExplorerBot(is_kid_mode=st.session_state.is_kid_mode)
            st.rerun()
        
        # Dynamic suggestions based on mode
        st.subheader("Need Ideas? Try These!")
        suggestions = get_science_fair_suggestions(st.session_state.is_kid_mode)
        for i in range(0, len(suggestions), 2):
            cols = st.columns(2)
            for j in range(2):
                if i + j < len(suggestions):
                    suggestion = suggestions[i + j]
                    if cols[j].button(suggestion, key=f"suggestion_{i+j}"):
                        st.session_state.suggestion_clicked = suggestion
                        st.rerun()
        
        # Scientific Method reminder
        if st.session_state.is_kid_mode:
            st.markdown("""
            ### 🔍 Scientific Method
            1. Ask a question ❓
            2. Make a guess (hypothesis) 🤔
            3. Test with an experiment 🧪
            4. Record what happens 📝
            5. Share what you learned! 🌟
            """)
        else:
            st.markdown("""
            ### 📋 Science Fair Checklist
            - Choose age-appropriate topic
            - Guide question formulation  
            - Help gather materials safely
            - Assist with documentation
            - Support independence
            - Practice presentation
            - Prepare display board
            """)
        
        st.markdown("""
        <footer>
            Hackett Elementary School Science Fair
        </footer>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Chat interface
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Handle suggestion clicks
    if st.session_state.suggestion_clicked is not None:
        suggestion = st.session_state.suggestion_clicked
        st.session_state.suggestion_clicked = None  # Reset after handling
        
        # Add user message to display
        with st.chat_message("user"):
            st.markdown(suggestion)
        st.session_state.messages.append({"role": "user", "content": suggestion})
        
        # Generate response with context
        with st.chat_message("assistant"):
            with st.spinner("Thinking of science ideas..." if st.session_state.is_kid_mode else "Researching educational approaches..."):
                response = st.session_state.bot.run(suggestion)
                st.markdown(response.content)
                
        # Add assistant response to UI history
        st.session_state.messages.append({"role": "assistant", "content": response.content})
    
    # If there are no messages yet, display a welcome message
    if not st.session_state.messages:
        with st.chat_message("assistant"):
            if st.session_state.is_kid_mode:
                welcome_message = """
                # Hello, future scientist! 👋🔬
                
                I'm **Professor Atom**, and I'm SUPER excited to help you with your Hackett Elementary Science Fair project! 🚀
                
                Science is like being a detective who solves nature's mysteries! ✨ We're going to:
                
                1. Ask awesome questions ❓
                2. Make cool guesses 🤔
                3. Test our ideas with experiments 🧪
                4. Write down what happens 📝
                5. Figure out what it all means! 🧠
                
                What kind of science stuff are you interested in? Plants? 🌱 Animals? 🐾 Weather? 🌦️ Space? 🪐 Tell me what you're curious about, and we'll start exploring together!
                
                Remember - real scientists don't know all the answers... they just know how to find them! 🔍
                """
            else:
                welcome_message = """
                # Welcome to the Science Fair Parent Support Center
                
                Thank you for helping your child navigate their science fair journey at Hackett Elementary. My name is Dr. Morgan, and I'm here to provide guidance that helps you support your young scientist while fostering their independence and critical thinking skills.
                
                The elementary school science fair is about:
                - Developing curiosity and scientific thinking 🧠
                - Learning the scientific method through hands-on experience 🔍
                - Building confidence in problem-solving abilities 💪
                - Creating documentation and presentation skills 📊
                
                What aspect of the science fair process would you like guidance on? Are you looking for project ideas, timeline planning, materials assistance, or strategies to support without taking over?
                """
            st.markdown(welcome_message)
            # Add this initial message to the history
            st.session_state.messages.append({"role": "assistant", "content": welcome_message})
            # Send to agent memory
            st.session_state.bot.run("Initialize conversation with appropriate welcome message")
    
    # Chat input
    if st.session_state.is_kid_mode:
        prompt = st.chat_input("What's your science question? 🔍")
    else:
        prompt = st.chat_input("How can I help with your child's science fair project?")
        
    if prompt:
        # Add user message to display
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Generate response with context
        with st.chat_message("assistant"):
            with st.spinner("Thinking of science ideas..." if st.session_state.is_kid_mode else "Researching educational approaches..."):
                response = st.session_state.bot.run(prompt)
                st.markdown(response.content)
                
        # Add assistant response to UI history
        st.session_state.messages.append({"role": "assistant", "content": response.content})
    
    st.markdown("---")
    if st.session_state.is_kid_mode:
        st.markdown(
            "*Where curious kids become awesome scientists!* 🔬✨"
        )
    else:
        st.markdown(
            "*Supporting the next generation of scientific thinkers* 🔬📚"
        )

if __name__ == "__main__":
    main()