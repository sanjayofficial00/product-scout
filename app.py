from flask import Flask, render_template, request
import requests
import http.client
import urllib.parse
from bs4 import BeautifulSoup
from jinja2 import Template
# from scrap import *
import scrap

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def search():
    flipkart_product_info_list = []
    amazon_product_info_list = []
    # iteams = []
    if request.method == 'POST':
        search_query = request.form['title']
        print(f"https://www.flipkart.com/search?q={search_query.replace(' ', '+')}")
        print(f"https://www.amazon.in/s?k={search_query.replace(' ', '+')}")

        flipkart_product_info_list = scrap.FlipkartProductScraper().scrape_flipkart_product_info(search_query)
        amazon_product_info_list = scrap.AmazonProductScraper().scrape_amazon_product_info(search_query)
         # Combine the lists before rendering the template
        # combined_data = list(zip(flipkart_product_info_list, iteams))

    return render_template("index.html", flipkart_product_info_list=flipkart_product_info_list, amazon_product_info_list = amazon_product_info_list)

if __name__ == "__main__":
    app.run(debug=True)
