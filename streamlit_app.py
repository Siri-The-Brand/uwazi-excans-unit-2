import streamlit as st
import pandas as pd
import time
import os
import uuid
from datetime import datetime

# File Paths
STUDENT_CSV = "students.csv"
TASKS_CSV = "tasks.csv"
SCORES_CSV = "scores.csv"

# Initialize CSV Files if they do not exist
def initialize_csv(file_path, columns):
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=columns)
        df.to_csv(file_path, index=False)

initialize_csv(STUDENT_CSV, ["Student Name", "Class Code"])
initialize_csv(TASKS_CSV, ["Student", "Task", "Day", "Time Block"])
initialize_csv(SCORES_CSV, ["Student", "XP", "Rating"])

# Generate Unique Codes
def generate_code():
    return str(uuid.uuid4())[:6]

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
    "Day": ["Day 1"] * 6 + ["Day 2"] * 6 + ["Day 3"] * 6,
    "Time Block": ["Soma Time", "Siri Time", "Solver Time"] * 6,
    "Task": [
        "Logical Problem-Solving", "Creative Motion Expression", "Team Challenge",
        "Numerical Analysis", "Balance & Coordination", "Puzzle Deduction",
        "Inductive Reasoning", "Acrobatic Challenge", "Physical Coordination",
        "Pattern Recognition", "Statistical Analysis", "Critical Thinking",
        "Mathematical Operations", "Dexterity Challenge", "Strategic Thinking",
        "Abstract Reasoning", "Reflex & Speed Test", "Real-World Simulation"
    ]
})

# Ensure all columns have the same length
assert len(unit_schedule["Day"]) == len(unit_schedule["Time Block"]) == len(unit_schedule["Task"]), "Mismatch in column lengths!"

# CSE View or Student View
role = st.radio("Select Your Role:", ["CSE (Coach)", "Siri Solver (Student)", "Admin"])

if role == "CSE (Coach)":
    st.markdown("### 🏫 Class Management")
    cse_name = st.text_input("Enter Your Name (CSE)")
    day_selected = st.selectbox("Select Day", unit_schedule["Day"].unique())
    time_block_selected = st.selectbox("Select Time Block", unit_schedule["Time Block"].unique())
    task_selected = st.selectbox("Select Task", unit_schedule["Task"].unique())
    
    student_df = pd.read_csv(STUDENT_CSV)
    student_names = student_df["Student Name"].tolist() if not student_df.empty else []
    selected_student = st.selectbox("Select Student", student_names)
    
    if st.button("Assign Task"):
        df = pd.read_csv(TASKS_CSV)
        new_entry = pd.DataFrame({"Student": [selected_student], "Task": [task_selected], "Day": [day_selected], "Time Block": [time_block_selected]})
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(TASKS_CSV, index=False)
        st.success(f"✅ Task '{task_selected}' assigned to {selected_student}!")
    
    st.markdown("### 📊 Evaluate Student Performance")
    rating = st.selectbox("Select Rating", ["Excellent", "Great", "Good", "Needs Improvement"])
    xp_awarded = calculate_xp(rating)
    
    if st.button("Save Rating"):
        df = pd.read_csv(SCORES_CSV)
        new_entry = pd.DataFrame({"Student": [selected_student], "XP": [xp_awarded], "Rating": [rating]})
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(SCORES_CSV, index=False)
        st.success(f"✅ Rating Saved! {selected_student} earned {xp_awarded} XP!")

elif role == "Admin":
    st.markdown("### 🔐 Admin Dashboard")
    admin_password = st.text_input("Enter Admin Password", type="password")
    
    if admin_password == "siriadmin123":
        st.success("✅ Admin Access Granted!")
        df_scores = pd.read_csv(SCORES_CSV)
        st.dataframe(df_scores)
        st.download_button("Download CSV", df_scores.to_csv(index=False), "scores.csv", "text/csv")

elif role == "Siri Solver (Student)":
    st.markdown("### 📝 Join Class & Start Task")
    student_name = st.text_input("Enter Your Name (Siri Solver)")
    class_code = st.text_input("Enter Class Code")
    
    if st.button("Join Class"):
        df = pd.read_csv(STUDENT_CSV)
        new_entry = pd.DataFrame({"Student Name": [student_name], "Class Code": [class_code]})
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(STUDENT_CSV, index=False)
        st.success(f"✅ {student_name} joined class {class_code}!")
    
    task_df = pd.read_csv(TASKS_CSV)
    assigned_tasks = task_df[task_df["Student"] == student_name]
    
    if not assigned_tasks.empty:
        st.markdown("### Your Assigned Tasks")
        st.dataframe(assigned_tasks)
        if st.button("Start Task"):
            start_time = datetime.now()
            st.session_state["start_time"] = start_time
            st.success("✅ Task Started! Complete it and upload proof.")
    
    if "start_time" in st.session_state:
        end_time = datetime.now()
        photo = st.file_uploader("Upload Proof of Completion")
        if st.button("Submit Task") and photo:
            umeme_points = calculate_umeme(st.session_state["start_time"], end_time)
            st.success(f"✅ Task Submitted! You earned {umeme_points} Umeme Points!")
