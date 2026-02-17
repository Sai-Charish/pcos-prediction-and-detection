import streamlit as st
import joblib
import pandas as pd
import hashlib
import os



# Load the trained models
xgb_model = joblib.load('./FRONTEND/best_xgb_model.pkl')
lr_model = joblib.load('./FRONTEND/best_lr_model.pkl')



# User database file
USER_DB = "users.csv"

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to check if the user exists
def load_users():
    if not os.path.exists(USER_DB):
        return pd.DataFrame(columns=["Username", "Password"])
    return pd.read_csv(USER_DB)

# Function to save a new user
def save_user(username, password):
    users = load_users()
    if username in users["Username"].values:
        return False  # User already exists
    new_user = pd.DataFrame([[username, hash_password(password)]], columns=["Username", "Password"])
    users = pd.concat([users, new_user], ignore_index=True)
    users.to_csv(USER_DB, index=False)
    return True

# Function to authenticate users
def authenticate(username, password):
    users = load_users()
    if username in users["Username"].values:
        stored_password = users.loc[users["Username"] == username, "Password"].values[0]
        return stored_password == hash_password(password)
    return False



# Function for login page with registration option
def login_page():
    st.title("PCOS Detection and Prediction System")
    st.write("Please log in or register to continue.")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:  # Login tab
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if authenticate(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome, {username}!")
            else:
                st.error("Invalid credentials, please try again.")

    with tab2:  # Registration tab
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        if st.button("Register"):
            if new_password != confirm_password:
                st.error("Passwords do not match!")
            elif save_user(new_username, new_password):
                st.success("Registration successful! You can now log in.")
            else:
                st.error("Username already exists. Please choose another.")

# Home page content
def home_page():
    st.title("PCOS Information")
    st.write("""
        **Polycystic Ovary Syndrome (PCOS)** is a condition that affects women's hormone levels. 
        It is a common endocrine disorder affecting up to 1 in 10 women of reproductive age. PCOS can cause a variety of symptoms that affect fertility, menstrual cycles, and overall health.
        """)

    # Use columns for better organization
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("""
        ## Symptoms of PCOS
        Women with PCOS may experience the following symptoms:
        - **Irregular periods** or absence of periods.
        - **Excessive hair growth** (hirsutism) on the face, chest, or back.
        - **Acne** and oily skin.
        - **Thinning hair** or male-pattern baldness.
        - **Weight gain**, especially around the abdomen.
        - **Darkening of the skin** (e.g., in the neck or underarms).
        - **Infertility** or difficulty in getting pregnant.
        """)

    with col2:
        # You can use PNG images for representation (replace with actual paths)
        st.image('data:image/jpeg;base64,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', caption="PCOS Symptoms")
        #st.image('path_to_your_image/pcos_image_2.png', caption="PCOS Diagnosis")

    st.write("""
        ## Causes of PCOS
        The exact cause of PCOS is still not fully understood, but several factors may contribute to its development:
        - **Genetics**: PCOS tends to run in families, indicating a genetic link.
        - **Hormonal Imbalance**: Women with PCOS have an imbalance in hormones like higher levels of androgens (male hormones) and insulin.
        - **Insulin Resistance**: Many women with PCOS have insulin resistance, meaning their body cannot use insulin effectively, which can lead to weight gain and difficulty losing weight.

        ## Diagnosis of PCOS
        To diagnose PCOS, doctors typically use a combination of the following:
        - **Medical history and symptoms**: Doctors will review menstrual cycles, weight changes, and other symptoms.
        - **Physical Exam**: This may include checking for excess hair growth and acne.
        - **Ultrasound**: A pelvic ultrasound may show cysts on the ovaries, which is a common feature of PCOS.
        - **Blood tests**: These tests help assess hormone levels, including androgen levels, and check for diabetes or cholesterol problems.

        ## Treatment Options
        While there is no cure for PCOS, treatment can help manage symptoms and prevent long-term complications:
        - **Medications for menstrual regulation**: Birth control pills or progestin can help regulate periods.
        - **Medications for hair growth**: Anti-androgen medications, like spironolactone, can reduce excessive hair growth.
        - **Fertility treatments**: For women struggling with fertility, medications like Clomid or assisted reproductive technologies (ART) may be recommended.
        - **Lifestyle changes**: Regular exercise, a healthy diet, and weight management can help manage insulin resistance and improve symptoms.

        ## Prevention and Lifestyle Changes
        While you cannot prevent PCOS, adopting a healthy lifestyle can help you manage its symptoms:
        - **Maintain a healthy weight**: Losing even a small amount of weight can help regulate insulin levels and restore menstrual cycles.
        - **Exercise regularly**: Physical activity helps manage insulin resistance and reduces the risk of diabetes.
        - **Eat a balanced diet**: A diet rich in whole grains, vegetables, lean proteins, and healthy fats can help manage weight and insulin levels.
        - **Stress management**: Stress can exacerbate symptoms, so practicing relaxation techniques like yoga or meditation may be helpful.
        """)

    # Second row of columns for further information
    col1, col2 = st.columns(2)

    with col1:
        st.write("""
        ## Impact on Health
        PCOS can affect not only fertility but also increase the risk of developing other health issues like **type 2 diabetes**, **high blood pressure**, **heart disease**, and **endometrial cancer**.
        It's important for women with PCOS to have regular check-ups to monitor their health and prevent complications.
        """)

    with col2:
        # Example of another image for impact on health
        st.image('https://www.researchgate.net/publication/361687194/figure/fig2/AS:11431281080411458@1661307141661/The-risk-factors-of-polycystic-ovary-syndrome-PCOS.png', caption="Health Impact of PCOS")

    st.write("""
        ## How the Prediction System Helps
        This system uses machine learning models to predict the likelihood of PCOS based on key indicators. By analyzing various factors such as follicle count, hormonal levels, and lifestyle choices, it helps you assess your risk for PCOS.
        """)

    col1, col2 = st.columns(2)

    with col1:
        st.write("""
        ## Key Statistics:
        - Approximately **5-10%** of women of reproductive age have PCOS.
        - PCOS is one of the leading causes of **infertility** in women.
        - Studies show that **50-70%** of women with PCOS have insulin resistance, even if they are not overweight.
        """)

    with col2:
        # Example of another image (replace with actual path)
        st.image('https://typeset-prod-media-server.s3.amazonaws.com/article_uploads/d32e41f7-755a-4120-9d1a-6e926254554b/image/005ed608-abf7-4189-92d7-1a5b82b051fb-uimage.png', caption="PCOS Statistics")

    st.write(""" 
    ## Further Resources
    - [PCOS Awareness Association.](https://www.pcosaa.org/)
    """)

    



# Prediction page content
def prediction_page():
    
    st.title("PCOS Prediction")
    
    # Collect user inputs
    col1, col2 = st.columns(2)
    
    with col1:
        follicle_no_r = st.number_input('Follicle No. (Right)', min_value=0.0, max_value=20.0, step=1.0)
        follicle_no_l = st.number_input('Follicle No. (Left)', min_value=0.0, max_value=22.0, step=1.0)
        hair_growth = st.selectbox('Hair Growth (Yes/No)', ['Yes', 'No'])
        skin_darkening = st.selectbox('Skin Darkening (Yes/No)', ['Yes', 'No'])
        weight_gain = st.selectbox('Weight Gain (Yes/No)', ['Yes', 'No'])

    with col2:
        amh = st.number_input('Anti-Müllerian hormone(AMH)(ng/mL)', min_value=0.0, max_value=32.0, step=0.1)
        fast_food = st.selectbox('Fast Food (Yes/No)', ['Yes', 'No'])
        cycle_length = st.number_input('Cycle Length (days)', min_value=0, max_value=60, step=1)
        cycle_type = st.number_input('Cycle Type (R/I)', min_value=2.0, max_value=5.0)
        fsh_lh = st.number_input('FSH/LH', min_value=0.0,max_value=30.0, step=0.1)

    # Convert inputs to a DataFrame
    input_data = {
        'Follicle No. (R)': follicle_no_r,
        'Follicle No. (L)': follicle_no_l,
        'hair growth(Y/N)': 1 if hair_growth == 'Yes' else 0,
        'Skin darkening (Y/N)': 1 if skin_darkening == 'Yes' else 0,
        'Weight gain(Y/N)': 1 if weight_gain == 'Yes' else 0,
        'AMH(ng/mL)': amh,
        'Fast food (Y/N)': 1 if fast_food == 'Yes' else 0,
        'Cycle length(days)': cycle_length,
        'Cycle(R/I)': 1 if cycle_type == 'R' else 0,
        'FSH/LH': fsh_lh
    }

    # Convert the scaled data to DataFrame
    input_df = pd.DataFrame([input_data])

    # Dropdown for selecting model
    model_choice = st.selectbox('Select Model', ['XGBoost', 'Logistic Regression'])
    
    # Prediction button
    if st.button("Predict"):
        if model_choice == 'XGBoost':
            model = xgb_model
        else:
            model = lr_model
        
        # Make prediction
        prediction = model.predict(input_df)[0]
        
        if prediction == 1:
            st.error("You may have been diagnosed with PCOS.")
            st.success(''' Suggestions : \n
                     \nFood Choices:

✔ Eat more veggies, whole grains, nuts, and lean proteins (chicken, fish, eggs).  
✔ Choose healthy fats like avocados, olive oil, and seeds.  
✔ Drink more water and green tea.
                       
Exercise:
                     
✔ Walk, jog, or dance for 30 minutes most days.  
✔ Lift light weights or do bodyweight exercises (squats, push-ups).  
✔ Try yoga or stretching to reduce stress.  

Lifestyle Tips:
                     
✔ Sleep 7-9 hours every night.  
✔ Reduce stress—listen to music, meditate, or take deep breaths.  
✔ Stay active—take the stairs, walk after meals.''')
        else:
            st.success("You seem to be safe (no PCOS symptoms detected).")
            

# Main function to control page flow
def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        login_page()
    else:
        st.sidebar.subheader(f"Welcome {st.session_state.username}")
        page = st.sidebar.selectbox("Select Page", ["Home", "Prediction"])
        
        
        if page == "Home":
            home_page()
        elif page == "Prediction":
            prediction_page()

if __name__ == "__main__":
    main()
