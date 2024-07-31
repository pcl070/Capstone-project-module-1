# 1830 Mobile Bar Booking System

<p align="center">
  <img src="logo.png" alt="1830 Bar Logo" width="100"/>
</p>

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Dependencies](#dependencies)
- [Configuration](#configuration)


## Description
1830 Mobile Bar Booking System is a Python-based application that allows users to register for personal events, manage their bookings, sign contracts, and pay deposits. The system also includes an admin interface for managing all bookings.

## Features
- User registration for personal events
- Event details management
- Contract generation and email notification
- Invoice generation and email notification
- Admin interface for managing bookings
- User data persistence in JSON format

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/pcl070/Capstone-project-module-1.git
   cd Capstone-project-module-1
   ```
## Set up a virtual environment and install dependencies:


```bash
python -m venv venv
source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```
## Place the following required files in the project directory:
```bash
DejaVuSans.ttf
DejaVuSans-Bold.ttf
logo.png
```

## Create a config.py file with the following content:

```bash
FROM_EMAIL = 'your-email@gmail.com'
PASS_EMAIL = 'your-email-password'
ADMIN_ID = 'your-admin-id'
DISTANCE_MATRIX_API_KEY = 'your-api-key'
```
## Usage
1. **Run the application**
    ```bash
    python bar_1830.py
    ```

2. **Follow the prompts**
    - **Login/Register**: Choose to login or register as a new user.
    - **User Menu**: Once logged in, users can manage their event details, sign contracts, and pay deposits.
    - **Admin Menu**: Admins can view all bookings, view specific booking details, delete bookings, and change booking details.

## Follow the on-screen instructions to log in, register, and manage bookings.

### File Structure
```bash
1830-mobile-bar/
│
├── bar_1830.py           # Main application file
├── config.py             # Configuration file
├── person_contract.py    # Contract generation module
├── person_deposit.py     # Invoice generation module
├── DejaVuSans.ttf        # Font file
├── DejaVuSans-Bold.ttf   # Font file
├── logo.png              # Logo image
├── user_data.json        # User data storage
└── requirements.txt      # List of dependencies

```

## Dependencies
```bash
Python 3.6+
reportlab
requests
num2words
email
ssl
smtplib
```
## Install dependencies via pip:

```bash
pip install -r requirements.txt
```
## Configuration
Update the config.py file with your own email credentials and API key for the Google Distance Matrix API.
