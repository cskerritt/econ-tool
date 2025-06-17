# Authentication Setup for Economic Tool

## Overview
The Economic Tool now includes user authentication using `streamlit-authenticator`. Users must sign in before accessing the application.

## Default Login Credentials

| Username | Password | Role |
|----------|----------|------|
| admin    | admin123 | Administrator |
| user1    | user123  | Economic Analyst |
| demo     | demo123  | Demo User |

## Files Added

1. **`auth.py`** - Authentication module with login/logout functionality
2. **`config.yaml`** - User credentials and authentication configuration
3. **`generate_passwords.py`** - Script to generate secure password hashes
4. **Updated `requirements.txt`** - Added authentication dependencies

## How It Works

1. When users visit the application, they see a login form
2. After successful authentication, users are welcomed by name
3. A logout button appears in the sidebar
4. User session is maintained with secure cookies

## Customizing Users

To add/modify users:

1. Edit the `config.yaml` file to add new users
2. Run `python generate_passwords.py` to hash the passwords
3. Restart the Streamlit application

## Security Features

- Passwords are hashed using bcrypt
- Session cookies with configurable expiration
- Logout functionality
- User session management

## Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Generate password hashes (if needed)
python generate_passwords.py

# Run the application
streamlit run econtool.py
```

## Changing Default Passwords

**Important**: Change the default passwords before deploying to production!

1. Edit the passwords in `generate_passwords.py`
2. Run the script to update hashes
3. Or manually edit `config.yaml` with new bcrypt hashes
