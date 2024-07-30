import os
import re
import random
import requests
from datetime import datetime, timedelta
import math
import config
import person_contract
import person_deposit
import smtplib
import ssl
import json
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import sys


def validate_phone_number(phone_number):
    return re.match(r"^\+|06|86\d{8,14}$", phone_number)


def get_personal_details():
    first_name = input("Enter your first name: ").capitalize().strip()
    last_name = input("Enter your last name: ").capitalize().strip()

    # Validate birth date
    while True:
        birth_date = input("Enter your birth date (yyyy-mm-dd): ").strip()
        if re.match(r"\d{4}-\d{2}-\d{2}", birth_date):
            try:
                birth_date_parsed = datetime.strptime(birth_date, "%Y-%m-%d")
                today = datetime.today()
                age = (today - birth_date_parsed).days // 365
                if age >= 18:
                    break
                else:
                    print("You must be at least 18 years old.")
            except ValueError:
                print("Invalid date format. Please enter a valid date.")
        else:
            print("Invalid date format. Please enter in yyyy-mm-dd format.")

    while True:
        residency_address = input(
            "Enter your residency address (street name and house number, city): "
        ).strip()
        if re.match(r"^[\w\s\.]+,\s*[\w\s]+$", residency_address):
            break
        else:
            print(
                "Invalid address format. Please enter in 'street name and house number, city' format. Example: Puodžių g. 20, Kaunas"
            )

    # Validate phone number
    while True:
        phone_number = input("Enter your phone number: ").strip()
        if validate_phone_number(phone_number):
            break
        else:
            print(
                "Invalid phone number. Please enter a valid phone number that starts with '+', '06', or '86'."
            )

    # Validate email
    while True:
        email = input("Enter your email: ").strip()
        if re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            break
        else:
            print("Invalid email address. Please enter a valid email.")

    return {
        "First name": first_name,
        "Last name": last_name,
        "Birth date": birth_date,
        "Residency Address": residency_address,
        "Phone Number": phone_number,
        "Email": email,
    }


def get_company_details():
    registration_number = input("Enter the company's registration number: ").strip()

    company_name = input("Enter the company's name: ").strip()
    company_address = input("Enter the company's address: ").strip()
    vat_number = input("Enter the VAT number (optional): ").strip()

    # Validate phone number
    while True:
        phone_number = input("Enter the company's phone number: ")
        if validate_phone_number(phone_number):
            break
        else:
            print(
                "Invalid phone number. Please enter a valid phone number that starts with '+', '06', or '86'."
            )

    # Validate email
    while True:
        email = input("Enter the company's email: ")
        if re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            break
        else:
            print("Invalid email address. Please enter a valid email.")

    return {
        "Registration number": registration_number,
        "Company name": company_name,
        "Company address": company_address,
        "VAT number": vat_number,
        "Phone number": phone_number,
        "Email": email,
    }


def get_event_details():
    while True:
        event_date = input("Enter the event date (yyyy-mm-dd): ").strip()
        if re.match(r"\d{4}-\d{2}-\d{2}", event_date):
            try:
                event_date_parsed = datetime.strptime(event_date, "%Y-%m-%d")
                if event_date_parsed > datetime.now():
                    break
                else:
                    print("The event date must be at least the next day from today.")
            except ValueError:
                print("Invalid date format. Please enter a valid date.")
        else:
            print("Invalid date format. Please enter in yyyy-mm-dd format.")

    while True:
        venue = input(
            "Enter the celebration venue (street name and house number, city): "
        ).strip()
        if re.match(r"^[\w\s\.]+,\s*[\w\s]+$", venue):
            break
        else:
            print(
                "Invalid venue format. Please enter in 'street name and house number, city' format. Example: Puodžių g. 20, Kaunas"
            )

    # Extract city
    city = venue.split(",")[-1].strip()
    distance_from_kaunas = 0

    while city.lower() != "kaunas":
        distance_from_kaunas = get_distance_from_kaunas(city)
        if distance_from_kaunas is not None:
            transport_cost = distance_from_kaunas * 0.3
            break
        else:
            print("The city you entered could not be found. Please enter a valid city.")
            while True:
                venue = input(
                    "Enter the celebration venue (street name and house number, city): "
                ).strip()
                if re.match(r"^[\w\s\.]+,\s*[\w\s]+$", venue):
                    break
                else:
                    print(
                        "Invalid venue format. Please enter in 'street name and house number, city' format. Example: Puodžių g. 20, Kaunas"
                    )
            city = venue.split(",")[-1].strip()

    else:
        transport_cost = 0

    # Ask for the number of people
    while True:
        try:
            num_people = int(
                input("Enter the number of people attending (maximum 200): ")
            )
            if 1 <= num_people <= 200:
                break
            else:
                print(
                    "We can not serve that many guests. Please enter a number between 1 and 200."
                )
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
    change_hours = (
        input("Do you want to change the working hours? (yes/no): ").strip().lower()
    )
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
        "Event date": event_date,
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
        "key": api_key,
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["rows"][0]["elements"][0]["status"] == "OK":
            distance_in_meters = data["rows"][0]["elements"][0]["distance"]["value"]
            return distance_in_meters / 1000  # Convert to kilometers
        else:
            print("Error in response:", data["rows"][0]["elements"][0]["status"])
            return None
    else:
        print("Failed to connect to API")
        return None


def confirm_details(details):
    while True:
        # Show the details without num_bartenders, num_barbacks, city, total_cost
        print("\nPlease review your details:")
        filtered_details = {
            k: v
            for k, v in details.items()
            if k
            not in [
                "Number of bartenders",
                "Number of barbacks",
                "City",
                "Total cost",
                "Base cost",
                "Transport cost",
                "Overtime cost",
            ]
        }
        for idx, (key, value) in enumerate(filtered_details.items(), 1):
            print(f"{idx}. {key}: {value}")

        valid = input("\nIs everything correct? (yes/no): ").strip().lower()
        if valid == "yes":
            return True
        elif valid == "no":
            while True:
                try:
                    line_to_change = int(
                        input("Enter the line number you want to change: ")
                    )
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
            if key_to_change in [
                "Event date",
                "Venue",
                "Number of guests",
                "Working hours",
                "Overtime hours",
            ]:
                event_details = get_event_details()
                details.update(event_details)
        else:
            print("Invalid input. Please enter yes or no.")


def send_email(to_email, content, attachment_path1, attachment_path2):
    from_email = config.FROM_EMAIL
    password = config.PASS_EMAIL

    # Create the email header
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = "Event Details and Contract"

    # Attach the email body
    msg.attach(MIMEText(content, "plain"))

    # Attach the first PDF file
    with open(attachment_path1, "rb") as attachment1:
        part1 = MIMEBase("application", "octet-stream")
        part1.set_payload(attachment1.read())

    encoders.encode_base64(part1)
    part1.add_header(
        "Content-Disposition",
        f'attachment; filename="{os.path.basename(attachment_path1)}"',
    )
    msg.attach(part1)

    # Attach the second PDF file
    with open(attachment_path2, "rb") as attachment2:
        part2 = MIMEBase("application", "octet-stream")
        part2.set_payload(attachment2.read())

    encoders.encode_base64(part2)
    part2.add_header(
        "Content-Disposition",
        f'attachment; filename="{os.path.basename(attachment_path2)}"',
    )
    msg.attach(part2)

    # Create SSL context
    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
            print("Contract and invoice sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")


def generate_random_id(existing_ids):
    while True:
        new_id = random.randint(10000, 99999)
        if new_id not in existing_ids:
            return new_id


def save_to_json(details, invoice_number, file_path="user_data.json"):
    if not os.path.exists(file_path):
        existing_ids = set()
    else:
        with open(file_path, "r") as f:
            try:
                data = json.load(f)
                existing_ids = {entry["ID"] for entry in data}
            except (json.JSONDecodeError, KeyError):
                existing_ids = set()

    new_id = generate_random_id(existing_ids)
    details["ID"] = new_id
    details["Invoice Number"] = invoice_number

    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump([details], f, indent=4)
    else:
        with open(file_path, "r+") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
            data.append(details)
            f.seek(0)
            json.dump(data, f, indent=4)


def load_user_data(file_path="user_data.json"):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_user_data(data, file_path="user_data.json"):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def login():
    user_data = load_user_data()
    user_id = input("Enter your ID: ").strip()
    if user_id == config.ADMIN_ID:
        return {"ID": config.ADMIN_ID, "Role": "Admin"}
    for user in user_data:
        if str(user["ID"]) == user_id:
            return user
    print("ID not found. Please try again or register.")
    return None


def register():
    print("Is this a personal celebration or a company's party?")
    print("1. Personal celebration (wedding/birthday/regular party)")
    print("2. Company's party")
    choice = input("Enter 1 or 2: ")

    if choice == "1":
        details = get_personal_details()
    elif choice == "2":
        details = get_company_details()
    else:
        print("Invalid choice.")
        return

    event_details = get_event_details()
    details.update(event_details)

    while not confirm_details(details):
        pass

    print(f"The total cost for the event is: €{details['Total cost']}")

    contract_file = person_contract.generate_contract(details)
    invoice, invoice_number = person_deposit.generate_invoice(details)
    email_content = f"Sveiki,\n\nSiunčiame Jums sugeneruotą mobilaus baro sutartį bei sąskaitą užstato apmokėjimui Jūsų šventei kuri vyks {details['Event date']}.\n\nLinkėjimai,\nMB Double Vision"
    send_email(details["Email"], email_content, contract_file, invoice)

    save_to_json(details, invoice_number)

    print(f"\nYOUR LOGIN ID IS {details['ID']}\n")


def display_menu():
    print("\nMenu:")
    print("1. Sign contract")
    print("2. Pay deposit for event")
    print("3. Select cocktails/change cocktails")
    print("4. View details of personal and event data")
    print("5. Change details of personal and event data")
    print("6. Cancel booking and delete account")
    print("7. Exit")


def handle_menu_choice(user):
    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            print("Sign contract selected.")
            # Implement signing contract
        elif choice == "2":
            print("Pay deposit for event selected.")
            # Implement paying deposit
        elif choice == "3":
            print("Select/change cocktails selected.")
            # Implement selecting/changing cocktails
        elif choice == "4":
            print("View details of personal and event data selected.")
            # Implement viewing details
        elif choice == "5":
            print("Change details of personal and event data selected.")
            # Implement changing details
        elif choice == "6":
            print("Cancel booking and delete account selected.")
            # Implement cancelling booking and deleting account
            return False
        elif choice == "7":
            print("Exiting...")
            return False
        else:
            print("Invalid choice. Please try again.")


def view_all_bookings():
    user_data = load_user_data()
    if not user_data:
        print("No bookings found.")
        return
    for user in user_data:
        print(f"ID: {user['ID']}, Name: {user['First name']} {user['Last name']}")


def view_booking_by_id():
    user_data = load_user_data()
    user_id = input("Enter the booking ID to view: ").strip()
    for user in user_data:
        if str(user["ID"]) == user_id:
            print(json.dumps(user, indent=4))
            return
    print("Booking ID not found.")


def delete_booking():
    user_data = load_user_data()
    user_id = input("Enter the booking ID to delete: ").strip()
    for user in user_data:
        if str(user["ID"]) == user_id:
            user_data.remove(user)
            save_user_data(user_data)
            print("Booking deleted.")
            return
    print("Booking ID not found.")


def change_booking_info():
    user_data = load_user_data()
    user_id = input("Enter the booking ID to change: ").strip()
    for user in user_data:
        if str(user["ID"]) == user_id:
            print("Current booking details:")
            print(json.dumps(user, indent=4))
            # Implement the logic to change booking details here
            print("Feature to change booking info is not yet implemented.")
            return
    print("Booking ID not found.")


def display_admin_menu():
    print("\nAdmin Menu:")
    print("1. View all bookings")
    print("2. See specific booking's info according to ID")
    print("3. Delete a booking/user")
    print("4. Change booking's info")
    print("5. Exit")


def handle_admin_menu_choice():
    while True:
        display_admin_menu()
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            view_all_bookings()
        elif choice == "2":
            view_booking_by_id()
        elif choice == "3":
            delete_booking()
        elif choice == "4":
            change_booking_info()
        elif choice == "5":
            print("Exiting admin menu...")
            return False
        else:
            print("Invalid choice. Please try again.")


def main():
    user = None
    while user is None:
        print("Welcome! Please log in or register to continue.")
        print("1. Log in")
        print("2. Register")
        print("3. Quit")
        choice = input("Enter 1, 2 or 3: ").strip()

        if choice == "1":
            user = login()
        elif choice == "2":
            user = register()
        elif choice == "3":
            print("Exiting program...")
            sys.exit(1)
        else:
            print("Invalid choice. Please enter 1 or 2.")
    if user["ID"] == config.ADMIN_ID:
        handle_admin_menu_choice()
    else:
        print(f"Welcome, {user['First name']} {user['Last name']}!")
        handle_menu_choice(user)


if __name__ == "__main__":
    main()
