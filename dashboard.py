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

# Load Data dengan Format Datetime yang Benar
df["Publish time"] = pd.to_datetime(df["Publish time"], format="%m/%d/%Y %H:%M")

# Filter hanya untuk "IG reel"
df = df[df["Post type"] == "IG reel"]

# Hapus entri dengan nilai "None"
df = df.replace("None", pd.NA).dropna()

# Buat kolom minggu dan pembagian menjadi 2 periode (2 minggu pertama vs 2 minggu terakhir)
df["Week"] = df["Publish time"].dt.strftime("%Y-%U")  # Format: Year-Week
df["Half"] = df["Week"].rank(method="dense", ascending=True).apply(lambda x: "First 2 Weeks" if x <= 2 else "Last 2 Weeks")

# Tambahkan total interaksi
df["Interactions"] = df["Likes"] + df["Shares"] + df["Comments"] + df["Saves"]

# Filter Data Berdasarkan Talent yang Dipilih
if selected_talent == "All":
    df_filtered = df
else:
    df_filtered = df[df["talent"] == selected_talent]

# Hitung Interaction Rate
df_filtered["Interaction Rate"] = df_filtered["Interactions"] / df_filtered["Views"]

# Grouping untuk 2 minggu pertama vs 2 minggu terakhir
df_grouped_avg = df_filtered.groupby(["Half"])[["Views", "Interaction Rate", "Avg Watch Time (Seconds)"]].mean().reset_index()
df_grouped_total = df_filtered.groupby(["Half"])[["Follows"]].sum().reset_index()  # TOTAL Follows

# --- Visualization ---

# 1. How Many Views and Effective are the CTAs?
st.subheader("1. How Many Views and Effective are the CTAs?")

# Buat layout dua kolom agar Interaction Rate dan Average Views sejajar
col1, col2 = st.columns(2)

with col1:
    st.write("### Interaction Rate")
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.barplot(x="Half", y="Interaction Rate", data=df_grouped_avg, palette="viridis", ax=ax)
    ax.set_ylabel("Interaction Rate")
    ax.set_xlabel("")
    st.pyplot(fig)

with col2:
    st.write("### Average Views")
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.barplot(x="Half", y="Views", data=df_grouped_avg, palette="Blues", ax=ax)
    ax.set_ylabel("Average Views")
    ax.set_xlabel("")
    st.pyplot(fig)

# 2. How Interesting is the Content?
st.subheader("2. How Interesting is the Content for the Audience?")
fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(x="Half", y="Avg Watch Time (Seconds)", data=df_grouped_avg, palette="coolwarm", ax=ax)
ax.set_ylabel("Avg Watch Time (Seconds)")
ax.set_xlabel("")
st.pyplot(fig)

# 3. How Many Follow After Watching Content?
st.subheader("3. How Many Follow After Watching Content?")
fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(x="Half", y="Follows", data=df_grouped_total, palette="magma", ax=ax)
ax.set_ylabel("Total Follows")  # Menampilkan TOTAL Follows, bukan rata-rata
ax.set_xlabel("")
st.pyplot(fig)
