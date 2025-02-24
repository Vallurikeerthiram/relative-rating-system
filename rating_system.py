import pandas as pd
import numpy as np
from scipy.stats import beta

class RelativeRatingSystem:
    def __init__(self, driver_file, user_ratings_file, user_scores_file):
        """Initialize the system with existing data."""
        self.driver_file = driver_file
        self.user_ratings_file = user_ratings_file
        self.user_scores_file = user_scores_file

        try:
            self.drivers = pd.read_excel(driver_file)
            self.user_ratings = pd.read_excel(user_ratings_file)
            self.user_scores = pd.read_excel(user_scores_file)
        except Exception as e:
            print(f"Error loading files: {e}")
            raise
        
    def get_user_score(self, user_id):
        """Retrieve user reliability score or initialize if missing."""
        if user_id in self.user_scores['user_id'].values:
            return self.user_scores.loc[self.user_scores['user_id'] == user_id, 'user_score'].values[0]
        else:
            self.user_scores = pd.concat([self.user_scores, pd.DataFrame({'user_id': [user_id], 'user_score': [0.5]})], ignore_index=True)
            return 0.5
    
    def update_user_score(self, user_id, given_rating):
        """Update user score using Bayesian probability based on rating behavior."""
        user_ratings = self.user_ratings[self.user_ratings['user_id'] == user_id]['given_rating']
        total_ratings = len(user_ratings)

        # Using Beta Distribution to model rating tendencies
        alpha = 1 + (user_ratings < 3).sum()  # Count of low ratings
        beta_val = 1 + (user_ratings >= 3).sum()  # Count of high ratings

        # Bayesian probability estimation
        updated_score = beta.mean(alpha, beta_val)
        self.user_scores.loc[self.user_scores['user_id'] == user_id, 'user_score'] = updated_score

    def update_driver_rating(self, driver_id, user_id, given_rating):
        """Update driver rating based on weighted average using user credibility score."""
        if driver_id not in self.drivers['driver_id'].values:
            print("Driver not found!")
            return
        
        user_score = self.get_user_score(user_id)
        driver_data = self.drivers.loc[self.drivers['driver_id'] == driver_id]
        current_rating = driver_data['rating'].values[0]
        num_reviews = self.user_ratings[self.user_ratings['driver_id'] == driver_id].shape[0]

        # Weighted average rating update
        new_rating = ((current_rating * num_reviews) + (given_rating * user_score)) / (num_reviews + 1)
        self.drivers.loc[self.drivers['driver_id'] == driver_id, 'rating'] = round(new_rating, 2)

        # Store the rating in user_ratings
        new_entry = pd.DataFrame({'user_id': [user_id], 'driver_id': [driver_id], 'given_rating': [given_rating]})
        self.user_ratings = pd.concat([self.user_ratings, new_entry], ignore_index=True)

        # Update user score using Bayesian updating
        self.update_user_score(user_id, given_rating)
        
    def save_data(self):
        """Save updated data to Excel files."""
        self.drivers.to_excel(self.driver_file, index=False)
        self.user_ratings.to_excel(self.user_ratings_file, index=False)
        self.user_scores.to_excel(self.user_scores_file, index=False)

    def run(self):
        """Main function to handle user input and update ratings."""
        user_id = int(input("Enter your User ID: "))
        driver_id = int(input("Enter the Driver ID you want to rate: "))
        given_rating = float(input("Enter your rating (1-5): "))
        
        self.update_driver_rating(driver_id, user_id, given_rating)
        self.save_data()
        print("Rating updated successfully!")
