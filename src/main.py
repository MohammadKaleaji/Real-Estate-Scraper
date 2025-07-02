# src/main.py
from scraper import AqarScraper
import pandas as pd

def main():
    print("🏠 Aqar.fm Property Scraper")
    print("--------------------------")
    
    city = input("Enter city name in Arabic (e.g. الرياض, جدة) [الرياض]: ") or "الرياض"
    max_price = int(input("Enter maximum price in SAR [500000]: ") or 500000)
    pages = int(input("Number of pages to scrape [1]: ") or 1)
    
    scraper = AqarScraper(headless=False)
    print("\n⏳ Scraping data... (This may take a few minutes)")
    
    try:
        df = scraper.scrape(city=city, max_price=max_price, pages=pages)
        
        if not df.empty:
            timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M")
            filename = f"aqar_results_{city}_{timestamp}.xlsx"
            df.to_excel(filename, index=False)
            print(f"\n✅ Success! Saved {len(df)} properties to '{filename}'")
            print("\nSample Results:")
            print(df.head(3).to_string(index=False))
        else:
            print("\n❌ No properties found matching your criteria")
    
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")

if __name__ == "__main__":
    main()