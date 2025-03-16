import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page title and layout
st.set_page_config(page_title="Content Performance Dashboard", layout="wide")

df = pd.read_excel("ig_data.xlsx", sheet_name="bi-weekly")

# Sidebar
with st.sidebar:
    st.image("Marketing.png")
    st.write("### Select Talent:")
    talents = ["All"] + sorted(df["talent"].dropna().unique().tolist())
    selected_talent = st.selectbox("", talents)

    st.markdown("[LinkedIn](https://www.linkedin.com/in/ihza-zhafran-010a0b21a/)")
    st.markdown("[GitHub](https://github.com/zrihza)")
    st.write("\n\nCopyright © Ihza Zhafran")
    
    
# Load Data
df["Publish time"] = pd.to_datetime(df["Publish time"], format="%d/%m/%Y %H:%M")
df["Week"] = df["Publish time"].dt.strftime("%Y-%U")  # Format: Year-Week
df["Half"] = df["Week"].rank(method="dense", ascending=True).apply(lambda x: "First 2 Weeks" if x <= 2 else "Last 2 Weeks")

# Tambahkan total interaksi
df["Interactions"] = df["Likes"] + df["Shares"] + df["Comments"] + df["Saves"]

# Filter Data Berdasarkan Talent yang Dipilih
if selected_talent == "All":
    df_filtered = df
else:
    df_filtered = df[df["talent"] == selected_talent]

# Grouping untuk perbandingan 2 minggu pertama vs 2 minggu terakhir
df_grouped = df_filtered.groupby(["Half"])[["Views", "Interactions", "Avg Watch Time (Seconds)", "Follows"]].mean().reset_index()

# --- Visualization ---

# 1. How Effective is CTA?
st.subheader("1. How Effective is CTA?")
fig, ax = plt.subplots(figsize=(8, 4))
df_grouped.plot(x="Half", y=["Views", "Interactions"], kind="bar", ax=ax, color=["#1f77b4", "#ff7f0e"])
plt.xticks(rotation=0)
plt.ylabel("Count")
st.pyplot(fig)

# 2. How Interesting is the Content?
st.subheader("2. How Interesting is the Content for the Audience?")
fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(x="Half", y="Avg Watch Time (Seconds)", data=df_grouped, palette="viridis", ax=ax)
plt.xticks(rotation=0)
st.pyplot(fig)

# 3. How Many Follow After Watching Content?
st.subheader("3. How Many Follow After Watching Content?")
fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(x="Half", y="Follows", data=df_grouped, palette="coolwarm", ax=ax)
plt.xticks(rotation=0)
st.pyplot(fig)
