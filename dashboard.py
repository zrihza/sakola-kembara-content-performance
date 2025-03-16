import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page title and layout
st.set_page_config(page_title="Content Performance Dashboard", layout="wide")

# Sidebar
with st.sidebar:
    st.image("https://media.licdn.com/dms/image/C5603AQEweWGGp1ovNA/profile-displayphoto-shrink_400_400/0/1632043804563?e=1712188800&v=beta&t=GF5DzzOih1xnd7sWj6aRDG6X1kR5FpNBLKVuG1OaHRw", width=150)
    st.markdown("[LinkedIn](https://www.linkedin.com/in/ihza-zhafran-010a0b21a/)")
    st.image("Marketing.png", width=50)
    st.markdown("[GitHub](https://github.com/zrihza)")
    st.write("\n\nCopyright © Ihza Zhafran")

# Download file from Google Drive
st.title("Content Performance Dashboard")

# Read data
df = pd.read_excel("ig_data.xlsx", sheet_name="bi-weekly")

# Data processing
df["Interactions"] = df["Likes"] + df["Shares"] + df["Comments"] + df["Saves"]
df["Interaction Rate"] = df["Interactions"] / df["Reach"]

# Section 1: CTA Effectiveness
st.subheader("1. How Effective is CTA from Talents?")
col1, col2 = st.columns(2)

with col2:
    st.write("### Interaction Rate Distribution")
    df_pie = df.groupby("talent")["Interaction Rate"].mean()
    
    # Generate lighter color palette (viridis)
    bright_colors = sns.color_palette("viridis", len(df_pie))

    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        df_pie,
        labels=df_pie.index,
        autopct="%1.1f%%",
        colors=bright_colors  # Menggunakan "viridis" yang lebih terang
    )
    st.pyplot(fig)

# Buat dictionary warna berdasarkan talent
talent_colors = dict(zip(df_pie.index, bright_colors))

with col1:
    st.write("### Views vs Interactions per Talent")
    df_plot = df.groupby("talent")[["Views", "Interactions"]].sum().reset_index()

    fig, ax = plt.subplots(figsize=(8, 4))
    df_plot.set_index("talent").plot(kind="bar", color=[talent_colors[t] for t in df_plot["talent"]], ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Section 2: Content Engagement
st.subheader("2. How Interesting is the Content for the Audience?")
st.write("### Average Watch Time per Talent")
df_watch = df.groupby("talent")["Avg Watch Time (Seconds)"].mean().reset_index()  # Perbaikan nama kolom

fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(x="talent", y="Avg Watch Time (Seconds)", data=df_watch, palette=[talent_colors[t] for t in df_watch["talent"]], ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# Section 3: Follows per Talent
st.subheader("3. How Many Follow Us After Watching Talent's Content?")
st.write("### Follows per Talent")
df_follow = df.groupby("talent")["Follows"].sum()

fig, ax = plt.subplots()
ax.pie(df_follow, labels=df_follow.index, autopct="%1.1f%%", colors=[talent_colors[t] for t in df_follow.index])
st.pyplot(fig)