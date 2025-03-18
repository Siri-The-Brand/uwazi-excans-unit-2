import streamlit as st
import pandas as pd
import os
import uuid
from datetime import datetime

# --------------------------
# FILE PATHS
# --------------------------
CLASSES_CSV = "classes.csv"
STUDENT_CSV = "students.csv"
TASKS_ASSIGNED_CSV = "tasks_assigned.csv"
TASKS_LIST_CSV = "tasks_list.csv"
SCORES_CSV = "scores.csv"
SUBMISSIONS_CSV = "submissions.csv"
SESSIONS_CSV = "sessions.csv"

# --------------------------
# INITIALIZE CSV FILES
# --------------------------
def initialize_csv(file_path, columns):
    """Creates an empty CSV with the given columns if it does not exist."""
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=columns)
        df.to_csv(file_path, index=False)

# Ensuring all required CSVs exist
initialize_csv(CLASSES_CSV, ["Class Code", "Class Name", "CSE"])
initialize_csv(STUDENT_CSV, ["Student Name", "Class Code"])
initialize_csv(TASKS_ASSIGNED_CSV, ["Student", "Task Name", "Day", "Time Block", "CSE"])
initialize_csv(SCORES_CSV, ["Student", "XP", "Rating", "Umeme"])
initialize_csv(SUBMISSIONS_CSV, ["Student", "Task Name", "File Type", "File Name", "Submission Time", "Start Time", "Day", "Time Block"])
initialize_csv(SESSIONS_CSV, ["Class Code", "Session Status"])

# Predefined list of tasks for assignment
if not os.path.exists(TASKS_LIST_CSV):
    tasks_data = [
        ["Day 1", "LM Soma Time", "Spot the Logic", "Play a game of *Spot It!* to identify logic-based sequences.", "Building blocks, puzzles, problem-solving worksheets"],
        ["Day 1", "KIN Siri Time", "Express Through Movement", "Mimic emotions through movement in response to music or images.", "Music, scarves, props"],
        ["Day 1", "KIN Solver Time", "Tangled Team Escape", "Work as a team to untangle a *Human Knot*.", "Ropes, small objects for team tasks"],
        ["Day 1", "LM Soma Time", "Data Detective", "Analyze a dataset to determine patterns and trends.", "Graph paper, calculators, data analysis charts"],
        ["Day 2", "LM Soma Time", "Predict the Pattern", "Guess the next item in a logic sequence.", "Pattern blocks, prediction exercises"],
        ["Day 2", "KIN Siri Time", "Acrobat's Flow", "Perform a sequence of controlled acrobatic movements focusing on balance and strength.", "Exercise mats, safety pads"],
        ["Day 2", "KIN Solver Time", "Speed & Agility Race", "Complete a series of physical coordination challenges such as ladder drills and obstacle navigation.", "Jump ropes, reaction speed tools"],
        ["Day 2", "LM Soma Time", "Color Code Challenge", "Sort and arrange items based on a color and pattern logic rule.", "Color sorting games, sequencing cards"],
        ["Day 2", "LM Siri Time", "Chart the Data", "Analyze bar charts to identify key statistical insights and predict trends.", "Bar charts, statistical datasets"],
        ["Day 2", "LM Solver Time", "Solve the Mystery", "Analyze a case study to uncover logical inconsistencies and solve a problem.", "Case study problems, debate prompts"]
        ["Day 3", "LM Solver Time", "Master of Strategy", "Play a board game like chess and explain strategic moves.", "Board games, scenario-based challenges"],
        ["Day 3", "LM Soma Time", "Number Puzzle Challenge", "Solve mathematical puzzles using operations like addition, subtraction, multiplication, and division.", "Math manipulatives, counters"],
        ["Day 3", "KIN Siri Time", "Steady Hands", "Complete a dexterity test by threading beads or sculpting fine details in clay.", "Fine motor skill activities (clay, threading beads)"],
        ["Day 3", "LM Solver Time", "Master of Strategy", "Play a board game like chess and explain strategic moves.", "Board games, scenario-based challenges"],
        ["Day 3", "LM Soma Time", "Mind's Eye", "Interpret abstract optical illusions and explain their logical or artistic significance.", "Optical illusions, abstract art exploration"],
        ["Day 3", "KIN Siri Time", "Fast Reflex Test", "Perform a reaction-time challenge using stopwatches and movement drills.", "Stopwatches, fast-paced movement drills"],
        ["Day 3", "Solver Time", "Virtual Problem-Solver", "Engage in a VR-based real-world simulation and solve a presented challenge.", "VR headset or interactive AR experience for simulations"]
        ["Day 4", "Soma & Siri Time", "Professional Interview", "Prepare and conduct an interview at the field trip location.", "Notebook, field trip guide"],
        ["Day 4", "Soma & Siri Time", "Field Trip to Observe Real-World Practitioners", "Visit Apollo space center, and gymnastics/Acrobatics Training Center"],
        ["Day 4", "Solver Time", "Hands-on Industry Engagement", "Interview professionals using Kinesthetic and Logical-Mathematical Intelligence"],
        ["Day 4", "Siri Time", "Reflection & Discussion", "Journaling and group discussion on field trip learnings"],
    ]
    df_tasks = pd.DataFrame(tasks_data, columns=["Day", "Element", "Task Name", "Description", "Resources"])
    df_tasks.to_csv(TASKS_LIST_CSV, index=False)

# --------------------------
# HELPER FUNCTIONS
# --------------------------
def generate_code():
    """Generates a short unique code."""
    return str(uuid.uuid4())[:6]
    
def check_session_status(class_code):
    """Check if a class has an active session."""
    df_sessions = pd.read_csv(SESSIONS_CSV)
    session = df_sessions[df_sessions["Class Code"] == class_code]
    return not session.empty and session["Session Status"].iloc[0] == "Active"
    
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

def ai_feedback(text):
    """Simple AI-generated feedback for text submissions."""
    if not text:
        return "No response provided."
    elif len(text) < 50:
        return "Try expanding your response with more details."
    elif "because" in text or "reason" in text:
        return "Great job explaining your reasoning!"
    else:
        return "Good effort! Consider adding examples or deeper insights."

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
    "📊 CSE Dashboard",
    "🎓 Student Dashboard",
    "🔐 Admin Dashboard"
])

# --------------------------
# 🏫 CLASS MANAGEMENT (CSEs create classes)
# --------------------------
if menu_option == "🏫 Class Management":
    st.markdown("### 🏫 Manage Your Class")

    cse_name = st.text_input("Enter Your Name (CSE)")
    class_name = st.text_input("Enter Class Name")
    class_code = generate_code()

    if st.button("Create Class"):
        df_classes = pd.read_csv(CLASSES_CSV)
        new_class = pd.DataFrame({"Class Code": [class_code], "Class Name": [class_name], "CSE": [cse_name]})
        df_classes = pd.concat([df_classes, new_class], ignore_index=True)
        df_classes.to_csv(CLASSES_CSV, index=False)
        st.success(f"✅ Class '{class_name}' created! Class Code: {class_code}")

# --------------------------
# 📊 CSE DASHBOARD: ASSIGN TASKS TO STUDENTS IN THEIR CLASS
# --------------------------
elif menu_option == "📊 CSE Dashboard":
    st.markdown("### 📊 CSE Dashboard - Assign Tasks")

    # Load CSE's classes
    df_classes = pd.read_csv(CLASSES_CSV)
    if df_classes.empty:
        st.warning("No classes created yet. Create one in 'Class Management'.")
    else:
        cse_classes = df_classes["Class Code"].tolist()
        selected_class = st.selectbox("Select Your Class", cse_classes)
        
        # Session Management
        session_active = check_session_status(selected_class)
        if session_active:
            st.success("✅ Session is ACTIVE for this class.")
        else:
            if st.button("Start Session"):
                df_sessions = pd.read_csv(SESSIONS_CSV)
                new_session = pd.DataFrame({"Class Code": [selected_class], "Session Status": ["Active"]})
                df_sessions = pd.concat([df_sessions, new_session], ignore_index=True)
                df_sessions.to_csv(SESSIONS_CSV, index=False)
                st.success(f"✅ Session started for class {selected_class}")

        # Assign Tasks
        student_df = pd.read_csv(STUDENT_CSV)
        students_in_class = student_df[student_df["Class Code"] == selected_class]["Student Name"].tolist()

        if students_in_class:
            selected_student = st.selectbox("Select Student", students_in_class)

            # Select Day & Task
            day_choice = st.selectbox("Select Day", ["Day 1", "Day 2", "Day 3", "Day 4"])
            task_df = pd.read_csv(TASKS_LIST_CSV)
            task_options = task_df[task_df["Day"] == day_choice]

            # Display available tasks
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

            # View submissions
            st.markdown("### 📌 Review Student Work")
            df_submissions = pd.read_csv(SUBMISSIONS_CSV)

            if not df_submissions.empty:
                st.dataframe(df_submissions)
                submission_students = df_submissions["Student"].unique().tolist()
                selected_student_review = st.selectbox("Select Student to Assess", submission_students)
                
                student_submissions = df_submissions[df_submissions["Student"] == selected_student_review]
                selected_task_review = st.selectbox("Select Task to Review", student_submissions["Task Name"].unique().tolist())

                task_details = student_submissions[student_submissions["Task Name"] == selected_task_review].iloc[0]
                st.markdown(f"📂 **File Submitted:** {task_details['File Name']}  \n📅 **Submission Time:** {task_details['Submission Time']}")

                # Assign a rating
                rating = st.selectbox("Rate the Submission", ["Excellent", "Great", "Good", "Needs Improvement"])
                xp_awarded = calculate_xp(rating)

                if st.button("Save Rating"):
                    df_scores = pd.read_csv(SCORES_CSV)
                    new_entry = pd.DataFrame({
                        "Student": [selected_student_review],
                        "XP": [xp_awarded],
                        "Rating": [rating],
                        "Umeme": [0]
                    })
                    df_scores = pd.concat([df_scores, new_entry], ignore_index=True)
                    df_scores.to_csv(SCORES_CSV, index=False)
                    st.success(f"✅ Rating Saved! {selected_student_review} earned {xp_awarded} XP!")

# --------------------------
# 🎓 STUDENT DASHBOARD: JOIN CLASS, VIEW TASKS, SUBMIT WORK
# --------------------------
elif menu_option == "🎓 Student Dashboard":
    st.markdown("### 🎓 Student Dashboard - Join Class & Submit Work")

    student_name = st.text_input("Enter Your Name")
    class_code = st.text_input("Enter Class Code")

    if st.button("Join Class"):
        df_students = pd.read_csv(STUDENT_CSV)
        new_entry = pd.DataFrame({"Student Name": [student_name], "Class Code": [class_code]})
        df_students = pd.concat([df_students, new_entry], ignore_index=True)
        df_students.to_csv(STUDENT_CSV, index=False)
        st.success(f"✅ {student_name} joined class {class_code}!")

    # --------------------------
    # VIEW & SUBMIT ASSIGNED TASKS
    # --------------------------
    if check_session_status(class_code):
        assigned_df = pd.read_csv(TASKS_ASSIGNED_CSV)
        student_tasks = assigned_df[assigned_df["Student"] == student_name]

        if not student_tasks.empty:
            st.markdown("### 📌 My Assigned Tasks")
            st.dataframe(student_tasks)
        else:
            st.warning("No tasks have been assigned yet.")
    else:
        st.warning("🚫 Session has not started for this class. Wait for the CSE to start the session.")

    assigned_df = pd.read_csv(TASKS_ASSIGNED_CSV)
    student_tasks = assigned_df[assigned_df["Student"] == student_name]

    if not student_tasks.empty:
        st.markdown("### 📌 My Assigned Tasks")
        st.dataframe(student_tasks)

        selected_task = st.selectbox("Select Task to Submit", student_tasks["Task Name"].tolist())

        # Submission Options
        st.markdown("### 📤 Submit Your Work")

        submission_type = st.radio(
            "Choose Submission Type:",
            ["Text", "Upload File", "Video Recording", "Audio Recording"]
        )

        submission_data = None
        file_name = None
        file_type = None
        start_time = datetime.now()  # Start timing the task

        if submission_type == "Text":
            submission_data = st.text_area("Enter your response:")
            file_type = "text"
            file_name = f"{student_name}_{selected_task}_response.txt"

        elif submission_type == "Upload File":
            uploaded_file = st.file_uploader("Upload Your Work", type=["png", "jpg", "pdf", "mp4", "mov", "txt", "docx"])
            if uploaded_file:
                submission_data = uploaded_file.getvalue()
                file_name = uploaded_file.name
                file_type = uploaded_file.type

        elif submission_type == "Video Recording":
            st.warning("📹 Video recording feature is under development. Please upload a video file for now.")

        elif submission_type == "Audio Recording":
            st.warning("🎤 Audio recording feature is under development. Please upload an audio file for now.")

        # Save Submission
        if st.button("Submit Task"):
            end_time = datetime.now()  # End timing the task
            umeme_points = calculate_umeme(start_time, end_time)

            # AI-Generated Feedback for Text Submissions
            feedback = ai_feedback(submission_data) if submission_type == "Text" else "CSE will review."

            submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_submission = pd.DataFrame({
                "Student": [student_name],
                "Task Name": [selected_task],
                "File Type": [file_type if file_type else "N/A"],
                "File Name": [file_name if file_name else "N/A"],
                "Submission Time": [submission_time],
                "Start Time": [start_time.strftime("%Y-%m-%d %H:%M:%S")],
                "Day": [student_tasks[student_tasks["Task Name"] == selected_task]["Day"].values[0]],
                "Time Block": [student_tasks[student_tasks["Task Name"] == selected_task]["Time Block"].values[0]],
                "Feedback": [feedback]
            })

            submission_df = pd.concat([pd.read_csv(SUBMISSIONS_CSV), new_submission], ignore_index=True)
            submission_df.to_csv(SUBMISSIONS_CSV, index=False)

            # Save Umeme Points
            df_scores = pd.read_csv(SCORES_CSV)
            new_score = pd.DataFrame({
                "Student": [student_name],
                "XP": [0],  # XP to be assigned by CSE
                "Rating": ["Pending"],
                "Umeme": [umeme_points]
            })
            df_scores = pd.concat([df_scores, new_score], ignore_index=True)
            df_scores.to_csv(SCORES_CSV, index=False)

            st.success(f"✅ Task submitted successfully! You earned {umeme_points} Umeme Points! ⚡")
            st.markdown(f"📝 **AI Feedback:** {feedback}")

# --------------------------
# 🔐 ADMIN DASHBOARD (View & Manage Data)
# --------------------------
if menu_option == "🔐 Admin Dashboard":
    admin_password = st.text_input("Enter Admin Password", type="password")
    
    if admin_password == "siriadmin123":
        st.success("✅ Access Granted to Admin Dashboard")
        
        # Display class information
        st.markdown("#### 📚 All Classes")
        if os.path.exists(CLASSES_CSV):
            df_classes = pd.read_csv(CLASSES_CSV)
            if not df_classes.empty:
                st.dataframe(df_classes)
            else:
                st.warning("No class data available.")
        else:
            st.error("🚨 Class data file not found!")
        
        # Display student data
        st.markdown("#### 🎓 Registered Students")
        if os.path.exists(STUDENT_CSV):
            df_students = pd.read_csv(STUDENT_CSV)
            if not df_students.empty:
                st.dataframe(df_students)
            else:
                st.warning("No student data available.")
        else:
            st.error("🚨 Student data file not found!")
        
        # Display task data
        st.markdown("#### 📌 Assigned Tasks")
        if os.path.exists(TASKS_LIST_CSV):
            df_tasks = pd.read_csv(TASKS_LIST_CSV)
            if not df_tasks.empty:
                st.dataframe(df_tasks)
            else:
                st.warning("No task data available.")
        else:
            st.error("🚨 Task data file not found!")
        
        # Display scores
        st.markdown("#### 🏆 Student Scores & XP")
        if os.path.exists(SCORES_CSV):
            df_scores = pd.read_csv(SCORES_CSV)
            if not df_scores.empty:
                st.dataframe(df_scores)
            else:
                st.warning("No scores recorded yet.")
        else:
            st.error("🚨 Scores file not found!")
        
        # Display submissions with student names
        st.markdown("#### 📸 Student Submissions")
        if os.path.exists(SUBMISSIONS_CSV):
            df_submissions = pd.read_csv(SUBMISSIONS_CSV)
            if not df_submissions.empty:
                # Ensure column names exist
                expected_columns = ["Student", "Task", "File Type", "File Name", "Submission Time"]
                available_columns = df_submissions.columns.tolist()
                
                missing_columns = [col for col in expected_columns if col not in available_columns]
                
                if not missing_columns:
                    st.dataframe(df_submissions[expected_columns])
                else:
                    st.error(f"🚨 Missing columns in submissions file: {missing_columns}")
            else:
                st.warning("No submissions recorded yet.")
        else:
            st.error("🚨 Submissions data file not found!")

        # Option to download all data
        st.markdown("### 📥 Download Reports")
        
        if os.path.exists(CLASSES_CSV):
            st.download_button("Download Class Data", df_classes.to_csv(index=False), "classes.csv", "text/csv")
        if os.path.exists(STUDENT_CSV):
            st.download_button("Download Student Data", df_students.to_csv(index=False), "students.csv", "text/csv")
        if os.path.exists(TASKS_LIST_CSV):
            st.download_button("Download Task Data", df_tasks.to_csv(index=False), "tasks.csv", "text/csv")
        if os.path.exists(SCORES_CSV):
            st.download_button("Download Score Data", df_scores.to_csv(index=False), "scores.csv", "text/csv")
        if os.path.exists(SUBMISSIONS_CSV):
            st.download_button("Download Submissions Data", df_submissions.to_csv(index=False), "submissions.csv", "text/csv")
    
    else:
        st.error("❌ Incorrect Password. Access Denied.")
