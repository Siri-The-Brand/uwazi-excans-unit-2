import streamlit as st
import random
import pandas as pd
import os
import uuid
import time
from pymongo import MongoClient

# Secure MongoDB Connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["siri_crm"]

# MongoDB Collections
collection_classes = db["sl_uwazi_classes"]
collection_students = db["sl_uwazi_students"]
collection_tasks = db["sl_uwazi_tasks"]
collection_scores = db["sl_uwazi_scores"]
collection_files = db["sl_uwazi_files"]
collection_xp = db["sl_uwazi_xp"]  # ✅ XP & Umeme Points Collection

# Generate Unique Codes
def generate_code():
    return str(uuid.uuid4())[:6]

# Save to MongoDB with Error Handling
def save_to_mongodb(collection, data):
    try:
        collection.insert_one(data)
        st.success("✅ Data Saved Successfully!")
    except Exception as e:
        st.error(f"⚠️ Error Saving Data: {e}")

# AI Feedback System
def generate_ai_feedback(score):
    if score >= 9:
        return "🔥 Excellent! You’ve mastered this skill. Keep pushing your limits!"
    elif 7 <= score < 9:
        return "✅ Great work! Review key concepts again."
    elif 5 <= score < 7:
        return "🛠️ You're making progress. Focus on improving consistency."
    else:
        return "⚡ Keep trying! Need help? Ask your CSE!"

# XP & UMEME POINTS SYSTEM
def calculate_xp(task_level):
    return {"Easy": 10, "Moderate": 20, "Difficult": 30}.get(task_level, 0)

def calculate_umeme(task_level):
    return {"Easy": 5, "Moderate": 10, "Difficult": 15}.get(task_level, 0)

# Streamlit App Configuration
st.set_page_config(page_title="Uwazi Unit 2", page_icon="🎭", layout="wide")

st.title("🌟 Uwazi Unit 2: Theatrical Innovations")
st.subheader("Building Certitude Through Logic, Motion & Creative Expression")

# --- CLASS MANAGEMENT ---
st.sidebar.markdown("## 🏫 Class Management")
cse_name = st.sidebar.text_input("Enter Your Name (CSE)")
class_action = st.sidebar.radio("Choose Action", ["Create Class", "Join Class", "View Class"])

if class_action == "Create Class":
    class_name = st.sidebar.text_input("Class Name")
    if st.sidebar.button("Create Class"):
        class_code = generate_code()
        save_to_mongodb(collection_classes, {"Class Name": class_name, "Class Code": class_code, "CSE": cse_name})
        st.sidebar.write(f"✅ Class Created! **Code: {class_code}**")

elif class_action == "Join Class":
    student_name = st.sidebar.text_input("Student Name")
    class_code = st.sidebar.text_input("Enter Class Code")
    if st.sidebar.button("Join Class"):
        student_code = generate_code()
        save_to_mongodb(collection_students, {"Student Name": student_name, "Class Code": class_code, "Student Code": student_code})
        st.sidebar.success(f"✅ Joined Class Successfully! **Student Code: {student_code}**")

elif class_action == "View Class":
    class_code = st.sidebar.text_input("Enter Class Code")
    if st.sidebar.button("View Students"):
        students = list(collection_students.find({"Class Code": class_code}))
        if students:
            st.sidebar.write("👨‍🎓 Students in Class:")
            for student in students:
                st.sidebar.write(f"- {student['Student Name']}")
        else:
            st.sidebar.warning("🚨 No students found for this class!")

# --- TIME BLOCK SELECTION ---
st.markdown("## ⏳ Choose Learning Block")
time_block = st.radio("Select Time Block", ["Soma Time", "Siri Time", "Solver Time"])

# --- TASKS & LOGIC ---
task_categories = {
    "Soma Time": {
        "Logical Reasoning": "Solve a math puzzle using a step-by-step approach.",
        "Problem-Solving": "Use a simulation to solve a real-world challenge.",
        "Mathematical Operations": "Complete an AI-generated probability quiz.",
        "Numerical Analysis": "Analyze a dataset and predict future trends."
    },
    "Siri Time": {
        "Body Awareness": "Perform a guided relaxation & breathing exercise.",
        "Balance": "Hold a yoga pose for 30 seconds & log performance.",
        "Fine Motor Control": "Draw a pattern using an AI-generated prompt.",
        "Gross Motor Control": "Follow a workout routine & upload a performance video."
    },
    "Solver Time": {
        "Physical Expressiveness": "Act out an emotion using body language & record it.",
        "Spatial Awareness": "Solve a blindfolded navigation puzzle with a partner.",
        "Physical Coordination": "Perform a teamwork-based physical challenge."
    }
}

if time_block:
    selected_task_key = st.selectbox(f"Select {time_block} Task", list(task_categories[time_block].keys()))
    selected_task = task_categories[time_block][selected_task_key]
    task_level = st.selectbox("Select Difficulty", ["Easy", "Moderate", "Difficult"])

    if st.button("Start Task"):
        start_time = time.time()
        xp_earned = calculate_xp(task_level)
        umeme_earned = calculate_umeme(task_level)

        save_to_mongodb(collection_tasks, {
            "Student": student_name,
            "Task": selected_task,
            "Task Level": task_level,
            "Time Block": time_block,
            "Start Time": start_time,
            "XP Earned": xp_earned,
            "Umeme Points Earned": umeme_earned
        })

        st.success(f"🕒 Task '{selected_task}' started! (+{xp_earned} XP, +{umeme_earned} Umeme Points)")

# --- REAL-TIME PROGRESS UPDATE ---
st.markdown("### 📊 Live Progress Updates")
if student_name:
    student_progress = list(collection_tasks.find({"Student": student_name}))
    if student_progress:
        progress_df = pd.DataFrame(student_progress)
        st.dataframe(progress_df)
    else:
        st.warning("🚨 No tasks started yet!")

# --- ADMIN DASHBOARD ---
st.markdown("### 🔐 Admin Dashboard")
admin_password = st.text_input("Enter Admin Password", type="password")

if admin_password == "siriadmin123":
    st.success("✅ Admin Access Granted!")
    results = list(collection_scores.find())
    if results:
        results_df = pd.DataFrame(results)
        st.dataframe(results_df)
    else:
        st.warning("🚨 No student scores available!")

st.success("✅ Congrats! 🚀")
