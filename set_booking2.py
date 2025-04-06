import random
import string
import sqlite3

class SeatBookingSystem:
    def __init__(self):
        # Initialize the seat map and the bookings dictionary
        self.seat_map = self.create_seat_map()
        self.bookings = {}  # Dictionary to store booking information with booking reference as key
        # Establish a database connection to store and retrieve bookings
        self.db_connection = self.connect_db()
        # Load bookings from the database into the system
        self.load_bookings_from_db()

    def connect_db(self):
        # Connect to the SQLite database (it will create the database if it doesn't exist)
        conn = sqlite3.connect("seat_booking.db")
        return conn

    def load_bookings_from_db(self):
        # Load the booking information from the database into the system
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM bookings")  # Query all records from the bookings table
        rows = cursor.fetchall()  # Fetch all rows of the result
        
        # Loop through each booking and store it in the in-memory dictionary
        for row in rows:
            reference, passport, first_name, last_name, seat_row, seat_column = row
            seat_id = f"{seat_row}{seat_column}"
            # Load the booking details into memory
            self.bookings[reference] = {
                'passport_number': passport,
                'first_name': first_name,
                'last_name': last_name,
                'seat_row': seat_row,
                'seat_column': seat_column
            }
            # Update the seat status as 'R' (reserved)
            self.seat_map[seat_id] = 'R'  # Mark the seat as reserved

    # Create a seat map to represent the seating arrangement
    def create_seat_map(self):
        seat_map = {}
        rows = 80  # Total rows
        cols = ['A', 'B', 'C', 'D', 'E', 'F']  # Seat columns
        # Iterate through rows and columns to create seat IDs and initial seat statuses
        for row in range(1, rows + 1):
            for col in cols:
                seat_id = f"{row}{col}"
                if col in ['D', 'E', 'F'] and row in [77, 78]:
                    seat_map[seat_id] = 'S'  # 'S' for storage area (seats in 77, 78 rows, columns D, E, F)
                else:
                    seat_map[seat_id] = 'F'  # 'F' for free seats
        # Insert aisle seats in between rows
        for row in range(1, rows + 1):
            seat_map[f"{row}X"] = 'X'  # 'X' represents the aisle
        return seat_map

    # Generate a unique booking reference
    def generate_booking_reference(self):
        while True:
            # Generate a random 8-character alphanumeric string as the booking reference
            reference = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            # Ensure the reference is unique
            if reference not in self.bookings:
                return reference

    # Book a seat for a customer
    def book_seat(self):
        seat = input("Enter seat number to book (e.g., 15C): ").upper()
        # Check if the seat number is valid
        if seat not in self.seat_map:
            print("Invalid seat number.")
        # If the seat is available (free)
        elif self.seat_map[seat] == 'F':
            # Generate a booking reference for the seat
            booking_reference = self.generate_booking_reference()
            print(f"Generated booking reference: {booking_reference}")
            # Collect customer information
            passport_number = input("Enter passport number: ")
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            
            # Store the booking information in the in-memory dictionary
            self.bookings[booking_reference] = {
                'passport_number': passport_number,
                'first_name': first_name,
                'last_name': last_name,
                'seat_row': seat[0:2],
                'seat_column': seat[2:]
            }

            # Mark the seat as reserved in the seat map
            self.seat_map[seat] = 'R'  # 'R' represents a reserved seat
            # Save the booking details to the database
            self.save_booking_to_db(booking_reference, passport_number, first_name, last_name, seat)
            print(f"Seat {seat} booked successfully with reference {booking_reference}.")
        else:
            print("This seat is not available.")  # If the seat is already reserved or unavailable

    # Save the booking information to the database
    def save_booking_to_db(self, reference, passport, first_name, last_name, seat):
        cursor = self.db_connection.cursor()
        # Create the bookings table if it does not exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS bookings 
                        (reference TEXT PRIMARY KEY, passport TEXT, first_name TEXT, 
                         last_name TEXT, seat_row TEXT, seat_column TEXT)''')
        # Insert the booking record into the database
        cursor.execute('''INSERT INTO bookings (reference, passport, first_name, last_name, seat_row, seat_column)
                          VALUES (?, ?, ?, ?, ?, ?)''', 
                          (reference, passport, first_name, last_name, seat[0:2], seat[2:]))
        self.db_connection.commit()

    # Free a previously booked seat
    def free_seat(self):
        seat = input("Enter seat number to free (e.g., 15C): ").upper()
        # Check if the seat exists and is already reserved
        if seat not in self.seat_map:
            print("Invalid seat number.")
        elif self.seat_map[seat] == 'R':  # If the seat is reserved
            booking_reference = self.get_booking_reference_by_seat(seat)
            self.seat_map[seat] = 'F'  # Mark the seat as free
            # Remove the booking from the in-memory dictionary
            del self.bookings[booking_reference]
            # Delete the booking record from the database
            self.delete_booking_from_db(booking_reference)
            print(f"Seat {seat} has been freed.")
        else:
            print("Seat is already free.")  # If the seat is not reserved

    # Get the booking reference associated with a seat
    def get_booking_reference_by_seat(self, seat):
        for ref, booking in self.bookings.items():
            if booking['seat_row'] + booking['seat_column'] == seat:
                return ref
        return None  # If no booking found

    # Delete the booking record from the database
    def delete_booking_from_db(self, reference):
        cursor = self.db_connection.cursor()
        cursor.execute('''DELETE FROM bookings WHERE reference = ?''', (reference,))
        self.db_connection.commit()

    # Display the status of all seats
    def show_booking_status(self):
        print("\n--- Booking Status ---")
        header = "    "
        for col in ['A', 'B', 'C', ' ', 'D', 'E', 'F']:
            header += f"{col} "
        print(header)
        
        # Display each row and column with the corresponding seat status
        for row in range(1, 81):
            line = f"{row:02d}: "
            for col in ['A', 'B', 'C', 'X', 'D', 'E', 'F']:
                seat = f"{row}{col}"
                if seat in self.seat_map:
                    status = self.seat_map[seat]
                    # If the seat is reserved, display 'R' instead of the booking reference
                    if status != 'F' and status != 'S' and status != 'X':
                        status = 'R'
                    line += f"{status} "
            print(line)
        print("----------------------\n")

# Main menu loop to interact with the user
def main_menu():
    booking_system = SeatBookingSystem()

    while True:
        print("=== Apache Airlines Seat Booking System ===")
        print("1. Check availability of seat")
        print("2. Book a seat")
        print("3. Free a seat")
        print("4. Show booking status")
        print("5. Exit program")
        print("6. Book multiple seats")

        choice = input("Enter your choice (1-6): ")

        # Handle user choices for seat booking operations
        if choice == '1':
            booking_system.check_availability()
        elif choice == '2':
            booking_system.book_seat()
        elif choice == '3':
            booking_system.free_seat()
        elif choice == '4':
            booking_system.show_booking_status()
        elif choice == '6':
            booking_system.book_multiple_seats()
        elif choice == '5':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid option. Please select 1-6.")

# Entry point of the program
if __name__ == "__main__":
    main_menu()
