# Stock Price Dataset Builder - Plan

## Goal
Build a dataset of historical stock price data from NASDAQ (https://www.nasdaq.com/market-activity/quotes/historical)

## Approach

### 1. Discovery Phase
- Examine the NASDAQ historical quotes page structure
- Identify how data is loaded (API, HTML parsing, etc.)
- Reverse-engineer the data source

### 2. Data Extraction Strategy
- Find the underlying API or data endpoint
- Determine required parameters (stock symbol, date range, etc.)
- Understand data format and fields

### 3. Development Plan
- Create Python scraper to fetch historical data
- Support fetching individual stocks (e.g., just Apple)
- Support fetching multiple stocks in bulk
- Clean and format data consistently

### 4. Output Format
- Save to CSV files with columns: date, open, high, low, close, volume
- Store individual stock files in `downloads/` directory
- Organized and ready for analysis

### 5. Directory Structure
```
/workspaces/stocks/
├── code/              # Python scraping code
│   └── scraper.py
├── downloads/         # CSV output files
│   └── AAPL.csv
└── plan.md           # This file
```

## Implementation Steps
1. ✅ Create directory structure
2. ⏳ Examine NASDAQ data source
3. ⏳ Build Python scraper
4. ⏳ Fetch Apple (AAPL) historical data
5. ⏳ Save to downloads/AAPL.csv
6. ⏳ Test and validate data
