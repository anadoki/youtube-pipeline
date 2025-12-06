# YouTube Trending Video Data Pipeline and Insights Dashboard

**DASHBOARD LINK**: https://youtube-pipeline-anadoki.streamlit.app

This project collects, processes, and analyzes data from YouTube’s Trending Videos API. It includes a data extraction script, a transformation pipeline, exploratory data analysis, and an interactive Streamlit dashboard for visualizing insights.

## Overview

The goal of this project is to understand patterns in trending videos, including view dynamics, engagement behavior, publishing time effects, and channel-level performance. The workflow covers:

- Automated data extraction from the YouTube Data API  
- Data cleaning and feature engineering  
- Exploratory data analysis  
- An interactive Streamlit dashboard for examining insights

## Features

### Data Pipeline
- Fetches trending video metadata from the YouTube API  
- Cleans raw fields and normalizes datatypes  
- Converts ISO 8601 durations into minutes  
- Generates derived metrics such as views per day, engagement rate, tag count, and time buckets

### Dashboard
- Global aggregated insights  
- Channel-level filtering  
- Time bucket filtering  
- Scatterplots for duration vs. views and likes vs. views  
- Correlation analysis between numerical features  
- Filtered data preview  
- CSV export functionality

## Project Structure


```bash
youtube-pipeline/
│
├── app/
│ └── main.py
│
├── data/
│ └── youtube_clean.csv
│
├── src/
│ └── util.py
│
├── notebooks/
│ ├── extract.ipynb
│ ├── transform.ipynb
│ └── eda.ipynb
│
├── README.md
└── .gitignore
```


## Installation

Clone the repository:

```bash
git clone https://github.com/anadoki/youtube-pipeline.git
cd youtube-pipeline
```
Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```
Install dependencies:
```bash
pip install -r app/requirements.txt
```
Running the Dashboard
From the project root:
```bash
streamlit run app/main.py
```
The application will open at http://localhost:8501.
Data Extraction
The extraction notebook retrieves trending video metadata using the YouTube Data API.
Store your API key in a .env file:
```bash
YOUTUBE_API_KEY=your_key_here
```
The extracted data is saved as youtube_data.csv and processed into youtube_clean.csv during transformation.

## Feature Engineering Summary

- `duration_parsed`: video duration converted to minutes  
- `views_per_day`: daily average view count  
- `engagement_rate`: likes divided by views  
- `tag_count`: number of tags  
- `time_bucket`: period of day based on upload time  
- `is_weekend`: weekend indicator after timezone conversion  

## Exploratory Data Analysis

The EDA notebook includes:

- Distribution plots for numerical features  
- Correlation matrix  
- Channel-level metrics  
- Relationships between engagement and upload patterns  

## Deployment

This project can be deployed on Streamlit Cloud by configuring the entry point as:




