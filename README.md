# Relative Rating System

A probability-based rating system that dynamically adjusts ratings based on user credibility and historical data.

## Features
- **Relative Rating Calculation:** Adjusts ratings based on user reliability.
- **Historical Data Usage:** Uses past ratings to refine future ratings.
- **Automated User Management:** Creates and updates users dynamically.
- **Excel-Based Storage:** Stores and updates data efficiently.
- **Open Source & Extensible:** Can be integrated into larger systems.

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Vallurikeerthiram/relative-rating-system.git
cd relative-rating-system
```
### 2. Set Up a Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
## How to Use
### Run the program:
```bash
python main.py  #for running main
uvicorn api:app --reload --log-level debug #for api

```
- Enter your User ID (If not found, it will create a new one).
- Enter the Driver ID you are rating.
- Provide a rating (1-5) → The system will adjust it based on your past ratings.
- The driver's rating and your user credibility score will be updated!

## Project Structure
```bash
relative-rating-system/
├── data/                 # Stores all rating data
│   ├── users_ratings.xlsx  
│   ├── users_scores.xlsx  
│   ├── drivers.xlsx                  
│── main.py           # Main script
│── rating_system.py  # Core logic
│── api.py            # API
├── tests/                # (Optional) Unit tests
├── requirements.txt      # Dependencies
├── LICENSE               # Open-source license (MIT)
├── .gitignore            # Ignore unnecessary files
├── README.md             # Documentation (This file)
```

## Technologies Used
- Python
- Pandas (Data Handling)
- NumPy (Mathematical Operations)
- Excel (XLSX) (Data Storage)

# Developer Info
- **Keerthi Ram Valluri**
- **BTech CSE, Amrita School of Engineering, Bangalore**
- [LinkedIn](https://in.linkedin.com/in/valluri-keerthi-ram-503576216)
- [Email](mailto:keerthiramvalluri@gmail.com)
