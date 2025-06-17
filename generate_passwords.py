#!/usr/bin/env python3
"""
Script to generate hashed passwords for the authentication config.
Run this script to generate proper bcrypt hashes for your passwords.
"""

import bcrypt
import yaml

def hash_password(password: str) -> str:
    """Generate a bcrypt hash for a password."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def update_config_with_hashed_passwords():
    """Update the config.yaml file with properly hashed passwords."""
    
    # Default passwords - change these as needed
    passwords = {
        'admin': 'admin123',
        'user1': 'user123', 
        'demo': 'demo123'
    }
    
    print("Generating password hashes...")
    
    # Load existing config
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    # Update passwords with proper hashes
    for username, password in passwords.items():
        if username in config['credentials']['usernames']:
            hashed = hash_password(password)
            config['credentials']['usernames'][username]['password'] = hashed
            print(f"Updated password for {username}")
    
    # Write back to file
    with open('config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)
    
    print("\nConfig file updated with hashed passwords!")
    print("Default login credentials:")
    for username, password in passwords.items():
        print(f"  Username: {username}, Password: {password}")

if __name__ == "__main__":
    update_config_with_hashed_passwords()
