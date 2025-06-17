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
    Check if user is authenticated and handle login/logout
    Returns True if authenticated, False otherwise
    """
    
    # Initialize authenticator
    authenticator, config = initialize_authenticator()
    
    # Create login widget
    try:
        authenticator.login()
    except Exception as e:
        st.error(e)
        return False

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
