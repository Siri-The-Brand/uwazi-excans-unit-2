import streamlit as st
import pandas as pd
import os
import uuid
from datetime import datetime

# --------------------------
# FILE PATHS
# --------------------------
STUDENT_CSV = "students.csv"
TASKS_ASSIGNED_CSV = "tasks_assigned.csv"
TASKS_LIST_CSV = "tasks_list.csv"
SCORES_CSV = "scores.csv"
SUBMISSIONS_CSV = "submissions.csv"

# --------------------------
# INITIALIZE CSV FILES
# --------------------------
def initialize_csv(file_path, columns):
    """Creates an empty CSV with the given columns if it does not exist."""
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=columns)
        df.to_csv(file_path, index=False)

# Ensuring all required CSVs exist
initialize_csv(STUDENT_CSV, ["Student Name", "Class Code"])
initialize_csv(TASKS_ASSIGNED_CSV, ["Student", "Task Name", "Day", "Time Block", "CSE"])
initialize_csv(SCORES_CSV, ["Student", "XP", "Rating", "Umeme"])
initialize_csv(SUBMISSIONS_CSV, ["Student", "Task Name", "File Type", "File Name", "Submission Time", "Start Time", "Day", "Time Block"])

# Predefined list of tasks for assignment
if not os.path.exists(TASKS_LIST_CSV):
    tasks_data = [
        ["Day 1", "LM Soma Time", "Spot the Logic", "Play a game of *Spot It!* to identify logic-based sequences.", "Building blocks, puzzles, problem-solving worksheets"],
        ["Day 1", "KIN Siri Time", "Express Through Movement", "Mimic emotions through movement in response to music or images.", "Music, scarves, props"],
        ["Day 1", "KIN Solver Time", "Tangled Team Escape", "Work as a team to untangle a *Human Knot*.", "Ropes, small objects for team tasks"],
        ["Day 1", "LM Soma Time", "Data Detective", "Analyze a dataset to determine patterns and trends.", "Graph paper, calculators, data analysis charts"],
        ["Day 2", "LM Soma Time", "Predict the Pattern", "Guess the next item in a logic sequence.", "Pattern blocks, prediction exercises"],
        ["Day 3", "LM Solver Time", "Master of Strategy", "Play a board game like chess and explain strategic moves.", "Board games, scenario-based challenges"],
        ["Day 4", "Soma & Siri Time", "Professional Interview", "Prepare and conduct an interview at the field trip location.", "Notebook, field trip guide"],
    ]
    df_tasks = pd.DataFrame(tasks_data, columns=["Day", "Element", "Task Name", "Description", "Resources"])
    df_tasks.to_csv(TASKS_LIST_CSV, index=False)

# --------------------------
# HELPER FUNCTIONS
# --------------------------
def generate_code():
    """Generates a short unique code."""
    return str(uuid.uuid4())[:6]

def calculate_xp(cse_rating):
    """Maps CSE rating to XP."""
    return {"Excellent": 30, "Great": 20, "Good": 15, "Needs Improvement": 5}.get(cse_rating, 0)

def calculate_umeme(start_time, end_time):
    """
    Calculates Umeme points based on time taken to complete a task.
    """
    time_taken = (end_time - start_time).total_seconds() / 60.0
    if time_taken <= 10:
        return 15
    elif time_taken <= 20:
        return 10
    else:
        return 5

# --------------------------
# STREAMLIT CONFIG & HEADER
# --------------------------
st.set_page_config(page_title="Uwazi Unit 2", page_icon="🎭", layout="wide")
st.title("🌟 Uwazi Unit 2: Theatrical Innovations")
st.subheader("Building Certitude Through Logic, Motion & Creative Expression")

# --------------------------
# SIDEBAR NAVIGATION
# --------------------------
menu_option = st.sidebar.radio("Navigation", [
    "🏫 Class Management",
    "📅 View Tasks & Assignments",
    "📊 CSE Dashboard",
    "🎓 Student Dashboard",
    "🔐 Admin Dashboard"
])

# --------------------------
# CSE DASHBOARD: ASSIGN TASKS
# --------------------------
if menu_option == "📊 CSE Dashboard":
    st.markdown("### 📊 CSE Dashboard - Assign Tasks")

    # Load student list
    student_df = pd.read_csv(STUDENT_CSV)
    if student_df.empty:
        st.warning("No students have joined any classes yet.")
    else:
        student_names = student_df["Student Name"].tolist()
        selected_student = st.selectbox("Select Student", student_names)

        # Select Day & Time Block
        day_choice = st.selectbox("Select Day", ["Day 1", "Day 2", "Day 3", "Day 4"])
        task_df = pd.read_csv(TASKS_LIST_CSV)
        task_options = task_df[task_df["Day"] == day_choice][["Element", "Task Name", "Description", "Resources"]]

        # Display available tasks
        st.markdown("### Available Tasks for Selected Day")
        st.dataframe(task_options)

        selected_task = st.selectbox("Select Task", task_options["Task Name"].tolist())

        # Assign Task
        if st.button("Assign Task"):
            assigned_tasks = pd.read_csv(TASKS_ASSIGNED_CSV)
            new_task = pd.DataFrame({
                "Student": [selected_student],
                "Task Name": [selected_task],
                "Day": [day_choice],
                "Time Block": [task_options[task_options["Task Name"] == selected_task]["Element"].values[0]],
                "CSE": ["CSE Name Placeholder"]
            })
            assigned_tasks = pd.concat([assigned_tasks, new_task], ignore_index=True)
            assigned_tasks.to_csv(TASKS_ASSIGNED_CSV, index=False)
            st.success(f"✅ Assigned '{selected_task}' to {selected_student}!")

# --------------------------
# STUDENT DASHBOARD: VIEW & SUBMIT TASKS
# --------------------------
elif menu_option == "🎓 Student Dashboard":
    st.markdown("### 🎓 Student Dashboard - My Tasks")

    student_name = st.text_input("Enter Your Name (Siri Solver)")
    
    if student_name:
        assigned_df = pd.read_csv(TASKS_ASSIGNED_CSV)
        student_tasks = assigned_df[assigned_df["Student"] == student_name]

        if student_tasks.empty:
            st.warning("No tasks assigned yet.")
        else:
            st.markdown("### My Assigned Tasks")
            st.dataframe(student_tasks)

            # Select a task to submit
            selected_task = st.selectbox("Select Task to Submit", student_tasks["Task Name"].tolist())
            uploaded_file = st.file_uploader("Upload Your Work", type=["png", "jpg", "pdf", "mp4", "mov", "txt", "docx"])

            if st.button("Submit Task"):
                submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                new_submission = pd.DataFrame({
                    "Student": [student_name],
                    "Task Name": [selected_task],
                    "File Type": [uploaded_file.type if uploaded_file else ""],
                    "File Name": [uploaded_file.name if uploaded_file else ""],
                    "Submission Time": [submission_time],
                    "Start Time": [""],  # Placeholder, to be updated later
                    "Day": [student_tasks[student_tasks["Task Name"] == selected_task]["Day"].values[0]],
                    "Time Block": [student_tasks[student_tasks["Task Name"] == selected_task]["Time Block"].values[0]]
                })
                submission_df = pd.concat([pd.read_csv(SUBMISSIONS_CSV), new_submission], ignore_index=True)
                submission_df.to_csv(SUBMISSIONS_CSV, index=False)
                st.success("✅ Task submitted successfully!")
