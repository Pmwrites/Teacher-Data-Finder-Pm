import streamlit as st
import pandas as pd

# --- Page Configuration ---
st.set_page_config(
    page_title="Teacher Data Finder",
    page_icon="🧑‍🏫",
    layout="wide"
)

# --- App Title and Description ---
st.title("🧑‍🏫 Teacher Data Finder")
st.write(
    "Upload your Excel file and use the sidebar filters to find teacher information "
    "by School UDISE Code or Subject Name."
)

# --- File Uploader Widget ---
uploaded_file = st.file_uploader("Choose your Excel file", type="xlsx")

# --- Main Application Logic ---
if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file, engine='openpyxl', header=None)

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
        
        df.rename(columns=column_mapping, inplace=True)

        st.success("✅ File uploaded successfully! Use the filters on the left to search.")

        # --- Sidebar for Filters ---
        st.sidebar.header("Filter Options")

        school_code_search = st.sidebar.text_input(
            "Search by School UDISE Code",
            help="Enter a partial or full school code to search."
        )

        subject_list = ["All"] + sorted(df['Subject Name'].dropna().unique().tolist())
        subject_filter = st.sidebar.selectbox("Filter by Subject Name", subject_list)

        # --- Filtering Data Logic ---
        filtered_df = df

        if school_code_search:
            filtered_df = filtered_df[
                filtered_df['School UDISE Code'].astype(str).str.contains(school_code_search, case=False, na=False)
            ]

        if subject_filter != "All":
            filtered_df = filtered_df[filtered_df['Subject Name'] == subject_filter]

        # --- Display Results ---
        st.header("Search Results")

        if filtered_df.empty:
            st.warning("No records found for the selected criteria. Please adjust your filters.")
        else:
            st.write(f"Displaying **{len(filtered_df)}** matching records.")
            st.dataframe(filtered_df, use_container_width=True)

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
        st.error("Please ensure your Excel file is formatted correctly with the first 8 columns.")

else:
    st.info("Please upload an Excel file to begin.")

