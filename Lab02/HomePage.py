# This creates the main landing page for the Streamlit application.
# Contains an introduction to the project and guide users to other pages.

# Import Streamlit
import streamlit as st

# st.set_page_config() is used to configure the page's appearance in the browser tab.
# It's good practice to set this as the first Streamlit command in your script.
st.set_page_config(
    page_title="Homepage",  # The title that appears in the browser tab
    page_icon="🏠",         # An emoji that appears as the icon in the browser tab
)

# WELCOME PAGE TITLE
st.title("Welcome to the Data Dashboard! 📊")

# INTRODUCTORY TEXT
st.write("""
Welcome to my CS 1301 Web Development Lab 02! This application is designed to collect and visualize data.
You can navigate to the different pages using the sidebar on the left.

### How to use this app:
- **Survey Page**: users submit a predicted 12-month return and confidence for any ticker, and the Visuals page charts the community’s responses.
- **Visuals Page**: Go here to see the highest return %'s for Tech/AI stocks in 2026 visualized!

This project is part of CS 1301's Lab 2.
""")

# OPTIONAL: ADD AN IMAGE
# 1. Navigate to the 'images' folder in your Lab02 directory.
# 2. Place your image file (e.g., 'welcome_image.png') inside that folder.
# 3. Uncomment the line below and change the filename to match yours.
#
# st.image("images/welcome_image.png")
