from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests
import time

app = Flask(__name__)


# class for shoes
class Shoe:
    def __init__(self, name1, url, amount):
        self.name = name1
        self.page = url
        self.profit = amount


@app.route("/")
def index():
    # a fake header to be put in request.get method in order to change user agent
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0"}

    # the Urls of the shoes I want to sell
    url1 = ("https://www.ebay.ca/sch/i.html?_from=R40&_trksid=p2334524.m570.l1312&_nkw=jordan+11+legend+blue&_sacat"
            "=93427&LH_TitleDesc=0&_osacat=93427&_odkw=foamposites+one+anthracite")
    url2 = ("https://www.ebay.ca/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=jordan+13+flint&_sacat=93427&LH"
            "_TitleDesc=0&_osacat=93427&_odkw=jordan+12+flint")
    url3 = ("https://www.ebay.ca/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=foamposites+one+anthracite&_s"
            "acat=93427&LH_TitleDesc=0&_osacat=93427&_odkw=foamposites+anthracite")
    url4 = "https://www.ebay.ca/sch/i.html?_from=R40&_trksid=p2499334.m570.l1313&_nkw=jordan+1+spades&_sacat=93427"

    display_shoes = []

    # Put all the shoe objects into a list
    # The number represents the minimum price I want to sell it at
    shoe_list = []
    shoe_list.append(Shoe("Jordan 11 legend blue", url1, 200))
    shoe_list.append(Shoe("Jordan 13 flint", url2, 200))
    shoe_list.append(Shoe("Foamposite anthracite", url3, 600))
    shoe_list.append(Shoe("Jordan 1 spades", url4, 200))
    print("Shoes that can be sold for a profit:")

    # iterate through all the shoes
    for x in shoe_list:
        # get the source code with request and make a bs object to be able to search through it
        source = requests.get(x.page, headers=headers)
        source_text = source.text
        soup = BeautifulSoup(source_text, "html.parser")

        # counter for finding average price for each shoe
        shoe_count = 0
        total_price = 0

        # for each shoe go find all the tags with the price in it
        for sales in soup.find_all("span", {"class": "s-item__price"}):
            if sales.string is not None:

                # When the shoe prices goes over a thousand they add comma so must check for it and then remove it
                # also remove the dollar and Canadian sign
                # We remove this stuff in order to convert the string to Float
                if "," in sales.string:
                    string_price = sales.string.replace("C $", "").replace(",", "")
                else:
                    string_price = sales.string.replace("C $", "")

                num_price = float(string_price)
                total_price += num_price
                shoe_count += 1

        average_price = total_price / shoe_count

        # Check if the average price is less then the selling price if so print it
        if average_price >= x.profit:
            print(round(average_price, 2))
            print(x.page)
            print(" ")
            display_shoes.append(x)

    # return the html template and the items that can be selled
    return render_template("index.html", display_shoes=display_shoes)


if __name__ == "__main__":
    app.run(debug=True)