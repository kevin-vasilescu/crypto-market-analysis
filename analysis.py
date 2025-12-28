import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import datetime, timedelta

# Fetch Bitcoin price data from CoinGecko
def fetch_crypto_data(days=30):
    """Fetch historical crypto price data"""
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days,
        "interval": "daily"
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # Extract prices and timestamps
        prices = data['prices']
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
        df = df[['date', 'price']]
        
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

# Calculate metrics
def analyze_crypto(df):
    """Calculate key metrics"""
    df['moving_avg_7'] = df['price'].rolling(window=7).mean()
    df['moving_avg_14'] = df['price'].rolling(window=14).mean()
    df['volatility'] = df['price'].rolling(window=7).std()
    df['price_change'] = df['price'].pct_change() * 100
    
    return df

# Visualize results
def visualize_analysis(df):
    """Create visualization plots"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Bitcoin Market Analysis (30 Days)', fontsize=16, fontweight='bold')
    
    # Price and Moving Averages
    axes[0, 0].plot(df['date'], df['price'], label='Price', linewidth=2)
    axes[0, 0].plot(df['date'], df['moving_avg_7'], label='7-day MA', linestyle='--')
    axes[0, 0].plot(df['date'], df['moving_avg_14'], label='14-day MA', linestyle='--')
    axes[0, 0].set_title('Price & Moving Averages')
    axes[0, 0].set_ylabel('Price (USD)')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Volatility
    axes[0, 1].bar(df['date'], df['volatility'], color='orange', alpha=0.7)
    axes[0, 1].set_title('Price Volatility (7-day std dev)')
    axes[0, 1].set_ylabel('Volatility')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Daily Returns
    axes[1, 0].bar(df['date'], df['price_change'], color=['red' if x < 0 else 'green' for x in df['price_change']], alpha=0.6)
    axes[1, 0].set_title('Daily Price Change %')
    axes[1, 0].set_ylabel('Change %')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Statistics
    stats_text = f"""Summary Statistics:
    
Price Range: ${df['price'].min():.2f} - ${df['price'].max():.2f}
Avg Price: ${df['price'].mean():.2f}
Volatility: {df['volatility'].mean():.2f}
Avg Daily Change: {df['price_change'].mean():.2f}%
Max Gain: {df['price_change'].max():.2f}%
Max Loss: {df['price_change'].min():.2f}%"""
    
    axes[1, 1].text(0.1, 0.5, stats_text, fontsize=11, family='monospace', verticalalignment='center')
    axes[1, 1].axis('off')
    
    plt.tight_layout()
    plt.savefig('crypto_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Analysis saved to crypto_analysis.png")
    plt.show()

# Main execution
if __name__ == "__main__":
    print("🔍 Fetching Bitcoin data...")
    df = fetch_crypto_data(days=30)
    
    if df is not None:
        print(f"✓ Loaded {len(df)} days of data")
        
        print("📊 Analyzing data...")
        df = analyze_crypto(df)
        
        print("📈 Generating visualizations...")
        visualize_analysis(df)
        
        # Print summary
        print("\n" + "="*50)
        print("ANALYSIS SUMMARY")
        print("="*50)
        print(f"Current Price: ${df['price'].iloc[-1]:.2f}")
        print(f"30-Day High: ${df['price'].max():.2f}")
        print(f"30-Day Low: ${df['price'].min():.2f}")
        print(f"Avg Volatility: {df['volatility'].mean():.2f}")
        print(f"Total Return: {((df['price'].iloc[-1] / df['price'].iloc[0]) - 1) * 100:.2f}%")
    else:
        print("❌ Failed to fetch data")