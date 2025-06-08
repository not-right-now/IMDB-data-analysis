import os
import sys
import argparse
import logging
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.io as pio

def setup_logging():
    """Sets up basic logging for the script."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

def get_csv_path(initial_path):
    """
    Ensures the CSV path is valid. If not, it prompts the user to enter a valid path.
    This makes the script more robust if the file isn't in the default location.
    """
    path = initial_path
    while not os.path.isfile(path):
        logging.error(f"CSV file not found at: {path}")
        try:
            path = input("Please enter a valid path to 'imdb_top_1000.csv': ").strip()
        except (KeyboardInterrupt, EOFError):
            logging.error("Input interrupted. Exiting.")
            sys.exit(1)
    logging.info(f"Found CSV file at: {path}")
    return path

def ensure_directory(path):
    """
    Checks if a directory exists and creates it if it doesn't.
    This is where the output visualizations will be saved.
    """
    try:
        os.makedirs(path, exist_ok=True)
        logging.info(f"Output directory is set to: {path}")
    except OSError as e:
        logging.error(f"Could not create directory {path}: {e}")
        sys.exit(1)

def main():
    """Main function to run the data analysis and visualization."""
    setup_logging()

    # --- Argument Parsing ---
    parser = argparse.ArgumentParser(
        description="A tool to analyze and create interactive visualizations for the IMDb Top 1000 movies dataset."
    )
    parser.add_argument(
        "--csv", dest="csv_path", default="data/imdb_top_1000.csv",
        help="Path to the input IMDb CSV file (default: data/imdb_top_1000.csv)"
    )
    parser.add_argument(
        "--out", dest="out_dir", default="visualizations",
        help="Directory to save the interactive HTML visualizations (default: visualizations)"
    )
    args = parser.parse_args()

    csv_path = get_csv_path(args.csv_path)
    out_dir = args.out_dir
    ensure_directory(out_dir)

    # --- Data Loading and Cleaning ---
    try:
        df = pd.read_csv(csv_path)
        logging.info("Successfully loaded the dataset.")
    except Exception as e:
        logging.error(f"Failed to read CSV file: {e}")
        sys.exit(1)

    logging.info("Initial missing values:\n%s", df.isnull().sum())

    # Fill missing 'Certificate' values. 'Not Rated' is a safe neutral placeholder.
    df['Certificate'] = df['Certificate'].fillna('Not Rated')

    # Clean and convert 'Gross' revenue column.
    if 'Gross' in df.columns and df['Gross'].dtype == 'object':
        df['Gross'] = df['Gross'].str.replace(',', '', regex=False)
    df['Gross'] = pd.to_numeric(df['Gross'], errors='coerce')
    median_gross = df['Gross'].median()
    # FIX: The line below is updated to avoid the FutureWarning.
    df['Gross'] = df['Gross'].fillna(median_gross)
    logging.info(f"Filled missing 'Gross' values with median: ${median_gross:,.2f}")

    # Drop rows where critical information is missing.
    df.dropna(subset=['Genre', 'Director', 'Series_Title', 'Released_Year'], inplace=True)

    # Clean and convert 'Released_Year'.
    df['Released_Year'] = pd.to_numeric(df['Released_Year'], errors='coerce')
    df.dropna(subset=['Released_Year'], inplace=True)
    df['Released_Year'] = df['Released_Year'].astype(int)

    # --- Feature Engineering ---
    # Extract runtime in minutes as an integer.
    df['Runtime_Minutes'] = df['Runtime'].str.extract(r'(\d+)').astype(int)
    # Create a 'Decade' column for trend analysis.
    df['Decade'] = (df['Released_Year'] // 10) * 10

    # Clean genre strings for consistency.
    df['Genre'] = df['Genre'].apply(lambda g: ", ".join(sorted([x.strip() for x in g.split(',')])))
    
    # Remove duplicate movie titles, keeping the first entry.
    df.drop_duplicates(subset=['Series_Title'], keep='first', inplace=True)
    logging.info("Data cleaning and feature engineering complete.")

    # --- Data Storytelling & Insights ---
    logging.info("--- Key Insights from the Data ---")
    highest_gross_movie = df.loc[df['Gross'].idxmax()]
    logging.info(f"🎬 Highest Grossing Movie: '{highest_gross_movie['Series_Title']}' with ${highest_gross_movie['Gross']:,.0f}")
    
    all_genres = df['Genre'].str.split(', ').explode()
    most_common_genre = all_genres.value_counts().idxmax()
    logging.info(f"🎭 Most Common Genre: '{most_common_genre}'")
    
    top_director = df['Director'].value_counts().idxmax()
    logging.info(f"🏆 Most Prolific Director in Top 1000: '{top_director}'")
    
    
    # --- Interactive Visualizations with Plotly ---
    pio.templates.default = "plotly_dark" # Using a nice dark theme!

    # 1. IMDb Rating Trends Over Decades (Line Chart)
    logging.info("Generating: 1. IMDb Rating Trends Over Decades")
    rating_by_decade = df.groupby('Decade')['IMDB_Rating'].mean().reset_index()
    fig1 = px.line(
        rating_by_decade, 
        x='Decade', 
        y='IMDB_Rating', 
        markers=True,
        title='✨ Average IMDb Rating of Top Movies Through the Decades',
        labels={'IMDB_Rating': 'Average IMDb Rating', 'Decade': 'Decade'},
        template='plotly_dark'
    )
    fig1.update_traces(marker=dict(size=10, line=dict(width=2, color='DarkSlateGrey')), line=dict(color='cyan'))
    fig1.write_html(os.path.join(out_dir, '1_rating_trend.html'))

    # 2. Genre Popularity (Bar Chart)
    logging.info("Generating: 2. Genre Popularity")
    genre_counts = all_genres.value_counts().nlargest(10).sort_values(ascending=True)
    fig2 = px.bar(
        genre_counts,
        x=genre_counts.values,
        y=genre_counts.index,
        orientation='h',
        title='🎭 Top 10 Most Frequent Genres in IMDb Top 1000',
        labels={'x': 'Number of Movies', 'y': 'Genre'},
        template='plotly_dark',
        color=genre_counts.values,
        color_continuous_scale=px.colors.sequential.Plasma
    )
    fig2.update_layout(showlegend=False)
    fig2.write_html(os.path.join(out_dir, '2_genre_popularity.html'))

    # 3. Correlation Heatmap
    logging.info("Generating: 3. Correlation Heatmap")
    corr_df = df[['IMDB_Rating', 'Runtime_Minutes', 'Gross', 'Released_Year']].corr()
    fig3 = px.imshow(
        corr_df,
        text_auto=True,
        aspect="auto",
        title='🔍 Correlation Between Key Movie Metrics',
        labels=dict(color="Correlation"),
        color_continuous_scale='Viridis'
    )
    fig3.write_html(os.path.join(out_dir, '3_feature_correlation.html'))
    
    # 4. Top 10 Directors by Movie Count (Bar Chart)
    logging.info("Generating: 4. Top Directors by Movie Count")
    top_directors = df['Director'].value_counts().nlargest(10).sort_values(ascending=True)
    fig4 = px.bar(
        top_directors,
        x=top_directors.values,
        y=top_directors.index,
        orientation='h',
        title='🏆 Top 10 Most Prolific Directors in IMDb Top 1000',
        labels={'x': 'Number of Movies', 'y': 'Director'},
        template='plotly_dark',
        color=top_directors.values,
        color_continuous_scale=px.colors.sequential.Cividis_r
    )
    fig4.update_layout(showlegend=False)
    fig4.write_html(os.path.join(out_dir, '4_top_directors.html'))
    
    # 5. Rating vs. Gross Revenue (Scatter Plot)
    logging.info("Generating: 5. Rating vs. Gross Revenue Scatter Plot")
    fig5 = px.scatter(
        df,
        x="Gross",
        y="IMDB_Rating",
        hover_name="Series_Title", # This shows movie title on hover!
        color="Runtime_Minutes",
        size="Gross",
        size_max=60,
        title="💰 IMDb Rating vs. Gross Revenue",
        labels={'Gross': 'Gross Revenue (in $)', 'IMDB_Rating': 'IMDB Rating'},
        template='plotly_dark',
        color_continuous_scale=px.colors.sequential.Inferno
    )
    fig5.update_xaxes(type="log") # Use a log scale for better visualization of Gross
    fig5.write_html(os.path.join(out_dir, '5_rating_vs_gross.html'))

    logging.info(f"🎉 All interactive visualizations have been saved in the '{out_dir}' directory!")

if __name__ == '__main__':
    main()

