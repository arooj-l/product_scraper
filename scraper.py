# -----------------------------------------------------------
# Product Scraper: Books to Scrape
# This script extracts product information such as:
# Title, Price, Rating, Availability, and Product Link
# from the website http://books.toscrape.com
# The extracted data is saved into a CSV file.
# -----------------------------------------------------------

import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

# Base URL of the websit
base_url = "http://books.toscrape.com/"

# variable to keep track of the current page being scraped.
# Initially it starts with homepage(base_url)
page_url = base_url

# to keep track which page is being tracked
page_number = 1

# Open CSV file to store scraped data
with open("books_full.csv", "w", newline = "", encoding= "utf_8")as file:

    # csv writer objectc for writing rows to the file
    writer = csv.writer(file)

    # Write the header row(column names)
    writer.writerow(["Title", "Price", "Rating", "Availability"])
    # Loop through all pages using paginatiom 
    while True:
        print(f"Scraping page {page_number}...")

        # Send HTTP request to the webpage
        response = requests.get(page_url)
        # Raise error if request fails
        response.raise_for_status() 

        # Parse HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all product conatiners
        products = soup.find_all("article", class_= "product_pod")

        for product in products:
            # Extract product title
            link_tag= product.find("h3").find("a")
            title = link_tag["title"]
            # Extract price
            price = product.find('p', class_="price_color").text
            # Extract rating from class attribute
            rating = product.find('p', class_='star-rating')['class'][1]
            # Extract availability
            availability = product.find(
                'p', class_= "instock availability"
            ).text.strip()

            # Convert relative URL to absolute URL and convert it to an absolute URL 
            relative_link = product.find("h3").find("a")["href"]
            product_link = urljoin(page_url, relative_link)

            writer.writerow([title, price, rating, availability, product_link])


        # Handle Pagination
        next_button = soup.find("li", class_="next")
        
        # The website includes a "NEXT" button, if more pages exist.
        # If this element is found, we procees to the next page

        if next_button:
            next_page = next_button.find("a")["href"]

            # Extract the relative url of the naxt page 
            page_url = urljoin(page_url, next_page)

            page_number +=1

        else:
            break
print("Scraping completed! Data saved to books_full.csv")