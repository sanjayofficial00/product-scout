import http.client
import urllib.parse
from bs4 import BeautifulSoup

# Set up the connection
conn = http.client.HTTPSConnection("www.flipkart.com")

# Specify the URL path
search_input = "iphone 14 pro max"
formatted_input = search_input.replace(" ", "+")
path = f"/search?q={urllib.parse.quote(formatted_input)}"

# Send the GET request
conn.request("GET", path)

# Get the response
response = conn.getresponse()

# Read the response data
data = response.read()

# Close the connection
conn.close()

# Now 'data' contains the response content

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(data, "html.parser")

# Extract product prices and other information
product_prices = [element.text for element in soup.find_all("div", class_="_30jeq3")]

# Initialize empty lists to store product names, ratings, and links
product_names = []
product_ratings = []
product_links = []

# Find the containers that have both prices and links (assuming the structure is consistent)
for element in soup.find_all("div", class_="_30jeq3"):
    price = element.text
    # Assuming the structure, find the parent container that includes the link
    parent_container = element.find_parent("div", class_="_1AtVbE")
    if parent_container:
        product_name = parent_container.find("a", class_="_1fQZEK").text
        product_rating = parent_container.find("div", class_="_3LWZlK").text
        product_link = "https://www.flipkart.com" + parent_container.find("a", class_="_1fQZEK")["href"]
        
        # Append the extracted information to the respective lists
        product_names.append(product_name)
        product_ratings.append(product_rating)
        product_links.append(product_link)

# Print product information
for name, rating, price, link in zip(product_names, product_ratings, product_prices, product_links):
    print("Product Name:", name)
    print("Rating:", rating)
    print("Price:", price)
    print("Link:", link)
    print()
