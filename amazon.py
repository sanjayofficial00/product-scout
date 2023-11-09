import http.client
import urllib.parse
from bs4 import BeautifulSoup

# Set up the connection
conn = http.client.HTTPSConnection("www.amazon.in")
print(conn)

# Specify the URL path
search_input = "iphone 14 pro max"
formatted_input = search_input.replace(" ", "+")
path = f"/s?k={urllib.parse.quote(formatted_input)}"

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

# Extract product names, ratings, and prices
product_names = [element.text for element in soup.find_all("span", class_="a-size-medium a-color-base a-text-normal")]
product_ratings = [element.text for element in soup.find_all("span", class_="a-icon-alt")]
product_prices = [element.text for element in soup.find_all("span", class_="a-price-whole")]

# Extract product links
product_links = []
product_containers = soup.find_all("div", class_="puis-card-container s-card-container s-overflow-hidden aok-relative puis-include-content-margin puis puis-v2q9dos4w4qqgu20zj8pkw7yd24 s-latency-cf-section puis-card-border")
for container in product_containers:
    link_element = container.find("a", class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")
    if link_element:
        product_links.append("https://www.amazon.in" + link_element["href"])
    else:
        product_links.append("Link not found")

# Print product information
for name, rating, price, link in zip(product_names, product_ratings, product_prices, product_links):
    print("Product Name:", name)
    print("Rating:", rating)
    print("Price:", price)
    print("Link:", link)
    print()
