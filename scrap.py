import http.client
import urllib.parse
from bs4 import BeautifulSoup

class FlipkartProductScraper:
    def __init__(self):
        self.web_url = "www.flipkart.com"

    def setup_connection(self):
        # Set up the connection
        self.conn = http.client.HTTPSConnection(self.web_url)

    def send_get_request(self, search_query):
        # Specify the URL path
        formatted_input = search_query.replace(" ", "+")
        path = f"/search?q={urllib.parse.quote(formatted_input)}"
        # print(path)

        # Send the GET request
        self.conn.request("GET", path)

    def get_response(self):
        # Get the response
        self.response = self.conn.getresponse()

    def read_response_data(self):
        # Read the response data
        self.data = self.response.read()

    def close_connection(self):
        # Close the connection
        self.conn.close()

    def parse_html_content(self):
        # Parse the HTML content using BeautifulSoup
        self.soup = BeautifulSoup(self.data, "html.parser")

    def extract_product_info(self):
        # Extract product names, ratings, and prices
        all_data = self.soup.find_all("div", class_=["_13oc-S"])
        # print(all_data)
        # print(len(all_data))
        # print()
        name = [element.text for i in all_data for element in i.find_all(["div", "a"], class_=["_4rR01T", "s1Q9rs"])]
        # print(len(name),name)
        # print()
        quantity = [element.text for i in all_data for element in i.find_all(["div"], class_=["_3Djpdu"])]
        # print(len(quantity),quantity)
        product_name = [n + ' ' + q for n, q in zip(name, quantity)]
        # print(product_name)
        if len(product_name) == 0:
            product_name = name
        # print(len(product_name),product_name)
        # print()
        product_link = [f"https://{self.web_url}{element['href']}" for i in all_data for element in i.find_all("a", class_=["_1fQZEK", "s1Q9rs"])]
        # print(len(product_link), product_link)
        # print()
        product_image = [element["src"] for i in all_data for element in i.find_all("img", class_="_396cs4")]
        # print(len(product_image), product_image)
        # print()
        product_rating = [element.text for i in all_data for element in i.find_all("div", class_="_3LWZlK")]
        # print(len(product_rating), product_rating)
        # print()
        product_price = [element.text for i in all_data for element in i.find_all("div", class_=["_30jeq3 _1_WHN1","_30jeq3"])]
        # print(len(product_price), product_price)
        product_info = []
        for name, rating, price, image, link in zip(product_name, product_rating, product_price, product_image, product_link):
            product_info.append({
                "Name": name,
                "Rating": rating,
                "Price": price,
                "Image": image,
                "Link": link
            })
        return product_info 

    def scrape_flipkart_product_info(self, search_query):
        self.setup_connection()
        self.send_get_request(search_query)
        self.get_response()
        self.read_response_data()
        self.close_connection()
        self.parse_html_content()
        return self.extract_product_info()


class AmazonProductScraper:
    def __init__(self):
        self.web_url = "www.amazon.in"

    def setup_connection(self):
        # Set up the connection
        self.conn = http.client.HTTPSConnection(self.web_url)

    def send_get_request(self, search_query):
        # Specify the URL path
        formatted_input = search_query.replace(" ", "+")
        path = f"/s?k={urllib.parse.quote(formatted_input)}"
        # print(f"https://{self.web_url}/s?k={path}")

        # Send the GET request
        self.conn.request("GET", path)

    def get_response(self):
        # Get the response
        self.response = self.conn.getresponse()

    def read_response_data(self):
        # Read the response data
        self.data = self.response.read()

    def close_connection(self):
        # Close the connection
        self.conn.close()

    def parse_html_content(self):
        # Parse the HTML content using BeautifulSoup
        self.soup = BeautifulSoup(self.data, "html.parser")
        # print(self.soup)

    def extract_product_info(self):
        # Extract product names, ratings, and prices
        all_data = self.soup.find_all("div", class_=["puis-card-container s-card-container s-overflow-hidden aok-relative puis-include-content-margin puis puis-v2q9dos4w4qqgu20zj8pkw7yd24 s-latency-cf-section puis-card-border","a-section a-spacing-base","puisg-row"])
        # print(all_data)
        # print(len(all_data))
        # print()
        product_name = [element.text for i in all_data for element in i.find_all("span", class_=["a-size-base-plus a-color-base a-text-normal","a-size-medium a-color-base a-text-normal"])]
        # print(len(product_name),product_name)
        product_link = [f"https://{self.web_url}{element['href']}" for i in all_data for element in i.find_all("a", class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")]
        # print(len(product_link), product_link)
        # print()
        product_image = [element["src"] for i in all_data for element in i.find_all("img", class_="s-image")]
        # print(len(product_image), product_image)

        # print()
        product_rating = [element.text for i in all_data for element in i.find_all("span", class_="a-icon-alt")]
        # print(len(product_rating), product_rating)
        # print()
        product_price = [element.text for i in all_data for element in i.find_all("span", class_="a-price-whole")]
        # print(len(product_price), product_price)
        product_info = []
        for name, rating, price, image, link in zip(product_name, product_rating, product_price, product_image, product_link):
            product_info.append({
                "Name": name,
                "Rating": rating,
                "Price": price,
                "Image": image,
                "Link": link
            })
        return product_info 
        
    def scrape_amazon_product_info(self, search_query):
        self.setup_connection()
        self.send_get_request(search_query)
        self.get_response()
        self.read_response_data()
        self.close_connection()
        self.parse_html_content()
        return self.extract_product_info()