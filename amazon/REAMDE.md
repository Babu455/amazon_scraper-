# Amazon Laptop Scraper 

## Project Overview
I developed this web scraper to extract laptop product information from Amazon.in . The script automatically browses through multiple pages and collects comprehensive product details into a timestamped CSV file.
What Data Gets Collected
For each laptop product on Amazon.in, the scraper extracts:

**Image URL** - Product image link
**Title** - Full product name/title
**Rating** - Customer rating (out of 5 stars)
**Price** - Current product price in INR
**Result Type** - Whether it's an "Ad" (sponsored) or "Organic" result

I used **Selenium** instead of simpler scraping libraries because Amazon loads product data dynamically using JavaScript. Selenium simulates a real browser, which means:

1. It can execute JavaScript and load dynamic content
2. It can navigate through pagination automatically
3. It handles requests that load products

Technical Requirements
Python libraries:
bashpip install -r requirements.txt
This installs:

### selenium - Browser automation framework
### pandas - Data manipulation and CSV export

amazon_laptops_YYYYMMDD_HHMMSS.csv

Implementation Details
Key Features
1. Pagination Handling
     The scraper automatically clicks through all available pages. I implemented logic to detect the "Next" button and stop when reaching the last page.
2. Ad Detection
     I check each product for "Sponsored" tags to classify results as advertisements or organic listings.
3. Error Handling
     Not every product has all fields. The code handles missing elements gracefully:

     If no rating exists, it records "No rating"
     If no price exists, it records "Price not available"
     If image/title missing, it skips that product

4. Timestamp Implementation
     Output file includes a timestamp using Python's datetime module, ensuring no file overwrites occur.

## Technical Challenges Solved
**Dynamic Content Loading**
    Amazon doesn't load all products immediately. I added explicit waits to ensure elements are present before trying to extract data. This prevents the script from crashing due to timing issues.
**Varying HTML Structure**
    Products sometimes have different CSS selectors depending on their type or promotion status. I implemented fallback selectors to try multiple approaches.
**Bot Detection**
Amazon has anti-scraping measures. I handled this by:

Adding human-like delays between actions
Using proper user-agent strings
Scrolling the page naturally

**Data Consistency**
I used pandas DataFrame to ensure consistent data structure, making it easier to analyze the results later.

1. Script saved as .py file
2. Output CSV saved with timestamp format
3. All required fields extracted (Image, Title, Rating, Price, Result Type)
4. Works across multiple pages, not just 1-2

I'm happy to discuss any implementation decisions or answer questions about the code.
