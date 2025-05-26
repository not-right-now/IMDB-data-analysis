import os
import sys
import argparse
import logging
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )


def get_csv_path(initial_path):
    """
    Ensure the CSV path is valid, prompt user until a valid file is provided.
    """
    path = initial_path
    while True:
        if os.path.isfile(path):
            logging.info(f"Found CSV file at: {path}")
            return path
        logging.error(f"CSV file not found at: {path}")
        try:
            path = input("Please enter a valid path to 'imdb_top_1000.csv': ").strip()
        except (KeyboardInterrupt, EOFError):
            logging.error("Input interrupted. Exiting.")
            sys.exit(1)


def ensure_directory(path):
    """
    Create the directory if it doesn't exist.
    """
    try:
        os.makedirs(path, exist_ok=True)
        logging.info(f"Output directory is set to: {path}")
    except Exception as e:
        logging.error(f"Could not create directory {path}: {e}")
        sys.exit(1)


def main():
    setup_logging()

    parser = argparse.ArgumentParser(
        description="Robust IMDb Top 1000 analysis and visualization script"
    )
    parser.add_argument(
        "--csv", dest="csv_path", default="data/imdb_top_1000.csv",
        help="Path to the IMDb CSV file"
    )
    parser.add_argument(
        "--out", dest="out_dir", default="visualizations",
        help="Directory to save visualizations"
    )
    args = parser.parse_args()

    csv_path = get_csv_path(args.csv_path)
    out_dir = args.out_dir
    ensure_directory(out_dir)

    # Load data
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        logging.error(f"Failed to read CSV: {e}")
        sys.exit(1)

    logging.info("Missing values before handling:\n%s", df.isnull().sum())

    # Handle missing values
    df['Certificate'] = df['Certificate'].fillna('Not Rated')

    # Process Gross
    if df['Gross'].dtype == 'object':
        df['Gross'] = df['Gross'].str.replace(',', '', regex=False)
    df['Gross'] = pd.to_numeric(df['Gross'], errors='coerce')
    median_gross = df['Gross'].median()
    df['Gross'].fillna(median_gross, inplace=True)

    # Drop missing critical fields
    df.dropna(subset=['Genre', 'Director', 'Series_Title'], inplace=True)

    # Process Released_Year
    df['Released_Year'] = pd.to_numeric(df['Released_Year'], errors='coerce')
    df.dropna(subset=['Released_Year'], inplace=True)
    df['Released_Year'] = df['Released_Year'].astype(int)

    # Feature extraction
    df['Num_Genres'] = df['Genre'].str.split(',').str.len()
    runtime_extracted = df['Runtime'].str.extract(r"(\d+)")
    df['Runtime_Minutes'] = runtime_extracted[0].astype(int)
    df['Decade'] = (df['Released_Year'] // 10) * 10

    # One-hot encode Certificate
    df = pd.get_dummies(df, columns=['Certificate'], drop_first=True)

    # Clean and standardize Genre
    def clean_genre(g):
        parts = [x.strip() for x in g.split(',')]
        return ", ".join(sorted(parts))
    df['Genre'] = df['Genre'].apply(clean_genre)

    # Ensure numeric types
    numeric_cols = ['IMDB_Rating', 'Runtime_Minutes', 'Gross', 'Released_Year']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Remove duplicates
    df.drop_duplicates(subset=['Series_Title'], keep='first', inplace=True)

    # Basic statistics
    logging.info("Basic statistics:\n%s", df[['IMDB_Rating', 'Runtime_Minutes', 'Gross']].describe())

    # Insights
    try:
        highest_gross = df.loc[df['Gross'].idxmax()]
        logging.info("Highest grossing movie: %s ($%s)",
                     highest_gross['Series_Title'],
                     f"{highest_gross['Gross']:,}")
    except ValueError:
        logging.warning("Could not determine highest grossing movie.")

    try:
        most_common_genre = df['Genre'].str.split(', ').explode().value_counts().idxmax()
        logging.info("Most common genre: %s", most_common_genre)
    except Exception:
        logging.warning("Could not determine the most common genre.")

    # Visualizations
    sns.set(style='whitegrid')

    # 1. IMDb Rating trends over decades
    plt.figure()
    rating_by_decade = df.groupby('Decade')['IMDB_Rating'].mean().reset_index()
    sns.lineplot(data=rating_by_decade, x='Decade', y='IMDB_Rating', marker='o')
    plt.title('IMDb Ratings Over Decades')
    plt.xlabel('Decade')
    plt.ylabel('Average Rating')
    plt.savefig(os.path.join(out_dir, 'rating_trend.png'))
    plt.close()

    # 2. Top 10 genres by count
    plt.figure()
    genre_counts = df['Genre'].str.split(', ').explode().value_counts()
    genre_counts.head(10).plot(kind='barh')
    plt.title('Top 10 Genres')
    plt.xlabel('Count')
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'genre_popularity.png'))
    plt.close()

    # 3. Cap Gross outliers and log-transform
    Q1 = df['Gross'].quantile(0.25)
    Q3 = df['Gross'].quantile(0.75)
    IQR = Q3 - Q1
    df_filtered = df[(df['Gross'] >= Q1 - 1.5 * IQR) & (df['Gross'] <= Q3 + 1.5 * IQR)].copy()
    df_filtered['Log_Gross'] = np.log1p(df_filtered['Gross'])

    # 4. Correlation heatmap
    plt.figure()
    corr = df_filtered[['IMDB_Rating', 'Runtime_Minutes', 'Gross', 'Log_Gross']].corr()
    sns.heatmap(corr, annot=True)
    plt.title('Feature Correlation')
    plt.savefig(os.path.join(out_dir, 'correlation.png'))
    plt.close()

    # 5. Top 10 directors
    plt.figure()
    df['Director'].value_counts().head(10).plot(kind='barh')
    plt.title('Top 10 Directors')
    plt.xlabel('Number of Movies')
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'top_directors.png'))
    plt.close()

    logging.info("All visualizations saved in '%s'", out_dir)


if __name__ == '__main__':
    main()
