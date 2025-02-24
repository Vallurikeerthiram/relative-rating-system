import pandas as pd
import numpy as np
from scipy.stats import beta  # Using beta distribution for Bayesian updates

class RelativeRatingSystem:
    def __init__(self, driver_file, user_ratings_file, user_scores_file):
        """Initialize the system with existing data."""
        self.driver_file = driver_file
        self.user_ratings_file = user_ratings_file
        self.user_scores_file = user_scores_file
        
        # Load data with error handling
        try:
            self.drivers = pd.read_excel(driver_file)
            self.user_ratings = pd.read_excel(user_ratings_file)
            self.user_scores = pd.read_excel(user_scores_file)
        except FileNotFoundError:
            print("One or more data files missing. Initializing empty data.")
            self.drivers = pd.DataFrame(columns=['driver_id', 'name', 'rating'])
            self.user_ratings = pd.DataFrame(columns=['user_id', 'driver_id', 'rating'])
            self.user_scores = pd.DataFrame(columns=['user_id', 'score'])
        
        self.K = 32  # Elo rating factor
        self.alpha = 0.2  # EMA smoothing factor
    
    def get_user_score(self, user_id):
        """Retrieve or initialize user reliability score."""
        if user_id in self.user_scores['user_id'].values:
            return self.user_scores.loc[self.user_scores['user_id'] == user_id, 'score'].values[0]
        else:
            new_entry = pd.DataFrame({'user_id': [user_id], 'score': [0.5]})
            self.user_scores = pd.concat([self.user_scores, new_entry], ignore_index=True)
            return 0.5
    
    def update_user_score(self, user_id, given_rating):
        """Update user score using Bayesian updating based on rating behavior."""
        user_ratings = self.user_ratings[self.user_ratings['user_id'] == user_id]['rating']
        total_ratings = len(user_ratings)

        # Using Beta Distribution to model rating tendencies
        alpha = 1 + (user_ratings < 3).sum()  # Count of low ratings
        beta_val = 1 + (user_ratings >= 3).sum()  # Count of high ratings

        # Bayesian probability estimation
        updated_score = beta.mean(alpha, beta_val)
        self.user_scores.loc[self.user_scores['user_id'] == user_id, 'score'] = round(updated_score, 2)
    
    def elo_adjustment(self, old_rating, user_score, given_rating):
        """Elo-based rating adjustment with user credibility."""
        expected = 1 / (1 + 10 ** ((old_rating - given_rating) / 400))
        new_rating = old_rating + self.K * user_score * (given_rating - expected)
        return round(min(5, max(1, new_rating)), 2)  # Keep within 1-5 scale
    
    def update_driver_rating(self, driver_id, user_id, given_rating):
        """Update driver rating with Elo and Exponential Moving Average (EMA)."""
        if driver_id not in self.drivers['driver_id'].values:
            print("Driver not found! Adding new driver with default rating 3.0.")
            new_driver = pd.DataFrame({'driver_id': [driver_id], 'name': [f"Driver_{driver_id}"], 'rating': [3.0]})
            self.drivers = pd.concat([self.drivers, new_driver], ignore_index=True)

        user_score = self.get_user_score(user_id)
        current_rating = self.drivers.loc[self.drivers['driver_id'] == driver_id, 'rating'].values[0]

        # Apply Elo adjustment
        adjusted_rating = self.elo_adjustment(current_rating, user_score, given_rating)

        # Apply EMA for smooth rating updates
        new_rating = (adjusted_rating * self.alpha) + (current_rating * (1 - self.alpha))
        self.drivers.loc[self.drivers['driver_id'] == driver_id, 'rating'] = round(new_rating, 2)

        # Store the rating in user_ratings
        new_entry = pd.DataFrame({'user_id': [user_id], 'driver_id': [driver_id], 'rating': [given_rating]})
        self.user_ratings = pd.concat([self.user_ratings, new_entry], ignore_index=True)

        # Update user credibility score using Bayesian updating
        self.update_user_score(user_id, given_rating)
    
    def save_data(self):
        """Save updated data to Excel files."""
        self.drivers.to_excel(self.driver_file, index=False)
        self.user_ratings.to_excel(self.user_ratings_file, index=False)
        self.user_scores.to_excel(self.user_scores_file, index=False)
    
    def run(self):
        """CLI function to handle user input and update ratings."""
        try:
            user_id = int(input("Enter your User ID: "))
            driver_id = int(input("Enter the Driver ID you want to rate: "))
            given_rating = float(input("Enter your rating (1-5): "))

            if not (1 <= given_rating <= 5):
                print("Invalid rating! Please enter a value between 1 and 5.")
                return

            self.update_driver_rating(driver_id, user_id, given_rating)
            self.save_data()
            print("Rating updated successfully!")

        except ValueError:
            print("Invalid input. Please enter numeric values for IDs and ratings.")

# Example Usage
if __name__ == "__main__":
    system = RelativeRatingSystem("data/drivers.xlsx", "data/user_ratings.xlsx", "data/user_scores.xlsx")
    system.run()
