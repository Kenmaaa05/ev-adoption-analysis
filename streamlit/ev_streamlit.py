import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import requests

st.set_page_config(page_title="EV Adoption in Washington", layout="wide")
st.title("⚡ Electric Vehicle Adoption in Washington State, USA")

#  Load Data 
@st.cache_data
def load_data():
    df = pd.read_csv('https://raw.githubusercontent.com/Kenmaaa05/ev-adoption-analysis/main/outputs/cleaned_ev.csv')
    return df

ev = load_data()

#  Filters 
st.sidebar.header("Filters")

# EV Type
ev_type_options = ev["electric_vehicle_type"].unique()
ev_type_filter = st.sidebar.multiselect("EV Type", ev_type_options)

# CAFV
cafv_options = ev["clean_alternative_fuel_vehicle_(cafv)_eligibility"].unique()
cafv_filter = st.sidebar.multiselect("CAFV Eligibility", cafv_options)

# Urban/Rural
urban_options = ev["if_urban"].unique()
urban_filter = st.sidebar.multiselect("Urban/Rural", urban_options)

#  Apply Filters if Selected 
ev_filtered = ev.copy()

if ev_type_filter:
    ev_filtered = ev_filtered[ev_filtered["electric_vehicle_type"].isin(ev_type_filter)]

if cafv_filter:
    ev_filtered = ev_filtered[ev_filtered["clean_alternative_fuel_vehicle_(cafv)_eligibility"].isin(cafv_filter)]

if urban_filter:
    ev_filtered = ev_filtered[ev_filtered["if_urban"].isin(urban_filter)]

#  PDF 
st.markdown("### 📄 EV Dashboard (PDF Preview)")

pdf_url = "https://raw.githubusercontent.com/Kenmaaa05/ev-adoption-analysis/main/outputs/ev_dashboard.pdf"
response = requests.get(pdf_url)

if response.status_code == 200:
    base64_pdf = base64.b64encode(response.content).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
else:
    st.error("Failed to load PDF from GitHub.")
#  Dataset Overview 
st.header("📊 Dataset Overview")
st.write(f"Total Vehicles: **{len(ev_filtered):,}**")
st.dataframe(ev_filtered, use_container_width=True)

#  Missing Values Summary (Post-Cleaning) 
st.subheader("🧹 Missing Value Summary (Post-Cleaning)")
missing = ev_filtered.isna().sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(10, 4))
sns.barplot(x=missing.index, y=missing.values, ax=ax, palette="coolwarm")
plt.xticks(rotation=90)
plt.title("Remaining Missing Values After Cleaning")
plt.ylabel("Count")
st.pyplot(fig)

#  Electric Range Distribution 
st.subheader("📈 Electric Range Distribution")
fig, ax = plt.subplots(figsize=(8, 4))
ev_filtered['electric_range'].hist(bins=50, color="mediumseagreen", edgecolor="black", ax=ax)
plt.title("Electric Range Distribution")
plt.xlabel("Range (miles)")
plt.ylabel("Frequency")
st.pyplot(fig)

#  Range Category Bar Plot 
st.subheader("🪫 Range Category Breakdown")
range_order = ['Low', 'Medium', 'High', 'Very High', 'Unknown']
fig, ax = plt.subplots(figsize=(6, 4))
ev_filtered['range_category'].value_counts().reindex(range_order).plot(kind='bar', color='dodgerblue', ax=ax)
plt.title("EVs by Electric Range Category")
plt.ylabel("Number of Vehicles")
st.pyplot(fig)

#  Urban vs Rural Count 
st.subheader("🌐 Urban vs Rural EV Adoption")
fig, ax = plt.subplots(figsize=(5, 3))
ev_filtered['if_urban'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax, colors=["lightcoral", "skyblue"])
ax.axis('equal')
plt.title("Urban vs Rural Classification")
st.pyplot(fig)

#  Manufacturer Trends 
st.subheader("🚗 Top Manufacturers")
top_makes = ev_filtered['make'].value_counts().head(10)
fig, ax = plt.subplots(figsize=(6, 4))
top_makes.plot(kind='barh', ax=ax, color='goldenrod')
plt.xlabel("Number of Registered EVs")
plt.title("Top 10 EV Manufacturers")
st.pyplot(fig)

#  CAFV Eligibility 
st.subheader("✅ CAFV Eligibility")
fig, ax = plt.subplots(figsize=(5, 3))
ev_filtered['clean_alternative_fuel_vehicle_(cafv)_eligibility'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, ax=ax, colors=['lightgreen', 'orange', 'salmon'])
plt.title("CAFV Eligibility Breakdown")
ax.axis('equal')
st.pyplot(fig)

#  Footer 
st.markdown("---")
st.caption("Data Source: [Data.gov - Electric Vehicle Population](https://catalog.data.gov/dataset/electric-vehicle-population-data) • Created by Kenmaaa")

