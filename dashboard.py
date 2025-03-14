import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import gdown

# Set page title and layout
st.set_page_config(page_title="Content Performance Dashboard", layout="wide")

# Sidebar
with st.sidebar:
    st.image("https://media.licdn.com/dms/image/C5603AQEweWGGp1ovNA/profile-displayphoto-shrink_400_400/0/1632043804563?e=1712188800&v=beta&t=GF5DzzOih1xnd7sWj6aRDG6X1kR5FpNBLKVuG1OaHRw", width=150)
    st.markdown("[LinkedIn](https://www.linkedin.com/in/ihza-zhafran-010a0b21a/)")
    st.image("https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png", width=50)
    st.markdown("[GitHub](https://github.com/zrihza)")
    st.write("\n\nCopyright © Ihza Zhafran")

# Download file from Google Drive
st.title("Content Performance Dashboard")

file_url = "https://drive.google.com/uc?id=1SxBOsTOf-x4SCJOVbScfuGntCGB5tjjH"
output_file = "ig_data.xlsx"
gdown.download(file_url, output_file, quiet=False)

# Read data
df = pd.read_excel(output_file, sheet_name="bi-weekly")

# Data processing
df["Interactions"] = df["Likes"] + df["Shares"] + df["Comments"] + df["Saves"]
df["Interaction Rate"] = df["Interactions"] / df["Reach"]

# Generate consistent colors for each talent
unique_talents = df["talent"].unique()
talent_colors = sns.color_palette("husl", len(unique_talents))  # Husl gives distinct colors
color_dict = dict(zip(unique_talents, talent_colors))

# Section 1: CTA Effectiveness
st.subheader("1. How Effective is CTA from Talents?")
col1, col2 = st.columns(2)

with col1:
    st.write("### Views vs Interactions per Talent")
    df_plot = df.groupby("talent")[["Views", "Interactions"]].sum().reset_index()

    fig, ax = plt.subplots(figsize=(8, 4))
    df_plot.set_index("talent").plot(kind="bar", color=[color_dict[t] for t in df_plot["talent"]], ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

with col2:
    st.write("### Interaction Rate Distribution")
    df_pie = df.groupby("talent")["Interaction Rate"].mean()

    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        df_pie,
        labels=df_pie.index,
        autopct="%1.1f%%",
        colors=[color_dict[t] for t in df_pie.index]
    )
    st.pyplot(fig)

# Section 2: Content Engagement
st.subheader("2. How Interesting is the Content for the Audience?")
st.write("### Average Watch Time per Talent")
df_watch = df.groupby("talent")["Avg Watch Time (Seconds)"].mean().reset_index()

fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(x="talent", y="Avg Watch Time (Seconds)", data=df_watch, palette="magma", ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# Section 3: Follows per Talent
st.subheader("3. How Many Follow Us After Watching Talent's Content?")
st.write("### Follows per Talent")
df_follow = df.groupby("talent")["Follows"].sum()

fig, ax = plt.subplots()
ax.pie(df_follow, labels=df_follow.index, autopct="%1.1f%%", colors=sns.color_palette("rainbow", len(df_follow)))
st.pyplot(fig)
