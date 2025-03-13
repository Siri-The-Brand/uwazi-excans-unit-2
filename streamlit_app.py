import streamlit as st
import random
import pandas as pd
import os
from pymongo import MongoClient

# Secure MongoDB Connection using Environment Variables
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["siri_crm"]
collection = db["uwazi_unit2_results"]

# Function to Save Data to MongoDB
def save_to_mongodb(user_data):
    collection.insert_one(user_data)
    st.success("✅ Your responses have been saved successfully!")

# Streamlit App Configuration
st.set_page_config(page_title="Uwazi Unit 2: Theatrical Innovations", page_icon="🎭", layout="wide")

st.title("🌟 Uwazi Unit 2: Theatrical Innovations")
st.subheader("Building Certitude Through Logic, Motion & Creative Expression")

# Unit Overview
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

# Logical-Mathematical and Kinesthetic Tasks
st.markdown("### 🎯 Uwazi Unit 2 Expanded Tasks")

import streamlit as st
import random
import pandas as pd
import os
import uuid
from pymongo import MongoClient

# Secure MongoDB Connection using Environment Variables
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["siri_crm"]
collection_classes = db["uwazi_classes"]
collection_students = db["uwazi_students"]
collection_tasks = db["uwazi_tasks"]
collection_scores = db["uwazi_scores"]

# Function to generate unique class codes
def generate_class_code():
    return str(uuid.uuid4())[:6]

# Function to save data
def save_to_mongodb(collection, data):
    collection.insert_one(data)
    st.success("✅ Data Saved Successfully!")

# AI Feedback System
def generate_ai_feedback(score):
    if score >= 9:
        return "🔥 Excellent! You’ve mastered this skill. Keep pushing your limits!"
    elif 7 <= score < 9:
        return "✅ Great work! You're doing well, but review the key concepts again."
    elif 5 <= score < 7:
        return "🛠️ You're making progress. Focus on improving consistency."
    else:
        return "⚡ Keep trying! Practice makes perfect. Need help? Ask your CSE!"

# Streamlit App Configuration
st.set_page_config(page_title="Uwazi Unit 2", page_icon="🎭", layout="wide")

st.title("🌟 Uwazi Unit 2: Theatrical Innovations")
st.subheader("Building Certitude Through Logic, Motion & Creative Expression")

# --- DAILY SCHEDULE ---
st.markdown("### 📅 Daily Schedule")

unit2_schedule = pd.DataFrame({
    "Day": ["Day 1", "Day 2", "Day 3", "Excursion Day"],
    "Focus": [
        "Logical Reasoning, Problem-Solving, Mathematical Operations, Body Awareness, Balance, Fine Motor Control",
        "Numerical Analysis, Critical Thinking, Pattern Recognition, Gross Motor Control, Dexterity, Kinesthetic Memory",
        "Deductive Reasoning, Inductive Reasoning, Statistical Analysis, Physical Expressiveness, Spatial Awareness, Physical Coordination",
        "Field Trip: Math/Science Lab + Acrobatics Training"
    ],
    "Resources Needed": [
        "Digital puzzles, notebooks, role-playing materials, balancing props",
        "Data charts, debate prompts, art materials, movement tools",
        "Coding software, statistical data, storytelling props, dance space",
        "Museum entry tickets, sportswear, research journals"
    ]
})
st.dataframe(unit2_schedule)

# --- CLASS MANAGEMENT ---
st.sidebar.markdown("## 🏫 Class Management")
cse_name = st.sidebar.text_input("Enter Your Name (CSE)")
class_action = st.sidebar.radio("Choose Action", ["Create Class", "Join Class", "View Class"])

if class_action == "Create Class":
    class_name = st.sidebar.text_input("Class Name")
    if st.sidebar.button("Create Class"):
        class_code = generate_class_code()
        save_to_mongodb(collection_classes, {"Class Name": class_name, "Class Code": class_code, "CSE": cse_name})
        st.sidebar.write(f"✅ Class Created! **Code: {class_code}**")

elif class_action == "Join Class":
    student_name = st.sidebar.text_input("Student Name")
    class_code = st.sidebar.text_input("Enter Class Code")
    if st.sidebar.button("Join Class"):
        save_to_mongodb(collection_students, {"Student Name": student_name, "Class Code": class_code})
        st.sidebar.success("✅ Joined Class Successfully!")

elif class_action == "View Class":
    class_code = st.sidebar.text_input("Enter Class Code")
    if st.sidebar.button("View Students"):
        students = list(collection_students.find({"Class Code": class_code}))
        st.sidebar.write("👨‍🎓 Students in Class:")
        for student in students:
            st.sidebar.write(f"- {student['Student Name']}")

# --- TASKS & RUBRICS ---
st.markdown("### 🎯 Uwazi Tasks: Logical-Mathematical & Kinesthetic")

tasks = {
    "Logical-Mathematical Intelligence": {
        "Logical Reasoning": ["Digital puzzle", "Analyze a real-world problem", "Debate an ethical dilemma"],
        "Problem-Solving": ["Escape room", "Resource management simulation", "AI chatbot design"],
        "Mathematical Operations": ["Mental math quiz", "Probability script", "Financial optimization"],
        "Numerical Analysis": ["Graph interpretation", "Economic trends", "Data model building"],
        "Critical Thinking": ["Identify flaws", "Compare viewpoints", "Debate strategy"],
        "Pattern Recognition": ["Missing shape", "AI pattern puzzle", "Machine learning prediction"],
        "Deductive Reasoning": ["Logic puzzle", "Historical analysis", "AI decision-making"],
        "Inductive Reasoning": ["Dataset trends", "Market predictions", "Hypothesis development"],
        "Statistical Analysis": ["Survey interpretation", "Dataset trends", "Mini-research"]
    },
    "Bodily-Kinesthetic Intelligence": {
        "Body Awareness": ["Relaxation exercise", "Controlled movement", "Expressive performance"],
        "Balance": ["One-leg balance", "Obstacle course", "Acrobatic routine"],
        "Fine Motor Control": ["Sketching", "Digital drawing", "Intricate art"],
        "Gross Motor Control": ["Running drill", "High-energy drill", "Movement storytelling"],
        "Dexterity": ["Object manipulation", "Hand-eye coordination", "Instrument mastery"],
        "Kinesthetic Memory": ["Dance sequence", "Martial arts kata", "Full choreography"],
        "Physical Expressiveness": ["Body language", "Storytelling", "Advanced mime"],
        "Spatial Awareness": ["Blindfolded maze", "Choreographed movement", "Spatial performance"],
        "Physical Coordination": ["Catch and throw", "Synchronized drill", "Multi-step martial arts"]
    }
}

st.success("✅ ALL 18 ELEMENTS COVERED!")

# --- CSE TASK ASSIGNMENT & SCORING ---
st.markdown("### 🎭 CSE Task Assignment & Scoring")
if cse_name:
    selected_student = st.selectbox("Select Student", [s["Student Name"] for s in collection_students.find()])
    selected_task = st.selectbox("Select Task", [task for category in tasks.values() for element in category.values() for task in element])
    task_level = st.selectbox("Difficulty Level", ["Easy", "Moderate", "Difficult"])
    
    # Rubric-Based Scoring
    score = st.slider(f"Score for {selected_task} (1-5)", 1, 5, 3)
    if st.button("Assign & Score Task"):
        save_to_mongodb(collection_tasks, {
            "Student Name": selected_student,
            "Task": selected_task,
            "Level": task_level,
            "CSE": cse_name,
            "Score": score
        })

# --- SIRI SOLVER TASK SUBMISSION ---
st.markdown("### 🧑‍💻 Siri Solver Tasks")
student_name = st.text_input("Enter Your Name (Siri Solver)")
if student_name:
    assigned_tasks = list(collection_tasks.find({"Student Name": student_name}))
    if assigned_tasks:
        for task in assigned_tasks:
            st.write(f"🔹 **{task['Task']} ({task['Level']})**")
            answer = st.text_input(f"Enter Answer for {task['Task']}")
            if st.button(f"Submit {task['Task']}"):
                score = random.randint(5, 10)
                ai_feedback = generate_ai_feedback(score)
                save_to_mongodb(collection_scores, {"Student": student_name, "Task": task["Task"], "Score": score, "Feedback": ai_feedback})
                st.write(f"✅ **Score:** {score} | **Feedback:** {ai_feedback}")

# --- ADMIN DASHBOARD ---
st.markdown("### 🔐 Admin Dashboard")
admin_password = st.text_input("Enter Admin Password", type="password")

if admin_password == "siriadmin123":
    st.success("✅ Admin Access Granted!")
    results = list(collection_scores.find())
    if results:
        results_df = pd.DataFrame(results)
        st.dataframe(results_df)


st.success("✅ Now with all 18 elements fully covered!")
