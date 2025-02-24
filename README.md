# Spotify Mood Playlist Creator

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Last Commit](https://img.shields.io/github/last-commit/Jakub-Horacek/spotify-playlist-helper)

## Overview

This Python application analyzes your **Spotify listening history** from JSON files and generates a **comprehensive PDF guide** to help you create mood-based playlists. By analyzing your listening patterns, it provides personalized recommendations organized by different moods and musical atmospheres.

## How It Works

### 1. **Input Files**

The application processes your Spotify data export files:

- **StreamingHistory\_\*.json** – Your listening history data
- **Playlist\*.json** – Your existing playlist data (optional)

To get your Spotify data:

1. Go to [Spotify Privacy Settings](https://www.spotify.com/account/privacy/)
2. Log in to your Spotify account
3. Request your data by clicking "Request" button
4. Wait for an email from Spotify (usually takes 1-7 days)
5. Download your data package when you receive the email
6. Extract the JSON files from the downloaded ZIP file
7. Place the extracted JSON files in a folder to use with this application

The most important files for this application are:

- `StreamingHistory_music_*.json` - Recent streaming history
- `Playlist*.json` - Your playlist data
- `Marquee_*.json` - Additional listening data

### 2. **Data Processing**

The application:

- **Analyzes listening patterns** across your entire history
- **Identifies mood patterns** based on music characteristics
- **Creates mood-based recommendations** using your listening preferences
- **Suggests new artists** that match your taste in each mood category

### 3. **Mood Categories**

The tool organizes music into key mood categories:

- Relaxing
- Energetic
- Melancholic
- Happy
- Focus

Each category is created based on genre analysis, tempo, and listening patterns.

### 4. **PDF Report Generation**

Once the data is processed, the script generates a **PDF report** with the following sections:

1. **Listening Overview**: A summary of the top genres, artists, and tracks.
2. **Trends**: The top genres, artists, and tracks broken down by timeframes: last month, last year, last 2 years, and lifetime.
3. **Top Tracks by Marquee Segments**: A section highlighting tracks that have been linked to **active listeners** or other segments based on the Marquee data.
4. **Recommendations**: A list of songs you might enjoy, clearly marked as recommendations.
5. **Visuals**: Simple, easy-to-read visuals (charts or graphs) showing genre and artist breakdowns.

### 5. **Customization**

The script allows for easy customization of several parameters:

- **Number of top items** to include in each section (e.g., top 10 or top 20 tracks/artists).
- **Exclusion of skipped tracks** during ranking.
- **Mood categorization settings**: Automatically suggest moods but allow manual overrides.
- **Visual types**: Customize the style of charts for genre and artist distributions.

### 6. **Performance**

The application is optimized to handle large datasets efficiently. It processes the JSON files one by one and uses logging to provide progress updates. An estimated time for completion is shown during the execution of the script.

### 7. **Output**

The final result is a **single PDF document** (maximum of 5-10 pages). The document is compact and readable, with sections clearly laid out for easy understanding. You can adjust the number of top items to display and customize the look and feel of the generated report.

### 8. **How to Run the Application**

1. **Install Dependencies**:
   Ensure you have the necessary Python packages installed. Run the following command:

```bash
pip install fpdf pandas matplotlib
```

2. **Prepare JSON Files**:
   Place all the relevant JSON files in a single folder.
3. **Run the Script**:
   Run the Python script by executing:

```bash
python spotify_report_generator.py
```

4. **Access the Report**:
   The PDF will be generated in the output folder (by default). You can adjust this by changing the script's settings.

### 9. Customization (for Developers)

- You can modify the script to adjust the count of top items (e.g., top 10 or top 20).
- Customize the visualization settings (like chart styles).
- Update how mood categorization works to fit your preferences.

### 10. Notes

- This application does not require a GUI, and it operates purely via command line.
- The report will focus on concise and relevant data, making it easy to help you or your friend create the perfect playlist.

### 11. Future Plans

Check out my [TODO list](TODO.md) for upcoming features and improvements.

### 12. Project Structure

- `input-data/` - Place your Spotify data files here
- `output/` - Generated PDF reports will be saved here
- `main.py` - Main script
- `src/` - Source code
- `src/analyzer/` - Data analysis logic
- `src/report/` - PDF generation code
- `src/utils/` - Helper functions
- `requirements.txt` - Dependencies
- `README.md` - This file
