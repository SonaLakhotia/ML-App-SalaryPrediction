import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Performing cleaning for the years of experience, educational level
def exp_clean(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)

def clean_ed(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' or 'Associate degree':
        return 'Post grad'
    return 'Less than Bachelors'


def country_threshold(counts, th):
    th_map = {}  
    for i in range(len(counts)):
        if counts.values[i] >= th:
            th_map[counts.index[i]] = counts.index[i]
        else:
            th_map[counts.index[i]] = 'Other'
    return th_map

def load_explore():
    df  = pd.read_csv('survey_results_public.csv')
    df = df[['EdLevel', 'Employment', 'RemoteWork','YearsCode','DevType','Country','CompTotal','AISent','WorkExp']]
    df = df[df.CompTotal.notnull()]
    df = df.dropna()
    df = df[df.Employment == 'Employed, full-time']
    df = df.drop("Employment", axis=1)
    country_map = country_threshold(df.Country.value_counts(), 350)
    df['Country'] = df.Country.map(country_map)
    df = df[df['CompTotal'] <= 250000]
    df = df[df['CompTotal'] >= 10000]
    df['YearsCode'] = df['YearsCode'].apply(exp_clean)
    df['EdLevel'] = df['EdLevel'].apply(clean_ed)
    return df

df = load_explore()

def show_explore_page():
    st.title("Explore Salaries")
    data1 = df['Country'].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(data1, labels= data1.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")
    st.write("### Data from different countries ###")
    st.pyplot(fig1)


    st.write("### Mean Salaries based on Countries ###")
    data2 = df.groupby(['Country'])['CompTotal'].mean()
    st.bar_chart(data2)

    st.write("### Mean based on Work Experience ###")
    data3 = df.groupby(['WorkExp'])['CompTotal'].mean()
    st.line_chart(data3)

