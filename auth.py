"""
Authentication module for the Economic Tool
Provides login/logout functionality using streamlit-authenticator
"""

import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os

def load_config():
    """Load authentication configuration from config.yaml"""
    config_path = 'config.yaml'
    if not os.path.exists(config_path):
        st.error("Authentication configuration file not found. Please run generate_passwords.py first.")
        st.stop()

    with open(config_path) as file:
        config = yaml.load(file, Loader=SafeLoader)
    return config

def save_config(config):
    """Save authentication configuration to config.yaml"""
    config_path = 'config.yaml'
    with open(config_path, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

def initialize_authenticator():
    """Initialize the streamlit authenticator"""
    config = load_config()

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )

    return authenticator, config

def check_authentication():
    """
    Check if user is authenticated and handle login/logout/registration
    Returns True if authenticated, False otherwise
    """

    # Initialize authenticator
    authenticator, config = initialize_authenticator()

    # Create tabs for Login, Register, and Forgot Password
    tab1, tab2, tab3 = st.tabs(["Login", "Register", "Forgot Password"])

    with tab1:
        # Create login widget
        try:
            authenticator.login()
        except Exception as e:
            st.error(e)
            return False

    with tab2:
        # Create registration widget
        try:
            if authenticator.register_user('Register user', preauthorization=False):
                st.success('User registered successfully! Please go to the Login tab to sign in.')
                # Save the updated config with new user
                save_config(config)
        except Exception as e:
            st.error(e)

    with tab3:
        # Create forgot password widget
        try:
            username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password('Forgot password')
            if username_forgot_pw:
                st.success('New password generated successfully!')
                st.info(f'Your new password is: **{random_password}**')
                st.warning('Please save this password and change it after logging in.')
                # Save the updated config with new password
                save_config(config)
            elif username_forgot_pw == False:
                st.error('Username not found')
        except Exception as e:
            st.error(e)

    # Get authentication status from session state
    name = st.session_state.get('name')
    authentication_status = st.session_state.get('authentication_status')
    username = st.session_state.get('username')

    if authentication_status == False:
        st.error('Username/password is incorrect')
        return False
    elif authentication_status == None:
        st.warning('Please enter your username and password')
        return False
    elif authentication_status:
        # User is authenticated

        # Create logout button in sidebar
        with st.sidebar:
            st.write(f'Welcome *{name}*')
            authenticator.logout(location='sidebar')
            st.markdown("---")

        # Store user info in session state for use in main app
        st.session_state['user_name'] = name
        st.session_state['username'] = username
        st.session_state['authenticated'] = True

        return True

    return False

def get_current_user():
    """Get current authenticated user information"""
    return {
        'name': st.session_state.get('user_name', ''),
        'username': st.session_state.get('username', ''),
        'authenticated': st.session_state.get('authenticated', False)
    }

def show_password_reset():
    """Show password reset widget for authenticated users"""
    authenticator, config = initialize_authenticator()
    username = st.session_state.get('username')

    if username:
        try:
            if authenticator.reset_password(username, 'Reset password'):
                st.success('Password modified successfully')
                # Save the updated config
                save_config(config)
        except Exception as e:
            st.error(e)

def show_update_user_details():
    """Show update user details widget for authenticated users"""
    authenticator, config = initialize_authenticator()
    username = st.session_state.get('username')

    if username:
        try:
            if authenticator.update_user_details(username, 'Update user details'):
                st.success('User details updated successfully')
                # Save the updated config
                save_config(config)
        except Exception as e:
            st.error(e)

def require_authentication(func):
    """
    Decorator to require authentication for a function
    Usage: @require_authentication
    """
    def wrapper(*args, **kwargs):
        if check_authentication():
            return func(*args, **kwargs)
        else:
            st.stop()
    return wrapper
