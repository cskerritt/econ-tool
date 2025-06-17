# Authentication Setup for Economic Tool

## Overview
The Economic Tool now includes comprehensive user authentication using `streamlit-authenticator`. Users can register new accounts, sign in, reset passwords, and manage their profiles.

## Default Login Credentials

| Username | Password | Role |
|----------|----------|------|
| admin    | admin123 | Administrator |
| user1    | user123  | Economic Analyst |
| demo     | demo123  | Demo User |

## Files Added

1. **`auth.py`** - Authentication module with login/logout/registration functionality
2. **`config.yaml`** - User credentials and authentication configuration
3. **`generate_passwords.py`** - Script to generate secure password hashes
4. **Updated `requirements.txt`** - Added authentication dependencies

## Features

### Login & Registration
1. **Login Tab**: Existing users can sign in with username/password
2. **Register Tab**: New users can create accounts (no pre-authorization required)
3. **Forgot Password Tab**: Users can reset forgotten passwords
4. User session is maintained with secure cookies

### User Account Management
Once logged in, users can access account settings in the sidebar:
1. **Reset Password**: Change current password
2. **Update Details**: Modify name and email address

## User Registration Process

### For New Users
1. Visit the application
2. Click on the "Register" tab
3. Fill in the registration form:
   - Username (must be unique)
   - Name (display name)
   - Email address
   - Password
4. Click "Register user"
5. Switch to "Login" tab and sign in with new credentials

### For Administrators
To manually add users or modify existing ones:
1. Edit the `config.yaml` file to add new users
2. Run `python generate_passwords.py` to hash the passwords
3. Restart the Streamlit application

## Security Features

- Passwords are hashed using bcrypt
- Session cookies with configurable expiration
- User registration with automatic config updates
- Password reset functionality
- Forgot password with random password generation
- User profile management
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
