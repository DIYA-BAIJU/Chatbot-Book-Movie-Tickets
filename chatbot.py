import re

class MovieTicketBookingBot:
    def __init__(self, movie_file='movies.txt'):
        self.movie_file = movie_file
        self.movies = self.load_movies()
        self.booked_tickets = []

    def load_movies(self):
        movies = {}
        try:
            with open(self.movie_file, 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    movie_name = parts[0]
                    showtimes = parts[1:-1]
                    seats = set(parts[-1].replace('seats:', '').split())
                    movies[movie_name.lower()] = {'showtimes': showtimes, 'seats': seats}
            return movies
        except FileNotFoundError:
            print("⚠️ Movie file not found. Please make sure 'movies.txt' exists in the directory.")
            return {}

    def update_seats_file(self):
        with open(self.movie_file, 'w') as file:
            for movie, details in self.movies.items():
                showtimes = ','.join(details['showtimes'])
                seats = ' '.join(details['seats'])
                file.write(f"{movie},{showtimes},seats:{seats}\n")

    def greet_user(self):
        print("🎬 Movie Ticket Booking Bot: Hello! Welcome to the movie ticket booking system.")
        print("🎬 Movie Ticket Booking Bot: You can type 'exit' at any time to leave.")

    def show_movies(self):
        print("\n🎬 Movies available for booking:")
        movie_names = list(self.movies.keys())
        for idx, movie in enumerate(movie_names, start=1):
            print(f"{idx}. {movie.title()}")
        return movie_names

    def show_showtimes(self, movie):
        print(f"\n🎬 Showtimes for {movie.title()}:")
        showtimes = self.movies[movie]['showtimes']
        for idx, time in enumerate(showtimes, start=1):
            print(f"{idx}. {time}")
        return showtimes

    def select_seat_type(self):
        seat_types = ["Balcony", "Regular", "Premium"]
        print("\n🎬 Available Seat Types:")
        for idx, seat in enumerate(seat_types, start=1):
            print(f"{idx}. {seat}")
        while True:
            try:
                seat_choice = int(input("🎬 Enter the number for your preferred seat type: ").strip())
                if 1 <= seat_choice <= len(seat_types):
                    selected_seat_type = seat_types[seat_choice - 1]
                    print(f"🎬 You selected Seat Type: {selected_seat_type}")
                    return selected_seat_type
                else:
                    print("⚠️ Invalid choice. Please select a valid seat type.")
            except ValueError:
                print("⚠️ Invalid input. Please enter a number corresponding to your choice.")

    def select_ticket_count(self):
        while True:
            try:
                count = int(input("🎬 Enter the number of tickets you'd like to book: ").strip())
                if count > 0:
                    print(f"🎬 You selected Ticket Count: {count}")
                    return count
                else:
                    print("⚠️ Please enter a positive number.")
            except ValueError:
                print("⚠️ Invalid input. Please enter a valid number.")

    def select_seats(self, movie, ticket_count):
        available_seats = self.movies[movie]['seats']
        print("\n🎬 Available Seats:", ' '.join(sorted(available_seats)))

        selected_seats = []
        while len(selected_seats) < ticket_count:
            seat = input(f"🎬 Select seat {len(selected_seats) + 1} (e.g., A1, B2): ").strip().upper()
            if seat in available_seats:
                selected_seats.append(seat)
                available_seats.remove(seat)
                print(f"🎬 You selected Seat: {seat}")
            else:
                print("⚠️ Seat unavailable or already booked. Please choose another seat.")

        self.update_seats_file()  # Update the file after seats selection
        return selected_seats

    def book_ticket(self, movie, time, seat_type, seats, ticket_count):
        ticket = {
            "movie": movie.title(),
            "time": time,
            "seat_type": seat_type,
            "seats": ', '.join(seats),
            "count": ticket_count
        }
        self.booked_tickets.append(ticket)
        print("\n🎬 Booking confirmed! Ticket details are below.")

    def show_ticket_summary(self):
        print("\n🎟️ Your Ticket Summary:")
        for ticket in self.booked_tickets:
            print("\n--------------------------------")
            print("| Movie:", ticket['movie'])
            print("| Showtime:", ticket['time'])
            print("| Seat Type:", ticket['seat_type'])
            print("| Seats:", ticket['seats'])
            print("| Ticket Count:", ticket['count'])
            print("--------------------------------")
        print("Thankyou for choosing PoPmOvies for booking your show!\n")
    def run(self):
        self.greet_user()

        while True:
            movies = self.show_movies()
            user_input = input("🎬 Enter the number of the movie you'd like to book: ").strip()

            if user_input.lower() == 'exit':
                print("🎬 Movie Ticket Booking Bot: Thank you for using the booking system. Goodbye!")
                break

            try:
                movie_choice = int(user_input) - 1
                if movie_choice < 0 or movie_choice >= len(movies):
                    print("⚠️ Invalid choice. Please select a valid number from the movie list.")
                    continue
                selected_movie = movies[movie_choice]
                print(f"🎬 You selected Movie: {selected_movie.title()}")

                showtimes = self.show_showtimes(selected_movie)
                time_input = input("🎬 Enter the number of the showtime you want to book: ").strip()
                time_choice = int(time_input) - 1

                if time_choice < 0 or time_choice >= len(showtimes):
                    print("⚠️ Invalid choice. Please select a valid showtime number.")
                    continue
                selected_showtime = showtimes[time_choice]
                print(f"🎬 You selected Showtime: {selected_showtime}")

                seat_type = self.select_seat_type()
                ticket_count = self.select_ticket_count()
                seats = self.select_seats(selected_movie, ticket_count)

                # Show final confirmation
                print("\n🎬 Please review your booking:")
                print(f"🎬 Movie: {selected_movie.title()}")
                print(f"🎬 Showtime: {selected_showtime}")
                print(f"🎬 Seat Type: {seat_type}")
                print(f"🎬 Seats: {', '.join(seats)}")
                print(f"🎬 Ticket Count: {ticket_count}")

                confirm = input("🎬 Do you confirm this booking? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    self.book_ticket(selected_movie, selected_showtime, seat_type, seats, ticket_count)
                    self.show_ticket_summary()
                else:
                    print("🎬 Booking cancelled. You can start a new booking if you want.")

                continue_booking = input("\n🎬 Would you like to book another ticket? (yes/no): ").strip().lower()
                if continue_booking != 'yes':
                    print("🎬 Movie Ticket Booking Bot: Thank you for using the booking system. Goodbye!")
                    break

            except ValueError:
                print("⚠️ Invalid input. Please enter a number corresponding to your choice.")

# Run the Movie Ticket Booking Bot
if __name__ == "__main__":
    bot = MovieTicketBookingBot()
    bot.run()
