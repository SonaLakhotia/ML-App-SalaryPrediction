import pickle
import streamlit as st
import numpy as np

def load_model():
    with open('saved_model.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()
model_loaded = data['model']
l_edlevel = data['l_edlevel']
l_remote = data['l_remote']
l_years = data['l_years']
l_DevType = data['l_DevType']
l_Country = data['l_Country']
l_AISent = data['l_AISent']

def show_predict_page():
    st.title("Salary Predictions")
    st.write("### We need some information to predict the salary ###")

    countries = ('United States of America', 'Other', 'Germany',
                 'United Kingdom of Great Britain and Northern Ireland', 'India',
                 'Canada', 'Brazil', 'France', 'Spain', 'Australia', 'Netherlands',
                 'Sweden', 'Poland', 'Italy', 'Israel', 'Switzerland', 'Portugal',
                 'Norway', 'Turkey', 'Austria', 'Denmark', 'Finland', 'South Africa',
                 'Mexico', 'New Zealand', 'Colombia', 'Czech Republic', 'Belgium',
                 'Pakistan', 'Ukraine', 'Romania')
    education = ('Bachelor’s degree', 'Post grad', 'Master’s degree')
    devType = ('Senior Executive (C-Suite, VP, etc.)', 'Developer, back-end',
               'Developer, full-stack', 'Developer, QA or test',
               'Developer, front-end', 'System administrator',
               'Developer, mobile',
               'Developer, desktop or enterprise applications',
               'Data scientist or machine learning specialist',
               'Other (please specify):', 'Database administrator',
               'Engineer, site reliability', 'Cloud infrastructure engineer',
               'Academic researcher',
               'Developer, embedded applications or devices',
               'Engineering manager', 'DevOps specialist',
               'Research & Development role', 'Blockchain', 'Developer Advocate',
               'Product manager', 'Data or business analyst', 'Project manager',
               'Engineer, data', 'Security professional', 'Developer Experience',
               'Developer, game or graphics', 'Scientist', 'Hardware Engineer',
               'Designer', 'Student', 'Educator',
               'Marketing or sales professional')
    remote = ('Remote', 'Hybrid (some remote, some in-person)', 'In-person')
    aiSent = ('Indifferent', 'Favorable', 'Unfavorable', 'Very favorable',
              'Unsure', 'Very unfavorable')

    country = st.selectbox("Country", countries)
    edu = st.selectbox("Education level", education)
    dev_type = st.selectbox("Role Type", devType)
    experience = st.slider("Years of Experience", 0, 50, 3)
    years_code = st.slider("Coding experience", 0, 50, 3)
    working = st.selectbox("Remote", remote)
    aiuse = st.selectbox("AI usage in work", aiSent)

    ok = st.button("Predict Salary")
    if ok:
        # Form the input array
        X_data = np.array([[country, edu, dev_type, experience, years_code, working, aiuse]])

        # Transform the categorical features using the fitted LabelEncoders
        X_data[:, 0] = l_Country.transform(X_data[:, 0])
        X_data[:, 1] = l_edlevel.transform(X_data[:, 1])
        X_data[:, 2] = l_DevType.transform(X_data[:, 2])
        X_data[:, 5] = l_remote.transform(X_data[:, 5])
        X_data[:, 6] = l_AISent.transform(X_data[:, 6])

        # Ensure the numeric features are correctly typed
        X_data[:, 3] = X_data[:, 3].astype(float)
        X_data[:, 4] = X_data[:, 4].astype(float)
        X_data = X_data.astype(float)

        # Make prediction
        salary = model_loaded.predict(X_data)
        st.subheader(f"The predicted salary is ${salary[0]:.2f}")
