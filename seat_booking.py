class SeatBookingSystem:
    # Initialize seat map
    def __init__(self):
        self.seat_map = self.create_seat_map()

    # Create seat map
    def create_seat_map(self):
        seat_map = {}
        rows = 80
        cols = ['A', 'B', 'C', 'D', 'E', 'F']
        for row in range(1, rows + 1):
            for col in cols:
                seat_id = f"{row}{col}"
                if col in ['D', 'E', 'F'] and row in [77, 78]:
                    seat_map[seat_id] = 'S'  # DEF in rows 77,78 is a storage area.
                else:
                    seat_map[seat_id] = 'F'  # Other seats are empty
        # Insertion of aisles
        for row in range(1, rows + 1):
            seat_map[f"{row}X"] = 'X'  # Aisle
        return seat_map

    # Check seat availability
    def check_availability(self):
        seat = input("Enter seat number to check (e.g., 12A): ").upper()
        status = self.seat_map.get(seat)
        if status is None:
            print("Invalid seat number.")
        elif status == 'F':
            print(f"Seat {seat} is available.")
        elif status == 'R':
            print(f"Seat {seat} is already reserved.")
        elif status in ['X', 'S']:
            print(f"Seat {seat} cannot be booked (Aisle or Storage).")

    # Book a seat
    def book_seat(self):
        seat = input("Enter seat number to book (e.g., 15C): ").upper()
        if seat not in self.seat_map:
            print("Invalid seat number.")
        elif self.seat_map[seat] == 'F':
            self.seat_map[seat] = 'R'
            print(f"Seat {seat} booked successfully.")
        elif self.seat_map[seat] == 'R':
            print("Seat already booked.")
        elif self.seat_map[seat] in ['X', 'S']:
            print("This seat cannot be booked.")

    # Free a seat
    def free_seat(self):
        seat = input("Enter seat number to free (e.g., 15C): ").upper()
        if seat not in self.seat_map:
            print("Invalid seat number.")
        elif self.seat_map[seat] == 'R':
            self.seat_map[seat] = 'F'
            print(f"Seat {seat} has been freed.")
        elif self.seat_map[seat] == 'F':
            print("Seat is already free.")
        elif self.seat_map[seat] in ['X', 'S']:
            print("This seat cannot be changed.")

    # Display all seat statuses
    def show_booking_status(self):
        print("\n--- Booking Status ---")
        # Output column headings (exclude aisle columns)
        header = "    "  # For alignment
        for col in ['A', 'B', 'C',' ', 'D', 'E', 'F']:
            header += f"{col} "
        print(header)
        
        # Output each row of seat status
        for row in range(1, 81):
            line = f"{row:02d}: "
            for col in ['A', 'B', 'C', 'X', 'D', 'E', 'F']:
                seat = f"{row}{col}"
                if seat in self.seat_map:
                    line += f"{self.seat_map[seat]} "
            print(line)
        print("----------------------\n")

    # Book multiple seats
    def book_multiple_seats(self):
        seats_input = input("Enter seat numbers separated by commas (e.g., 12A, 12B, 12C): ")
        seats = [seat.strip().upper() for seat in seats_input.split(",")]

        all_valid = True
        for seat in seats:
            if seat not in self.seat_map:
                print(f"{seat} is invalid.")
                all_valid = False
            elif self.seat_map[seat] != 'F':
                print(f"{seat} is not available.")
                all_valid = False

        if all_valid:
            for seat in seats:
                self.seat_map[seat] = 'R'
            print("All seats booked successfully!")
        else:
            print("Group booking failed. Please check seat availability and try again.")

# Main menu cycle
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

# Entrance to the program
if __name__ == "__main__":
    main_menu()
