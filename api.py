from fastapi import FastAPI, HTTPException
import pandas as pd
from rating_system import RelativeRatingSystem

app = FastAPI()

# Initialize the rating system
rating_system = RelativeRatingSystem("data/drivers.xlsx", "data/users_ratings.xlsx", "data/users_scores.xlsx")

@app.post("/rate/")
def rate_driver(user_id: int, driver_id: int, rating: float):
    """API endpoint to submit a rating."""
    if rating < 1 or rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5.")

    rating_system.update_driver_rating(driver_id, user_id, rating)
    rating_system.save_data()
    
    return {"message": "Rating submitted successfully!"}

@app.get("/drivers/{driver_id}")
def get_driver_rating(driver_id: int):
    """API endpoint to get a driver's rating."""
    if driver_id not in rating_system.drivers['driver_id'].values:
        raise HTTPException(status_code=404, detail="Driver not found.")

    rating = rating_system.drivers.loc[rating_system.drivers['driver_id'] == driver_id, 'rating'].values[0]
    return {"driver_id": driver_id, "rating": rating}

@app.get("/users/{user_id}/user_score")
def get_user_score(user_id: int):
    """API endpoint to get a user's credibility score."""
    score = rating_system.get_user_score(user_id)
    return {"user_id": user_id, "score": score}
