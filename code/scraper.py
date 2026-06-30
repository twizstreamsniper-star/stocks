"""
NASDAQ Stock Price Scraper
Fetches historical stock data from NASDAQ API
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path


class StockScraper:
    def __init__(self):
        self.api_url = "https://api.nasdaq.com/api/quote/{symbol}/historical"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        }
    
    def fetch_stock(self, symbol, years=2):
        """Fetch historical data for a stock"""
        
        # Calculate date range
        to_date = datetime.now().strftime('%Y-%m-%d')
        from_date = (datetime.now() - timedelta(days=years*365)).strftime('%Y-%m-%d')
        
        params = {
            "assetclass": "stocks",
            "fromdate": from_date,
            "todate": to_date,
            "limit": 1000
        }
        
        print(f"Fetching {symbol} from {from_date} to {to_date}...")
        
        try:
            response = requests.get(
                self.api_url.format(symbol=symbol),
                headers=self.headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Extract trading data
            rows = data.get('data', {}).get('tradesTable', {}).get('rows', [])
            
            if not rows:
                print(f"No data found for {symbol}")
                return None
            
            # Clean data
            df = self._clean_data(rows, symbol)
            print(f"✓ Got {len(df)} records")
            
            return df
            
        except Exception as e:
            print(f"✗ Error fetching {symbol}: {e}")
            return None
    
    def _clean_data(self, rows, symbol):
        """Clean and format raw API data"""
        cleaned = []
        
        for row in rows:
            try:
                cleaned.append({
                    'symbol': symbol,
                    'date': datetime.strptime(row['date'], '%m/%d/%Y').strftime('%Y-%m-%d'),
                    'open': float(row['open'].replace('$', '').replace(',', '')),
                    'high': float(row['high'].replace('$', '').replace(',', '')),
                    'low': float(row['low'].replace('$', '').replace(',', '')),
                    'close': float(row['close'].replace('$', '').replace(',', '')),
                    'volume': int(row['volume'].replace(',', ''))
                })
            except (KeyError, ValueError):
                continue
        
        df = pd.DataFrame(cleaned)
        df = df.sort_values('date').reset_index(drop=True)
        return df
    
    def save_to_csv(self, df, symbol, output_dir='downloads'):
        """Save dataframe to CSV"""
        Path(output_dir).mkdir(exist_ok=True)
        filepath = Path(output_dir) / f"{symbol}.csv"
        df.to_csv(filepath, index=False)
        print(f"✓ Saved to {filepath}")
        return filepath


if __name__ == "__main__":
    scraper = StockScraper()
    
    # Fetch Apple
    df = scraper.fetch_stock('AAPL', years=2)
    
    if df is not None:
        scraper.save_to_csv(df, 'AAPL')
        print(f"\nSummary:")
        print(f"  Records: {len(df)}")
        print(f"  Date range: {df['date'].min()} to {df['date'].max()}")
        print(f"  Price: ${df['close'].min():.2f} - ${df['close'].max():.2f}")
