from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def search_flipkart():
    new_list = []

    if request.method == 'POST':
        search_input = request.form['title']
        formatted_input = search_input.replace(" ", "+")

        url = f"https://www.flipkart.com/search?q={formatted_input}"
        r = requests.get(url)

        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            product_names = soup.find_all("div", class_="_4rR01T")
            product_prices = soup.find_all("div", class_="_30jeq3")
            product_ratings = soup.find_all("div", class_="_3LWZlK")

            for name, price, rating in zip(product_names, product_prices, product_ratings):
                product_info = {
                    "Name": name.text.strip(),
                    "Price": price.text,
                    "Rating": rating.text
                }
                new_list.append(product_info)
        else:
            new_list = ["Failed to retrieve data. Status code: " + str(r.status_code)]

    return render_template("index.html", new_list=new_list)

if __name__ == "__main__":
    app.run(debug=True)
