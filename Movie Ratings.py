"""Movie Ratings Explorer.

Run with: python movie_ratings_explorer.py
The script reads movies.csv from the same folder and prints analysis to the terminal.
"""

from pathlib import Path

import numpy as np
import pandas as pd


DATA_FILE = Path(__file__).with_name("movies.csv")


def load_and_clean_data(filename: Path) -> pd.DataFrame:
    """Load the movie CSV and remove incomplete or invalid records."""
    movies = pd.read_csv(filename)
    print(f"Rows before cleaning: {len(movies)}")

    numeric_columns = ["release_year", "rating", "vote_count", "duration_minutes"]
    for column in numeric_columns:
        movies[column] = pd.to_numeric(movies[column], errors="coerce")

    movies = movies.dropna(subset=["title", "genre", "release_year", "rating"])
    movies = movies[movies["rating"].between(0, 10)]
    movies = movies[movies["duration_minutes"] > 0].copy()
    movies["release_year"] = movies["release_year"].astype(int)

    print(f"Rows after cleaning: {len(movies)}")
    return movies


def main() -> None:
    if not DATA_FILE.exists():
        print(f"Error: Could not find {DATA_FILE.name}.")
        return

    movies = load_and_clean_data(DATA_FILE)
    ratings = movies["rating"].to_numpy()

    print("\nOVERALL RATING STATISTICS")
    print(f"Average rating: {np.mean(ratings):.2f}")
    print(f"Median rating: {np.median(ratings):.2f}")
    print(f"25th percentile: {np.percentile(ratings, 25):.2f}")
    print(f"75th percentile: {np.percentile(ratings, 75):.2f}")

    # A movie can have multiple genres, so count it in each listed genre.
    genre_movies = movies.assign(genre=movies["genre"].str.split("|")).explode("genre")
    genre_summary = (
        genre_movies.groupby("genre")["rating"]
        .agg(average_rating="mean", movie_count="count")
        .query("movie_count >= 3")
        .sort_values("average_rating", ascending=False)
    )
    print("\nGENRES WITH THE HIGHEST AVERAGE RATINGS")
    print(genre_summary.round(2).to_string())

    year_summary = (
        movies.groupby("release_year")["rating"]
        .agg(average_rating="mean", movie_count="count")
        .sort_index()
    )
    print("\nAVERAGE RATING BY RELEASE YEAR")
    print(year_summary.round(2).to_string())

    most_popular = movies.nlargest(10, "vote_count")[
        ["title", "release_year", "rating", "vote_count"]
    ]
    print("\n10 MOST POPULAR FILMS (BY VOTE COUNT)")
    print(most_popular.to_string(index=False))

    highest_rated = movies[movies["vote_count"] >= 500_000].nlargest(10, "rating")[
        ["title", "release_year", "genre", "rating", "vote_count"]
    ]
    print("\n10 HIGHEST-RATED FILMS (AT LEAST 500,000 VOTES)")
    print(highest_rated.to_string(index=False))

    print("\nAnalysis complete.")


if __name__ == "__main__":
    main()
