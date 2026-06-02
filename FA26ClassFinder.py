import pandas as pd
import streamlit as st

# Load your CSV
df = pd.read_csv("FA26_cleaned_room_schedule.csv")

# Map full day → schedule letters
day_map = {
    "Monday": "M",
    "Tuesday": "T",
    "Wednesday": "W",
    "Thursday": "R"
}

# Expand MW/TR into lists
def expand_days(schedule):
    return list(schedule)

df["Days_List"] = df["Section Meet Schedule"].apply(expand_days)

# Group Map
group_map = {
    # Social Science
    "ANTH": "Social Science",
    "ECON": "Social Science",
    "ETHN": "Social Science",
    "GBST": "Social Science",
    "HIST": "Social Science",
    "PHIL": "Social Science",
    "POLS": "Social Science",
    "PSYC": "Social Science",
    "SOCI": "Social Science",

    # Creative Arts
    "ARTH": "Creative Arts",
    "ART": "Creative Arts",
    "DGME": "Creative Arts",
    "MUS.": "Creative Arts",

    # Health and Wellness
    "ADS": "Health and Wellness"
}

# Color Map
color_map = {
    "Social Science": "#1d4e89",  
    "Creative Arts": "#7D6AC8",    
    "Health and Wellness": "#f79256", 
    "Other": "#7f7f7f"             
}

# Group Icons
group_icons = {
    "Social Science": "📘",
    "Creative Arts": "🎨",
    "Health and Wellness": "🧡",
    "Other": "⚪"
}

# Extract building number (everything before '-')
df["Building"] = (
    df["Section Building Code"]
    .astype(str)
    .str.split("-").str[0]
    .replace({"0": "Unknown", "UNKN": "Unknown"})
)

# Extract prefix from "DGME-100-AA"
def get_prefix(course):
    return course.split("-")[0]

# Extract prefix
df["Prefix"] = df["Course"].apply(get_prefix)

# Assign group
df["Group"] = df["Prefix"].map(group_map).fillna("Other")

# UI
st.title("FA26 CASS Class Finder")

# Day Select
day_input = st.selectbox("Select Day", list(day_map.keys()))
time_input = st.number_input("Enter Time (HHMM)", value=900)

selected_day_letter = day_map[day_input]

# ACC Filter
group_input = st.selectbox(
    "Filter by ACC",
    ["All", "Social Science", "Creative Arts", "Health and Wellness", "Other"]
)

# Filtering
results = df[
    df["Days_List"].apply(lambda days: selected_day_letter in days)
    & (df["Section Meet Begin Time"] <= time_input)
    & (df["Section Meet End Time"] >= time_input)
]

if group_input != "All":
    results = results[results["Group"] == group_input]

# Sort results by time
results = results.sort_values(by="Section Meet Begin Time")

# Display results
st.subheader("Classes Happening Now")

# if results.empty:
#    st.write("No classes found.")
# else:
#    for _, row in results.iterrows():
#        st.markdown(f"""
#        **{row['Course']} – {row['Title']}**  
#        Instructor: {row['Instructor']}  
#        Email: {row['Instructor Email']}  
#        Building: {row['Building']}  
#        Room: {row['Room']}  
#        Time: {row['Section Meet Begin Time']}–{row['Section Meet End Time']}
#        """)


if results.empty:
    st.write("No classes found.")
else:
    for _, row in results.iterrows():
        group = row["Group"]
        color = color_map.get(group, "#333333")
        icon = group_icons.get(group, "⚪")

        st.markdown(f"""
        <div style="
            border-left: 8px solid {color};
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 10px;
            background-color: {color}22;
        ">
            <h4 style="color:{color}; margin-bottom:5px;">
                {icon} {row['Course']} – {row['Title']}
            </h4>
            <b>Category:</b> {group}<br>
            <b>Instructor:</b> {row['Instructor']}<br>
            <b>Email:</b> <a href="mailto:{row['Instructor Email']}">{row['Instructor Email']}</a><br>
            <b>Location:</b> Bldg {row['Building']}, Room {row['Room']}<br>
            <b>Time:</b> {row['Section Meet Begin Time']}–{row['Section Meet End Time']}
        </div>
        """, unsafe_allow_html=True)
