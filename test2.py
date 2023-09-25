import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import time

# Function to register a new user
def register_user(username, password):
    # Load user data from the CSV file
    user_data = pd.read_csv('login - Sheet1.csv')

    # Check if the username already exists
    if username in user_data['Username'].values:
        return "Username already exists. Please choose another one."
    else:
        # Add the new user to the DataFrame
        new_user = {'Username': username, 'Password': password}
        user_data = user_data.append(new_user, ignore_index=True)
        
        # Save the updated DataFrame back to the CSV file
        user_data.to_csv('login - Sheet1.csv', index=False)
        return "Registration successful. You can now log in."

# Function to log in a user
def login_user(username, password):
    # Load user data from the CSV file
    user_data_raw = pd.read_csv('login - Sheet1.csv')
    user_data = pd.DataFrame(user_data_raw)

    # Check if the username and password match
    print(user_data)
    # print((user_data['Username'] == username) & (user_data['Password'] == password).any())
    if username in user_data['Username'].values:
        if (user_data.loc[user_data['Username'] == username, 'Password'].values[0]) == password:
            # print("1")
            # return "Login successful. Welcome, " + username + "!"
            return True
        else:
            # return "Password Incorrect"
            # print("2")
            return False
    else:
        # return "Login failed. Please check your credentials."
        # print("3")
        return False


shopping_apps_data_raw = pd.read_csv('movie_data.csv')
shopping_apps_data = shopping_apps_data_raw.head(50)

def display_comparison(data,selected_values):
    st.title('Top Movies Comparison')

    # selected_values = st.multiselect('Select Apps for Comparison', data['movie_title'].unique(), default=data['movie_title'].tolist())

    # Filter the data based on selected apps

    selected_shopping_apps = data[data['movie_title'].isin(selected_values)]
    
    selected_shopping_apps = selected_shopping_apps.sort_values(by='imdb_score', ascending=False)

    # Display the selected shopping apps
    st.write('Selected Movies for Comparison:')
    st.write(selected_shopping_apps)

    # Plot a bar chart for rating comparison
    st.write('### Scores Comparison')
    fig, ax = plt.subplots(figsize=(15, 12))
    # fig, ax = plt.subplots(figsize=(10, 12))
    
    # Adjust the bar width to add space between the bars

    bar_width = 0.4
    bar_positions = np.arange(len(selected_shopping_apps))
    # ax.bar(bar_positions, selected_shopping_apps['imdb_score'], width=bar_width, tick_label=selected_shopping_apps['movie_title'])
    plt.barh(bar_positions, selected_shopping_apps['imdb_score'], height=bar_width, tick_label=selected_shopping_apps['movie_title'], color='skyblue')
    plt.xlabel('IMDB Score')
    plt.ylabel('Movie Title')
    plt.title('Top Movies by IMDB Score')
    plt.yticks(rotation=2, ha='right')
    plt.tight_layout()
    plt.gca().invert_yaxis() 
    
    st.pyplot(fig)

    # Plot a figure for download counts
    st.write('### Voters Counts')
    fig, ax = plt.subplots(figsize=(15, 12))
    ax.plot(selected_shopping_apps['movie_title'], selected_shopping_apps['num_voted_users'], marker='d', ms = 10, mfc = 'r')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)
    # st.empty()

# Streamlit UI
def main():
    st.title("User Registration and Login")

    page = st.sidebar.radio("Select Page", ["Register", "Login"])
    flag = 0

    if page == "Register":
        st.header("Register")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Register"):
            result = register_user(username, password)
            st.write(result)
        # if st.button("Back to Login"):
        #     st.empty()  # Clear the current page
        #     st.sidebar.empty()  # Clear the sidebar
        #     st.sidebar.radio("Select Page", ["Register", "Login"], index=1)  # Switch to the Login page

    elif page == "Login":
        if "selected_values" not in st.session_state:
            st.session_state.selected_values = []
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            result = login_user(username, password)
            # st.write(result)
            if result == True:
               st.write("Welcome, " + username + "!") 
               st.success('Login successful!')
               flag = 1
            #    data = shopping_apps_data
            #    selected_values = st.multiselect('Select for Comparison', data['movie_title'].unique(), default=data['movie_title'].tolist())
            #    st.session_state.selected_values = selected_values  
            #    if len(selected_values) > 0: 
            #     display_comparison(shopping_apps_data,selected_values)
            else:
                flag = 0
                st.write("Login failed. Please check your credentials.")
                st.error('Invalid credentials. Please try again.')
        if flag == 1:
            data = shopping_apps_data
            selected_values = st.multiselect('Select for Comparison', data['movie_title'].unique(), default=data['movie_title'].tolist())
            st.session_state.selected_values = selected_values  
            if len(selected_values) > 0: 
                display_comparison(shopping_apps_data,selected_values)

        # if st.button("Back to Register"):
        #     st.empty()  # Clear the current page
        #     st.sidebar.empty()  # Clear the sidebar
        #     st.sidebar.radio("Select Page", ["Register", "Login"], index=0)  # Switch to the Register page


# Run the app
if __name__ == '__main__':
    main()