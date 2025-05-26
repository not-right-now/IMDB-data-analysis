# IMDb Data Analysis

A Python-based CLI tool for analyzing and visualizing the IMDb Top 1000 movies dataset. This project cleans and enriches the data, extracts key features, computes summary statistics, and generates a series of insightful plots.

## Repository Structure

```
IMDB-data-analysis/
├── data/
│   └── imdb_top_1000.csv       # Raw IMDb dataset (Top 1000 movies)
├── IMDB_data_analysis.py       # Main analysis & visualization script
├── visualizations/             # Output folder for generated plots
│   ├── correlation.png
│   ├── genre_popularity.png
│   ├── rating_trend.png
│   └── top_directors.png
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation (this file)
```

## Features

* **Robust CSV handling**: Verifies file existence and prompts for correct path.
* **Missing value management**: Fills or drops nulls for critical fields.
* **Feature engineering**: Parses runtime, counts genres, extracts decade bins, and one-hot encodes certificates.
* **Outlier filtering**: Caps gross revenue using the IQR method and applies a log transform.
* **Statistical summary**: Computes basic descriptive statistics and key insights (highest grossing movie, most common genre).
* **Visualizations**:

  1. IMDb rating trends over decades (`rating_trend.png`)
  2. Top 10 genres by frequency (`genre_popularity.png`)
  3. Feature correlation heatmap (`correlation.png`)
  4. Top 10 directors by movie count (`top_directors.png`)

## Requirements

* Python 3.8 or higher
* Packages listed in `requirements.txt`:

  ```text
  numpy
  pandas
  matplotlib
  seaborn
  ```

## Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/imdb-data-analysis.git
   cd imdb-data-analysis
   ```

2. **Create & activate a virtual environment** (recommended)

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate    # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Place the CSV file**
   Ensure `imdb_top_1000.csv` resides in the `data/` folder. If you store it elsewhere, you’ll be prompted to enter its path when running the script.

## Usage

Run the analysis script with optional arguments:

```bash
python IMDB_data_analysis.py \
  --csv data/imdb_top_1000.csv \
  --out visualizations
```

* `--csv`: Path to the IMDb CSV file (default: `data/imdb_top_1000.csv`).
* `--out`: Directory where plots will be saved (default: `visualizations`).

During execution, the script will:

1. Validate the CSV path.
2. Load and clean the data.
3. Compute summary statistics.
4. Generate and save plots to the specified output folder.

## Output

After successful execution, you will find:

* Four PNG charts in the `visualizations/` directory.
* Console logs detailing progress, statistics, and insights.

## Contributing

Feel free to open issues or PRs to:

* Add new visualizations (e.g., rating distributions, actor networks).
* Export results as CSV, Excel, or interactive HTML.
* Improve performance or add unit tests.

## License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.

