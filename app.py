import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Job Analyst Dashboard", layout="wide")
st.title("💼 Job Analyst Internship Dashboard")

# 2. Load Dataset
@st.cache_data
def load_data():
    df = pd.read_csv('your_dataset.csv')
    if 'Posting Date' in df.columns:
        df['Posting Date'] = pd.to_datetime(df['Posting Date'], errors='coerce')
    return df

try:
    df_raw = load_data()
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# Static Lists for geo-filtering helper metrics
asian_countries = ['India', 'China', 'Japan', 'South Korea', 'Pakistan', 'Bangladesh', 'Indonesia', 'Malaysia', 'Philippines', 'Vietnam', 'Thailand']
african_countries = ['Nigeria', 'Egypt', 'South Africa', 'Kenya', 'Ethiopia', 'Ghana', 'Morocco', 'Algeria', 'Uganda', 'Tanzania']

# --- TASK 1: India vs Germany Job Comparison ---
st.header("1. India vs Germany Job Comparison")

df1 = df_raw.copy()
df1 = df1[
    (df1['Country'].isin(['India', 'Germany'])) &
    (df1['Qualification'] == 'B.Tech') &
    (df1['Work Type'] == 'Full-Time') &
    (df1['Experience'] > 2) &
    (df1['Job Title'].isin(['Data Scientist', 'Art Teacher', 'Aerospace Engineer'])) &
    (df1['Salary'] > 10000) &
    (df1['Portal'].str.lower() == 'indeed') &
    (df1['Company Name'].str.len() > 8) &
    (df1['Location'].notna()) & (df1['Location'] != '')
]

if not df1.empty:
    fig1 = px.bar(
        df1, x="Job Title", color="Country", 
        title="Job Postings Comparison: India vs Germany",
        barmode="stack", color_discrete_map={'India': '#1f77b4', 'Germany': '#ff7f0e'}
    )
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.warning("No records matched the filter criteria for India vs Germany Job Comparison.")


# --- TASK 2: Top 10 Companies ---
st.header("2. Top 10 Companies Hiring")

df2 = df_raw.copy()
def ends_with_vowel(name):
    return str(name).lower().strip()[-1] in ['a', 'e', 'i', 'o', 'u'] if pd.notna(name) else False

df2 = df2[
    (df2['Role'] == 'Data Engineer') & 
    (df2['Job Title'] == 'Data Scientist') &
    (~df2['Country'].isin(asian_countries)) &
    (~df2['Country'].str.startswith('C', na=False)) &
    (df2['Company Size'] >= 10000) &
    (df2['Qualification'] == 'B.Tech') &
    (df2['Preference'].str.lower() == 'female') &
    (df2['Posting Date'] >= '2023-01-01') & (df2['Posting Date'] <= '2023-06-01') &
    (df2['Contact Person'].apply(ends_with_vowel))
]

if not df2.empty:
    top_companies = df2['Company Name'].value_counts().head(10).reset_index()
    top_companies.columns = ['Company Name', 'Count']
    fig2 = px.treemap(
        top_companies, path=['Company Name'], values='Count',
        title="Top 10 Companies Hiring (Data Scientist / Data Engineer Roles)"
    )
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("No data found matching the exact criteria for Top 10 Companies.")


# --- TASK 3: Preference vs Work Type ---
st.header("3. Preference vs Work Type Distribution")

df3 = df_raw.copy()
df3 = df3[
    (df3['Work Type'] == 'Intern') &
    (df3['Company Size'] < 50000) &
    (df3['Salary'] > 9000)
]

if not df3.empty:
    pref_counts = df3['Preference'].value_counts().reset_index()
    pref_counts.columns = ['Preference', 'Count']
    pref_counts = pref_counts.sort_values(by='Count', ascending=False)
    
    fig3 = px.bar(
        pref_counts, x='Preference', y='Count',
        title="Preference Distribution Across Internships",
        text_auto=True
    )
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.warning("No records matched the filter criteria for Preference vs Work Type.")


# --- TASK 4: Company Size vs Company Name ---
st.header("4. Company Size vs Company Name Scatter Plot")

df4 = df_raw.copy()
def count_vowels(text):
    return sum(1 for char in str(text).lower() if char in 'aeiou')

df4 = df4[
    (df4['Company Size'] < 50000) &
    (df4['Job Title'] == 'Mechanical Engineer') &
    (df4['Experience'] > 5) &
    (df4['Salary'] > 50000) &
    (df4['Work Type'].isin(['Full-Time', 'Part-Time'])) &
    (df4['Preference'].str.lower() == 'male') &
    (df4['Country'].isin(asian_countries)) &
    (~df4['Country'].str.startswith('I', na=False)) &
    (df4['Portal'].str.lower() == 'idealist') &
    (df4['Company Name'].apply(lambda x: count_vowels(x) >= 2))
]

if not df4.empty:
    fig4 = px.scatter(
        df4, x='Company Name', y='Company Size', size='Salary', color='Country',
        title="Scatter Plot: Company Size vs Company Name (Mechanical Engineers)"
    )
    st.plotly_chart(fig4, use_container_width=True)
else:
    st.warning("No records matched the filters for Company Size vs Company Name.")


# --- TASK 5: Work Type Salary Distribution ---
st.header("5. Internship Salary Distribution")

df5 = df_raw.copy()
df5 = df5[
    (df5['Work Type'] == 'Intern') &
    (df5['Latitude'] < 10) &
    (df5['Company Size'] < 50000) &
    (df5['Salary'] > 8000) &
    (df5['Job Title'].str.split().apply(len) == 1) &
    (df5['Job Title'].str.len() < 10) &
    (df5['Experience'] % 2 == 0) &
    (df5['Posting Date'].dt.year.between(2021, 2023)) &
    (df5['Contact Person'].str.lower().str.contains('e', na=False))
]

if not df5.empty:
    fig5 = px.box(
        df5, y='Salary', points="all",
        title="Box-and-Whisker Distribution: Internship Salaries"
    )
    st.plotly_chart(fig5, use_container_width=True)
else:
    st.warning("No records matched the target metrics for Internship Salary Distribution.")


# --- TASK 6: Qualification Drilldown Map ---
st.header("6. African Region Qualification Drilldown Map")

df6 = df_raw.copy()
df6 = df6[
    (df6['Country'].isin(african_countries)) &
    (df6['Qualification'].isin(['B.Tech', 'M.Tech', 'PhD'])) &
    (df6['Work Type'] == 'Full-Time') &
    (df6['Job Title'].str.startswith('D', na=False)) &
    (df6['Preference'].str.lower() == 'male') &
    (df6['Company Size'] > 80000) &
    (df6['Salary'] > 20000) &
    (df6['Contact Person'].str.startswith('A', na=False)) &
    (df6['Portal'].str.lower() == 'indeed')
]

if not df6.empty and 'Latitude' in df6.columns and 'Longitude' in df6.columns:
    fig6 = px.scatter_geo(
        df6, lat='Latitude', lon='Longitude',
        hover_name='Location', color='Qualification', size='Salary',
        projection="natural earth", title="African Job Postings Drilldown Map"
    )
    st.plotly_chart(fig6, use_container_width=True)
else:
    st.warning("No spatial or filtered records exist matching the requested parameters.")