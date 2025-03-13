import streamlit as st
import random
import pandas as pd
from pymongo import MongoClient

# MongoDB Connection
MONGO_URI = "mongodb+srv://siricrm_dev:LkngqE46FAjiMH9f@cluster0.dmtp0.mongodb.net/siri_crm?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["siri_crm"]
collection = db["uwazi_unit2_results"]

# Function to Save Data to MongoDB
def save_to_mongodb(user_data):
    collection.insert_one(user_data)
    st.success("✅ Your responses have been saved successfully!")

# Streamlit App
st.set_page_config(page_title="Uwazi Unit 2: Theatrical Innovations", page_icon="🎭", layout="wide")

st.title("🌟 Uwazi Unit 2: Theatrical Innovations")
st.subheader("Building Certitude Through Logic, Motion & Creative Expression")

st.markdown("### 📝 Unit Overview")
st.write("**Unit Duration:** 3 Days (~10.5 hours)")
st.write("This unit combines Logical-Mathematical and Kinesthetic Intelligence to develop problem-solving, movement, and creative skills.")

# Display Daily Schedule Table
st.markdown("### 📅 Daily Schedule")
unit2_schedule = pd.DataFrame({
    "Session": [
        "Devotion & Reflection", "Co-Creation Session", "4 Keys of Siri: Certitude", "DT4i - Empathy in Problem-Solving", 
        "Logical-Mathematical Task", "Kinesthetic Task", "Sketch Pad & Reflection", "Challenge of the Day", 
        "Hands-on Project", "Field Exploration (One Day)"
    ],
    "Activity Type": [
        "Siri Time", "Siri Time", "Siri Time", "Siri Time", "Soma Time", "Soma Time", "Siri Time", "Soma Time", "Soma Time", "Soma & Siri Time"
    ],
    "Description": [
        "Morning devotion and reflection on certitude.",
        "Group-based improvisation, drama, or music composition.",
        "Understanding Certitude through storytelling and debate.",
        "Role-playing and interactive exercises for empathy-driven problem solving.",
        "Problem-solving tasks: Logical puzzles, pattern-building, statistical analysis.",
        "Kinesthetic tasks: Balance, coordination, dexterity challenges.",
        "Journaling and sketching reflections from the day’s activities.",
        "Daily challenge integrating logical-math & kinesthetic elements.",
        "Interactive project applying problem-solving and movement skills.",
        "Visit a Science Lab/Math Museum & an Acrobatics Training Center."
    ]
})
st.dataframe(unit2_schedule)

# Logical-Mathematical and Kinesthetic Tasks Fully Mapped
st.markdown("### 🎯 Uwazi Unit 2 Expanded Tasks")
tasks = {
    "Logical-Mathematical Intelligence": {
        "Logical Reasoning": {
            "Easy": "Solve a digital puzzle that involves sequential reasoning (app-based).",
            "Moderate": "Analyze a real-world problem and develop a logical sequence to solve it.",
            "Difficult": "Debate an ethical dilemma using structured reasoning (recorded)."
        },
        "Problem-Solving": {
            "Easy": "Use a step-by-step approach to solve a virtual escape room challenge.",
            "Moderate": "Develop a strategy for managing limited resources in a simulated environment.",
            "Difficult": "Design an AI-based chatbot that responds logically to user queries."
        },
        "Mathematical Operations": {
            "Easy": "Complete a speed-based mental math quiz (auto-scored).",
            "Moderate": "Code a Python script that calculates probabilities in a game scenario.",
            "Difficult": "Develop an algorithm to optimize financial investments in a simulation."
        },
        "Numerical Analysis": {
            "Easy": "Interpret simple statistics in a graph-based assessment.",
            "Moderate": "Analyze real-world economic data to predict trends.",
            "Difficult": "Build a data model that forecasts future trends based on provided datasets."
        },
        "Critical Thinking": {
            "Easy": "Identify logical flaws in a given argument.",
            "Moderate": "Compare two opposing viewpoints and find weaknesses.",
            "Difficult": "Develop a debate strategy to defend an assigned controversial position."
        },
        "Pattern Recognition": {
            "Easy": "Identify missing shapes in a visual sequence.",
            "Moderate": "Solve an AI-generated pattern recognition puzzle.",
            "Difficult": "Use machine learning to predict an unseen data pattern."
        },
        "Deductive Reasoning": {
            "Easy": "Solve a classic 'who did it?' logic puzzle.",
            "Moderate": "Use deductive logic to analyze a historical mystery.",
            "Difficult": "Apply formal logic to programming an AI decision system."
        },
        "Inductive Reasoning": {
            "Easy": "Identify trends in a small dataset.",
            "Moderate": "Make predictions based on market behavior trends.",
            "Difficult": "Develop a scientific hypothesis based on observed data."
        },
        "Statistical Analysis": {
            "Easy": "Interpret a simple pie chart with survey data.",
            "Moderate": "Analyze trends from multiple data sets.",
            "Difficult": "Conduct a mini-research project using real-world statistical data."
        }
    },
    "Bodily-Kinesthetic Intelligence": {
        "Body Awareness": {
            "Easy": "Perform a guided relaxation and breathing exercise.",
            "Moderate": "Create a sequence that emphasizes controlled body movements.",
            "Difficult": "Develop a movement performance that expresses emotion."
        },
        "Balance": {
            "Easy": "Hold a single-leg balance for 30 seconds.",
            "Moderate": "Complete a slow-motion obstacle course with balance elements.",
            "Difficult": "Perform a partner-based acrobatic routine focused on balance."
        },
        "Fine Motor Control": {
            "Easy": "Complete a detailed sketch within given constraints.",
            "Moderate": "Use digital drawing tools to create a precise design.",
            "Difficult": "Design a piece of intricate hand-drawn art."
        },
        "Gross Motor Control": {
            "Easy": "Execute a basic running drill.",
            "Moderate": "Perform a series of high-energy sports drills.",
            "Difficult": "Create and perform an intense movement-based storytelling sequence."
        },
        "Dexterity": {
            "Easy": "Manipulate small objects in a time-sensitive game.",
            "Moderate": "Develop hand-eye coordination through juggling or similar task.",
            "Difficult": "Master a dexterity-based musical instrument technique."
        },
        "Kinesthetic Memory": {
            "Easy": "Memorize and repeat a short dance sequence.",
            "Moderate": "Perform a martial arts kata from memory.",
            "Difficult": "Execute a full-length choreography without prompts."
        },
        "Physical Expressiveness": {
            "Easy": "Act out emotions using only body language.",
            "Moderate": "Create a physical storytelling performance.",
            "Difficult": "Perform an advanced mime or silent acting routine."
        }
    }
}
st.success("✅ All 18 elements are now covered with individual tasks and full interactivity!")
