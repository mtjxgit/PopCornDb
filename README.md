---

# Popcorn Ratings

Popcorn Ratings is a web application similar to IMDb, which provides movie details and ratings. The movie data is scraped from IMDb and Rotten Tomatoes using Selenium Chromedriver. Users can get movie recommendations based on the movies they've rated before. This project uses SQLite3 as its database.

## Features

- **Movie Details**: View details of movies including title, rating, genre, description, year, certificate, runtime, OTT platform, OTT image, directors, writers, and stars.
- **Ratings**: Rate movies and view ratings from other users.
- **Recommendations**: Get personalized movie recommendations based on your rating history.
- **Web Scraping**: Scrape movie data from IMDb and Rotten Tomatoes using Selenium Chromedriver.
- **User Authentication**: Work in progress. Currently being implemented using FastAPI's inbuilt OAuth2 integration and PyJWT.

## Directory Structure

```
popcorn_reviews
├── app
│   ├── main.py
│   ├── models.py
│   ├── routers
│   ├── schemas
│   ├── database
├── scraper
│   ├── scrape_250.py
│   ├── scrape_movie.py
│   ├── scrape_news.py
├── frontend
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── profile.html
├── requirements.txt
```

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/popcorn_reviews.git
    cd popcorn_reviews
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1. **Start the FastAPI application**:
    ```bash
    uvicorn app.main:app --reload
    ```

2. **Scrape movie data**:
    The `scrape_250.py` script inside the `scraper` folder should be run manually to update the movies table with the latest data from IMDb:
    ```bash
    python scraper/scrape_250.py
    ```

## Usage

1. **Visit the application**:
    Open your browser and go to `http://127.0.0.1:8000/` to see the homepage.

2. **User Registration and Login**:
    - **Register**: Go to the signup page and create a new account.
    - **Login**: Use your credentials to log in.

3. **Profile**:
    - View your profile to see your rated movies and watchlist.

4. **Recommendations**:
    - Get movie recommendations based on your previous ratings.


## Future Plans

- Complete the implementation of user authentication using FastAPI's inbuilt OAuth2 integration and PyJWT.
- Add automated tests for the application.
- Enhance the recommendation algorithm for better accuracy.
- Implement more features such as social sharing, user reviews, and more.


---
