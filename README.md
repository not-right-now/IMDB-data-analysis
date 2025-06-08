# 📊 IMDb Data Analysis & Interactive Visualization

*An interactive exploration of the top 1000 movies, brought to life with Python and Plotly.*

This project offers an interactive exploration of the IMDb Top 1000 movies dataset. It cleans the data, derives key insights, and generates a series of **interactive visualizations** to tell a story about the best movies of all time.

## 🚀 Project Highlights

* **Interactive Charts**: Instead of static images, the project generates interactive HTML plots using Plotly. You can hover for details, zoom, and pan!
* **Data Storytelling**: The visualizations are designed to present a clear narrative about movie trends over time, genre popularity, and what makes a film successful.
* **Robust Scripting**: The Python script is designed to be user-friendly, with clear logging, error handling, and argument parsing.

## 📂 Repository Structure

```
IMDB-data-analysis/
├── data/
│   └── imdb_top_1000.csv       # Raw IMDb dataset
├── visualizations/             # Output folder for generated plots
│   ├── 1_rating_trend.html
│   ├── 2_genre_popularity.html
│   ├── 3_feature_correlation.html
│   ├── 4_top_directors.html
│   └── 5_rating_vs_gross.html
├── IMDB_data_analysis.py       # Main analysis & visualization script
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation (this file)
```

## 📊 The Visualizations: A Data Story

You can find the interactive `.html` files in the `visualizations/` folder after running the script. Open them in your web browser to explore!

### 1. ✨ Average IMDb Rating Through the Decades
> See how the average rating of top-tier movies has evolved over time.

### 2. 🎭 Top 10 Most Frequent Genres
> Discover which genres dominate the IMDb Top 1000 list.

### 3. 🔍 Correlation Between Key Movie Metrics
> Answer questions like, "Do longer movies get better ratings?".

### 4. 🏆 Top 10 Most Prolific Directors
> Celebrate the directors who appear most frequently in the Top 1000.

### 5. 💰 IMDb Rating vs. Gross Revenue
> Explore the link between critical acclaim and commercial success. Hover over any bubble to see the movie's title!

## ✅ Requirements

* Python 3.8 or higher
* Packages listed in `requirements.txt`:
    * `pandas`
    * `plotly`
    * `numpy`

## 🔧 Setup

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/not-right-now/IMDB-data-analysis.git](https://github.com/not-right-now/IMDB-data-analysis.git)
    cd IMDB-data-analysis
    ```

2.  **Create & activate a virtual environment** (recommended)
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate    # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Place the CSV file**
    Ensure `imdb_top_1000.csv` resides in the `data/` folder.

## 🚀 Usage

Run the analysis script from your terminal.

```bash
python IMDB_data_analysis.py
```

You can also specify custom paths:
```bash
python IMDB_data_analysis.py --csv path/to/your.csv --out path/to/save
```
The default CSV path is `data/imdb_top_1000.csv` and the default output folder is `visualizations/`.

## 📈 Output

* Five interactive **HTML files** in the `visualizations/` directory.
* Console logs detailing the script's progress and key insights.

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**. Feel free to open an issue or submit a pull request!

## 📜 License

This project is released under the MIT License.
