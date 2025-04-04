import streamlit as st
import pandas as pd
import numpy as np
import cv2  # opencv-python library for image processing
import json
from PIL import Image  # pillow library for image processing

# Function to display the front page
def front_page():
    st.title('🏋️ Workout Planner App')

    st.image("images/gym_art.jpg", use_container_width=True)

    st.write("""
    ## Welcome to the Workout Planner App! 💪
    This app helps you plan your workouts and visualize the muscles targeted by different exercises. You can select various exercises, and the app will highlight the corresponding muscles on an anatomical template.

    ### How it works:
    - Select the exercises you want to include in your workout routine.
    - The app will highlight the muscles that are engaged during those exercises.
    - Use this to tailor your workouts and target specific muscle groups.
    """)

    st.write("""
    ## Group Members
    - **Alice Viegas** (20240572)
    - **Bernardo Faria** (20240579)
    - **Brandon Seichal** (20240592)
    - **Diogo Duarte** (20240525)
    """)

# Load exercise data
def load_exercise_data():
    df = pd.read_csv("data/gym_exercises.csv")
    df["muscle_gp"] = df["muscle_gp"].str.replace(" ", "")
    return df

# Load muscle annotations
def load_muscle_data():
    with open("annotations.json", "r") as f:
        data = json.load(f)
        # Access the muscle regions directly from the "template.jpg" key
        return data.get("template.jpg", {}).get("regions", {})

# Load and prepare template image
def load_template_image():
    image = cv2.imread("images/template.jpg")
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


# init_col_1 = (255, 217, 102) 
# init_col_2 = (255, 140, 66)  
# init_col_3 = (216, 59, 1)

# Function to get the color based on the number of exercises targeting the muscle
def get_gradient_color(count):

    color_1 = (255, 185, 50)  # Bright golden amber
    color_2 = (230, 150, 60)  # Warm sunset orange
    color_3 = (180, 110, 50)  # Subdued burnt orange
    color_4 = (120, 80, 40)   # Deep bronze
    color_5 = (60, 50, 30)    # Dark brownish-bronze

    if count == 1:
        return color_1
    elif count == 2:
        return color_2
    elif count == 3:
        return color_3
    elif count == 4:
        return color_4
    else:
        return color_5



# Function to highlight selected muscles
def highlight_muscles(selected_exercises, exercise_data, muscle_data, template_image):
    highlighted_image = template_image.copy()
    muscle_counts = {}

    # Count the number of exercises targeting each muscle
    for exercise in selected_exercises:
        muscles = exercise_data[exercise_data["Exercise_Name"] == exercise]["muscle_gp"].values
        for muscle in muscles:
            muscle_counts[muscle] = muscle_counts.get(muscle, 0) + 1

    for region in muscle_data.values():
        muscle_label = region["region_attributes"].get("label", "")
        count = muscle_counts.get(muscle_label, 0)
        
        if count > 0:
            # Get the appropriate color based on the muscle count
            highlight_color = get_gradient_color(count)
            points = np.array(list(zip(region["shape_attributes"]["all_points_x"],
                                       region["shape_attributes"]["all_points_y"])), np.int32)
            points = points.reshape((-1, 1, 2))
            cv2.fillPoly(highlighted_image, [points], highlight_color)

    return Image.fromarray(highlighted_image)

def planner_page():
    # Streamlit UI
    st.title("Gym Exercise Muscle Visualization")

    # Load data
    exercise_data = load_exercise_data()
    muscle_data = load_muscle_data()
    template_image = load_template_image()

    # Load premade workouts
    premade_workouts = {
        "MCDD Workout": [
            "Treadmill running", "Leg Press", "Leg Extensions", "Lying Leg Curls", "Leverage Decline Chest Press",
            "Rocky Pull-Ups/Pulldowns", "Standing dumbbell shoulder press", "Dumbbell Bicep Curl", 
            "Single-arm cable triceps extension", "Elbow plank", "Rower"
        ],
        "Intensity Test": [
            "Tire flip", "Standing Hip Circles", "Clam", "Suspended ab fall-out", "Ab bicycle", "Ab Roller",
            "Incline cable chest press", "Leverage Chest Press", "Cable Chest Press", "Chest dip",
            "Seated barbell shoulder press", "Smith machine shoulder press", "Seated cable shoulder press",
            "Machine shoulder press", "Barbell Shoulder Press"
        ]
    }

    # Sidebar for selecting premade workouts
    st.sidebar.title("Workout Options")
    selected_workout = st.sidebar.selectbox("Choose a Workout Plan:", ["None"] + list(premade_workouts.keys()))

    # Initialize selected exercises
    selected_exercises = []

    # Populate exercises based on selected workout
    if selected_workout != "None":
        selected_exercises = premade_workouts[selected_workout]

    # Multiselect dropdown for selecting exercises
    selected_exercises = st.multiselect(
        "Select Exercises:",
        exercise_data["Exercise_Name"].unique(),
        default=selected_exercises  # Preselect exercises
    )

    # Display the selected workout's visualization
    if selected_exercises:
        result_image = highlight_muscles(selected_exercises, exercise_data, muscle_data, template_image)
        st.image(result_image, caption="Highlighted Muscles", use_container_width=True)
    else:
        st.image(template_image, caption="Workout Preview", use_container_width=True)

# Navigation
PAGES = {
    "Front Page": front_page,
    "Planner Page": planner_page
}

st.sidebar.title("Navigation")
choice = st.sidebar.radio("Go to", list(PAGES.keys()))
PAGES[choice]()