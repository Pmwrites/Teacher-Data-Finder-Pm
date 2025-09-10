import streamlit as st
import pandas as pd
import re

# --- Page Configuration ---
st.set_page_config(
    page_title="Teacher Data Finder (Bulk Filter)",
    page_icon="🧑‍🏫",
    layout="wide"
)

# --- App Title and Description ---
st.title("🧑‍🏫 Teacher Data Finder (Bulk Filter)")
st.write(
    "Upload your Excel file and use the sidebar to filter for **multiple** "
    "School UDISE Codes and Subjects at once."
)

# --- File Uploader Widget ---
uploaded_file = st.file_uploader("Choose your Excel file", type="xlsx")

# --- Main Application Logic ---
if uploaded_file is not None:
    try:
        # Read the Excel file, assuming no header row
        df = pd.read_excel(uploaded_file, engine='openpyxl', header=None)

        # Define the column mapping based on A=0, B=1, etc.
        column_mapping = {
            0: 'Teacher ID',
            1: 'Block Name',
            2: 'School UDISE Code',
            3: 'School Name',
            4: 'Teacher Code',
            5: 'Teacher Name',
            6: 'Class Category',
            7: 'Subject Name'
        }
        
        # Rename the columns
        df.rename(columns=column_mapping, inplace=True)

        st.success("✅ File uploaded successfully! Use the filters on the left to search.")

        # --- Sidebar for Filters ---
        st.sidebar.header("Filter Options")

        # --- NEW: Text Area for multiple UDISE codes ---
        # We use a text_area for pasting multiple codes
        udise_input_text = st.sidebar.text_area(
            "Enter one or more School UDISE Codes",
            help="You can paste multiple codes separated by commas, spaces, or new lines."
        )

        # --- NEW: Multi-select for multiple subjects ---
        # We use a multiselect for choosing multiple subjects
        subject_list = sorted(df['Subject Name'].dropna().unique().tolist())
        selected_subjects = st.sidebar.multiselect(
            "Filter by Subject Name(s)",
            options=subject_list,
            default=[] # No subjects selected by default
        )

        # --- Filtering Data Logic ---
        # Start with the full, original dataframe
        filtered_df = df

        # --- NEW: Logic for filtering multiple UDISE codes ---
        # This block runs only if the user has typed something in the text area
        if udise_input_text:
            # First, clean up the input. Replace commas and newlines with spaces.
            # Then, split the string into a list of individual codes.
            udise_codes = [code.strip() for code in re.split(r'[,\s\n]+', udise_input_text) if code.strip()]
            
            # Use pandas' .isin() method to keep only the rows where the UDISE code
            # is in our list of user-provided codes.
            # .astype(str) is important to ensure we are comparing text with text.
            if udise_codes:
                filtered_df = filtered_df[filtered_df['School UDISE Code'].astype(str).isin(udise_codes)]

        # --- NEW: Logic for filtering multiple subjects ---
        # This block runs only if the user has selected one or more subjects
        if selected_subjects:
            # Use .isin() again to keep rows where the subject is in our list
            # of selected subjects.
            filtered_df = filtered_df[filtered_df['Subject Name'].isin(selected_subjects)]

        # --- Display Results ---
        st.header("Search Results")

        if filtered_df.empty:
            st.warning("No records found for the selected criteria. Please adjust your filters.")
        else:
            st.write(f"Displaying **{len(filtered_df)}** matching records.")
            st.dataframe(filtered_df, use_container_width=True)

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
        st.error("Please ensure your Excel file is formatted correctly.")

else:
    st.info("Please upload an Excel file to begin.")

