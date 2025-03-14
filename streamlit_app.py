import streamlit as st
import pandas as pd
import time
import os
import uuid
from datetime import datetime
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
collection_xp = db["sl_uwazi_xp"]
collection_files = db["sl_uwazi_files"]

# Generate Unique Codes
def generate_code():
    return str(uuid.uuid4())[:6]

# Save to MongoDB
def save_to_mongodb(collection, data):
    try:
        collection.insert_one(data)
        st.success("✅ Data Saved Successfully!")
    except Exception as e:
        st.error(f"⚠️ Error Saving Data: {e}")

# XP & Umeme Points System
def calculate_xp(cse_rating):
    return {"Excellent": 30, "Great": 20, "Good": 15, "Needs Improvement": 5}.get(cse_rating, 0)

def calculate_umeme(start_time, end_time):
    time_taken = (end_time - start_time).total_seconds() / 60  # Time in minutes
    if time_taken <= 10:
        return 15
    elif time_taken <= 20:
        return 10
    else:
        return 5

# Streamlit App Configuration
st.set_page_config(page_title="Uwazi Unit 2", page_icon="🎭", layout="wide")
st.title("🌟 Uwazi Unit 2: Theatrical Innovations")
st.subheader("Building Certitude Through Logic, Motion & Creative Expression")

# Define Unit Schedule with 18 tasks properly structured
unit_schedule = pd.DataFrame({
    "Day": [
        "Day 1", "Day 1", "Day 1", "Day 1", "Day 1", "Day 1",
        "Day 2", "Day 2", "Day 2", "Day 2", "Day 2", "Day 2",
        "Day 3", "Day 3", "Day 3", "Day 3", "Day 3", "Day 3"
    ],
    "Time Block": [
        "Soma Time", "Siri Time", "Solver Time", "Soma Time", "Siri Time", "Solver Time",
        "Soma Time", "Siri Time", "Solver Time", "Soma Time", "Siri Time", "Solver Time",
        "Soma Time", "Siri Time", "Solver Time", "Soma Time", "Siri Time", "Solver Time"
    ],
    "Task": [
        "Logical Problem-Solving", "Creative Motion Expression", "Team Challenge",
        "Numerical Analysis", "Balance & Coordination", "Puzzle Deduction",
        "Inductive Reasoning", "Acrobatic Challenge", "Physical Coordination",
        "Pattern Recognition", "Statistical Analysis", "Critical Thinking",
        "Mathematical Operations", "Dexterity Challenge", "Strategic Thinking",
        "Abstract Reasoning", "Reflex & Speed Test", "Real-World Simulation"
    ]
})

# CSE View or Student View
role = st.radio("Select Your Role:", ["CSE (Coach)", "Siri Solver (Student)"])

if role == "CSE (Coach)":
    st.markdown("### 🏫 Class Management")
    cse_name = st.text_input("Enter Your Name (CSE)")
    day_selected = st.selectbox("Select Day", unit_schedule["Day"].unique())
    time_block_selected = st.selectbox("Select Time Block", unit_schedule["Time Block"].unique())
    task_selected = st.selectbox("Select Task", unit_schedule["Task"].unique())
    
    students = list(collection_students.find())
    student_names = [s["Student Name"] for s in students]
    selected_student = st.selectbox("Select Student", student_names)
    
    if st.button("Assign Task"):
        save_to_mongodb(collection_tasks, {
            "Student": selected_student,
            "Task": task_selected,
            "Day": day_selected,
            "Time Block": time_block_selected
        })
        st.success(f"✅ Task '{task_selected}' assigned to {selected_student}!")
    
    st.markdown("### 📊 Evaluate Student Performance")
    rating = st.selectbox("Select Rating", ["Excellent", "Great", "Good", "Needs Improvement"])
    xp_awarded = calculate_xp(rating)
    
    if st.button("Save Rating"):
        save_to_mongodb(collection_xp, {"Student": selected_student, "XP": xp_awarded, "Rating": rating})
        st.success(f"✅ Rating Saved! {selected_student} earned {xp_awarded} XP!")

elif role == "Siri Solver (Student)":
    st.markdown("### 📝 Join Class & Start Task")
    student_name = st.text_input("Enter Your Name (Siri Solver)")
    task = st.selectbox("Select Your Assigned Task", unit_schedule["Task"].unique())
    
    if st.button("Start Task"):
        start_time = datetime.now()
        st.session_state["start_time"] = start_time
        st.success("✅ Task Started! Complete it and upload proof.")
    
    if "start_time" in st.session_state:
        end_time = datetime.now()
        photo = st.file_uploader("Upload Proof of Completion")
        if st.button("Submit Task") and photo:
            umeme_points = calculate_umeme(st.session_state["start_time"], end_time)
            save_to_mongodb(collection_files, {"Student": student_name, "Task": task, "Umeme Points": umeme_points})
            st.success(f"✅ Task Submitted! You earned {umeme_points} Umeme Points!")

# --- Admin Dashboard ---
st.markdown("### 🔐 Admin Dashboard")
admin_password = st.text_input("Enter Admin Password", type="password")

if admin_password == "siriadmin123":
    st.success("✅ Admin Access Granted!")
    all_scores = list(collection_scores.find())
    if all_scores:
        df_scores = pd.DataFrame(all_scores)
        st.dataframe(df_scores)
        df_scores.to_csv("uwazi_scores.csv", index=False)
        st.download_button("Download CSV", "uwazi_scores.csv", "text/csv")
    else:
        st.warning("🚨 No student scores available!")
