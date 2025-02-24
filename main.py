import pandas as pd
import os

# File paths
driver_file = "data/drivers.xlsx"
user_ratings_file = "data/users_ratings.xlsx"
user_scores_file = "data/users_scores.xlsx"

def load_data(file_path):
    """Loads data from an Excel file, creates an empty one if not found."""
    if os.path.exists(file_path):
        return pd.read_excel(file_path)
    else:
        return pd.DataFrame()

def save_data(df, file_path):
    """Saves DataFrame to an Excel file."""
    df.to_excel(file_path, index=False)

def get_or_create_user(user_id, users_scores_df):
    """Retrieves user score or creates a new user."""
    if user_id not in users_scores_df["user_id"].values:
        new_user = pd.DataFrame({"user_id": [user_id], "user_score": [1.0]})
        users_scores_df = pd.concat([users_scores_df, new_user], ignore_index=True)
        print("New user created.")
    return users_scores_df

def adjust_rating(user_score, given_rating):
    """Adjusts the rating based on user score."""
    adjusted_rating = min(5, max(1, given_rating * user_score))  # Scale within 1-5
    return round(adjusted_rating, 2)

def update_user_score(user_id, users_scores_df, new_score):
    """Updates the user score as a moving average."""
    prev_score = users_scores_df.loc[users_scores_df["user_id"] == user_id, "user_score"].values[0]
    updated_score = (prev_score + new_score) / 2  # Moving average
    users_scores_df.loc[users_scores_df["user_id"] == user_id, "user_score"] = round(updated_score, 2)
    return users_scores_df

def update_driver_rating(driver_id, drivers_df, adjusted_rating):
    """Updates the driver's average rating."""
    if driver_id in drivers_df["driver_id"].values:
        prev_ratings = drivers_df.loc[drivers_df["driver_id"] == driver_id, "rating"].values[0]
        new_rating = (prev_ratings + adjusted_rating) / 2  # Average
        drivers_df.loc[drivers_df["driver_id"] == driver_id, "rating"] = round(new_rating, 2)
    return drivers_df

if __name__ == "__main__":
    # Load datasets
    drivers_df = load_data(driver_file)
    user_ratings_df = load_data(user_ratings_file)
    users_scores_df = load_data(user_scores_file)
    
    # Get user ID
    user_id = int(input("Enter your user ID: "))
    users_scores_df = get_or_create_user(user_id, users_scores_df)
    user_score = users_scores_df.loc[users_scores_df["user_id"] == user_id, "user_score"].values[0]
    
    # Get driver ID and rating
    driver_id = int(input("Enter the driver ID you want to rate: "))
    given_rating = float(input("Enter your rating (1-5): "))
    
    # Adjust the rating based on user score
    adjusted_rating = adjust_rating(user_score, given_rating)
    print(f"Your adjusted rating for driver {driver_id}: {adjusted_rating}")
    
    # Update user ratings
    new_entry = pd.DataFrame({"user_id": [user_id], "driver_id": [driver_id], "given_rating": [given_rating]})
    user_ratings_df = pd.concat([user_ratings_df, new_entry], ignore_index=True)
    
    # Update user score
    users_scores_df = update_user_score(user_id, users_scores_df, given_rating / 5)
    
    # Update driver rating
    drivers_df = update_driver_rating(driver_id, drivers_df, adjusted_rating)
    
    # Save updated data
    save_data(drivers_df, driver_file)
    save_data(user_ratings_df, user_ratings_file)
    save_data(users_scores_df, user_scores_file)
    
    print("Ratings updated successfully!")
