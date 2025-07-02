# src/main.py
from scraper import AqarScraper

def main():
    print("Aqar.fm Riyadh Flat Scraper")
    city = input("Enter city name in Arabic (default: الرياض): ") or "الرياض"
    max_price = int(input("Enter maximum price in SAR (default: 500000): ") or 500000)
    pages = int(input("Number of pages to scrape (default: 1): ") or 1)
    
    scraper = AqarScraper(headless=False)  # Set headless=True for production
    listings = scraper.scrape(city, max_price, pages)
    
    if listings:
        scraper.save_to_csv(listings)
        print(f"\nFound {len(listings)} matching listings:")
        for idx, item in enumerate(listings[:3], 1):  # Show first 3 samples
            print(f"{idx}. {item['title']} - {item['price']} SAR")
        print("\nFull results saved to 'src/output/results.csv'")
    else:
        print("No listings found matching your criteria.")

if __name__ == "__main__":
    main()