import re
import requests
from datetime import datetime
import config  # Import the configuration file
import math  # Import math for ceiling function

def validate_phone_number(phone_number):
    return re.match(r'^\+|06|86\d{8,14}$', phone_number)

def get_personal_details():
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")

    # Validate birth date
    while True:
        birth_date = input("Enter your birth date (yyyy-mm-dd): ")
        if re.match(r'\d{4}-\d{2}-\d{2}', birth_date):
            try:
                datetime.strptime(birth_date, '%Y-%m-%d')
                break
            except ValueError:
                print("Invalid date format. Please enter a valid date.")
        else:
            print("Invalid date format. Please enter in yyyy-mm-dd format.")

    residency_address = input("Enter your residency address: ")

    # Validate phone number
    while True:
        phone_number = input("Enter your phone number: ")
        if validate_phone_number(phone_number):
            break
        else:
            print("Invalid phone number. Please enter a valid phone number that starts with '+', '06', or '86'.")

    # Validate email
    while True:
        email = input("Enter your email: ")
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            break
        else:
            print("Invalid email address. Please enter a valid email.")

    return {
        "First name": first_name,
        "Last name": last_name,
        "Birth date": birth_date,
        "Residency Address": residency_address,
        "Phone Number": phone_number,
        "Email": email
    }

def get_company_details():
    registration_number = input("Enter the company's registration number: ")

    company_name = input("Enter the company's name: ")
    company_address = input("Enter the company's address: ")
    vat_number = input("Enter the VAT number (optional): ")

    # Validate phone number
    while True:
        phone_number = input("Enter the company's phone number: ")
        if validate_phone_number(phone_number):
            break
        else:
            print("Invalid phone number. Please enter a valid phone number that starts with '+', '06', or '86'.")

    # Validate email
    while True:
        email = input("Enter the company's email: ")
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            break
        else:
            print("Invalid email address. Please enter a valid email.")

    return {
        "Registration number": registration_number,
        "Company name": company_name,
        "Company address": company_address,
        "VAT number": vat_number,
        "Phone number": phone_number,
        "Email": email
    }

def get_event_details():
    while True:
        venue = input("Enter the celebration venue (street name and house number, city): ")
        if re.match(r'^[\w\s\.]+,\s*[\w\s]+$', venue):
            break
        else:
            print("Invalid venue format. Please enter in 'street name and house number, city' format.")

    # Extract city
    city = venue.split(",")[-1].strip()
    distance_from_kaunas = 0

    if city.lower() != "kaunas":
        distance_from_kaunas = get_distance_from_kaunas(city)
        transport_cost = distance_from_kaunas * 0.3
    else:
        transport_cost = 0

    # Ask for the number of people
    while True:
        try:
            num_people = int(input("Enter the number of people attending: "))
            break
        except ValueError:
            print("Invalid number. Please enter a valid number.")

    # Calculate bartenders and barback needed
    num_barback = 0
    if num_people <= 60:
        num_bartenders = 2
        base_cost = 650
    elif num_people <= 80:
        num_bartenders = 3
        base_cost = 800
    elif num_people <= 120:
        num_bartenders = 4
        base_cost = 1050
    else:
        num_bartenders = 4
        num_barback = 1
        base_cost = 1400

    working_hours = "17:00-01:00"
    change_hours = input("Do you want to change the working hours? (yes/no): ").strip().lower()
    if change_hours == "yes":
        working_hours = input("Enter the new working hours (e.g., 18:00-02:00): ")

    overtime_hours = 0
    if input("Do you want overtime? (yes/no): ").strip().lower() == "yes":
        while True:
            try:
                overtime_hours = int(input("Enter the number of overtime hours: "))
                break
            except ValueError:
                print("Invalid number. Please enter a valid number.")

    overtime_cost = overtime_hours * (50 * num_bartenders + (40 if num_barback else 0))

    total_cost = math.ceil(base_cost + transport_cost + overtime_cost)

    return {
        "Venue": venue,
        "Number of guests": num_people,
        "Number of bartenders": num_bartenders,
        "Number of barbacks": num_barback,
        "Working hours": working_hours,
        "Overtime hours": overtime_hours,
        "Total cost": total_cost,
        "City": city,
        "Base cost": base_cost,
        "Transport cost": transport_cost,
        "Overtime cost": overtime_cost,
    }

def get_distance_from_kaunas(city):
    api_key = config.DISTANCE_MATRIX_API_KEY
    base_url = "https://api.distancematrix.ai/maps/api/distancematrix/json"
    params = {
        "origins": "Kaunas",
        "destinations": city,
        "departure_time": "now",
        "units": "metric",
        "key": api_key
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['rows'][0]['elements'][0]['status'] == 'OK':
            distance_in_meters = data['rows'][0]['elements'][0]['distance']['value']
            return distance_in_meters / 1000  # Convert to kilometers
        else:
            print("Error in response:", data['rows'][0]['elements'][0]['status'])
            return None
    else:
        print("Failed to connect to API")
        return None

def confirm_details(details):
    while True:
        # Show the details without num_bartenders, num_barbacks, city, total_cost
        print("\nPlease review your details:")
        filtered_details = {k: v for k, v in details.items() if k not in ["Number of bartenders", "Number of barbacks", "City", "Total cost", "Base cost", "Transport cost", "Overtime cost"]}
        for idx, (key, value) in enumerate(filtered_details.items(), 1):
            print(f"{idx}. {key}: {value}")

        valid = input("\nIs everything correct? (yes/no): ").strip().lower()
        if valid == "yes":
            return True
        elif valid == "no":
            while True:
                try:
                    line_to_change = int(input("Enter the line number you want to change: "))
                    if 1 <= line_to_change <= len(filtered_details):
                        break
                    else:
                        print("Invalid line number.")
                except ValueError:
                    print("Invalid input. Please enter a valid line number.")

            key_to_change = list(filtered_details.keys())[line_to_change - 1]
            new_value = input(f"Enter new value for {key_to_change}: ")
            details[key_to_change] = new_value

            # Recalculate costs if any relevant detail was changed
            if key_to_change in ["Venue", "Number of guests", "Working hours", "Overtime hours"]:
                event_details = get_event_details()
                details.update(event_details)
        else:
            print("Invalid input. Please enter yes or no.")

def main():
    print("Is this a personal celebration or a company's party?")
    print("1. Personal celebration (wedding/birthday/regular party)")
    print("2. Company's party")
    choice = input("Enter 1 or 2: ")

    if choice == '1':
        details = get_personal_details()
    elif choice == '2':
        details = get_company_details()
    else:
        print("Invalid choice.")
        return

    event_details = get_event_details()
    details.update(event_details)

    while not confirm_details(details):
        pass

    print(f"The total cost for the event is: €{details['Total cost']}")

if __name__ == "__main__":
    main()
