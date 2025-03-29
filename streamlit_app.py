import streamlit as st
import pandas as pd
import numpy as np
import cv2
import json
from PIL import Image

# Load exercise data
def load_exercise_data():
    df = pd.read_csv("data/gym_exercises.csv")
    df["muscle_gp"] = df["muscle_gp"].str.replace(" ", "")
    return df

# Load muscle annotations
def load_muscle_data():
    with open("annotations.json", "r") as f:
        return json.load(f)["images/template.jpg"]["regions"]

# Load and prepare template image
def load_template_image():
    image = cv2.imread("images/template.jpg")
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Function to highlight selected muscles
def highlight_muscles(selected_exercises, exercise_data, muscle_data, template_image):
    highlighted_image = template_image.copy()
    muscles_to_highlight = set()
    
    for exercise in selected_exercises:
        muscles_to_highlight.update(exercise_data[exercise_data["Exercise_Name"] == exercise]["muscle_gp"].values)
    
    highlight_color = (255, 0, 0)  # Red in RGB
    for region in muscle_data.values():
        muscle_label = region["region_attributes"]["label"]
        if muscle_label in muscles_to_highlight:
            points = np.array(list(zip(region["shape_attributes"]["all_points_x"],
                                       region["shape_attributes"]["all_points_y"])), np.int32)
            points = points.reshape((-1, 1, 2))
            cv2.fillPoly(highlighted_image, [points], highlight_color)
    
    return Image.fromarray(highlighted_image)

# Streamlit UI
st.title("Gym Exercise Muscle Visualization")

# Display gym artwork
st.image("images/gym_art.jpg", use_column_width=True)

exercise_data = load_exercise_data()
muscle_data = load_muscle_data()
template_image = load_template_image()

selected_exercises = st.multiselect("Select Exercises:", exercise_data["Exercise_Name"].unique())

if selected_exercises:
    result_image = highlight_muscles(selected_exercises, exercise_data, muscle_data, template_image)
    st.image(result_image, caption="Highlighted Muscles", use_column_width=True)
else:
    st.image(template_image, caption="Muscle Template", use_column_width=True)