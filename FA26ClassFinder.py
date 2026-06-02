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

# UI
st.title("Class Schedule Finder")

day_input = st.selectbox("Select Day", list(day_map.keys()))
time_input = st.number_input("Enter Time (HHMM)", value=900)

selected_day_letter = day_map[day_input]

# Filtering
results = df[
    df["Days_List"].apply(lambda days: selected_day_letter in days)
    & (df["Section Meet Begin Time"] <= time_input)
    & (df["Section Meet End Time"] >= time_input)
]

# Display results
st.subheader("Classes Happening Now")

if results.empty:
    st.write("No classes found.")
else:
    for _, row in results.iterrows():
        st.markdown(f"""
        **{row['Course']} – {row['Title']}**  
        Instructor: {row['Instructor']}  
        Email: {row['Instructor Email']}  
        Room: {row['Room']}  
        Time: {row['Section Meet Begin Time']}–{row['Section Meet End Time']}
        """)