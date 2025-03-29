import streamlit as st

# Function to display the front page
def front_page():
    st.title('🏋️ Workout Planner App')

    st.image("images/gym_art.jpg", use_container_width=True)

    st.write("""
    ## Sample Text
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    """)

    st.write("""
    ## Group Members
    - **Alice Viegas** (20240572)
    - **Bernardo Faria** (20240579)
    - **Brandon Seichal** (20240592)
    - **Diogo Duarte** (20240525)
    """)

# Navigation
PAGES = {
    "Front Page": front_page
    # "Planner Page": planner_page,
    # "Visualizations": visualization_page
}

st.sidebar.title("Navigation")
choice = st.sidebar.radio("Go to", list(PAGES.keys()))
PAGES[choice]()