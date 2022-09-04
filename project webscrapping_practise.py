from flask import Flask, request, render_template
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

#source = urllib.request.urlopen('https://www.flipkart.com/search?q="+"iphone11"').read()
#print(source)

app = Flask(__name__)

@app.route('/', methods = ['GET'])
@cross_origin()
def homepage():
    return render_template("index.html")

@app.route('/review', methods = ['POST'])
@cross_origin()
def index():

    if request.method == 'POST':
        searchString = request.form['content'].replace(" ", "")
        flipkart_URL = "https://www.flipkart.com/search?q=" + searchString
        uClient = uReq(flipkart_URL)
        flipkartPage = uClient.read()
        uClient.close()
        flipkart_html = bs(flipkartPage, "html.parser")
        bigboxes = flipkart_html.find_all('div', {"class": "_1AtVbE col-12-12"})
        box = bigboxes[5]
        productLink = "https://www.flipkart.com" + box.div.a['href']
        prodRes = requests.get(productLink)
        prodRes.encoding = 'utf-8'
        prod_html = bs(prodRes.text, "html.parser")
        all_review = prod_html.find_all('div', {"class": "_16PBlm"})
        print(all_review)
        Commenthead = all_review[5].div.find_all('p', {"class": "_2-N8zT"})[0].text
        custComment = all_review[5].div.div.find_all("div", {"class": ""})[0].text
        Name = all_review[0].div.div.find_all("p", {"class":"_2sc7ZR _2V5EHH"})[0].text
        Rating = all_review[0].div.div.div.div.text
        filename = searchString + ".csv"
        fw = open(filename, "w")
        headers = "Product, CommentHead, Comment \n"
        fw.write(headers)
        reviews = []
        for i in all_review:
            Commenthead = i.div.find_all('p', {"class": "_2-N8zT"})[0].text
            custComment = i.div.div.find_all("div", {"class": ""})[0].text
            Name = all_review[0].div.div.find_all("p", {"class": "_2sc7ZR _2V5EHH"})[0].text
            Rating = all_review[0].div.div.div.div.text
            mydict = {"Product": searchString, "CommentHead": Commenthead,
                      "Comment": custComment, "Name": Name, "Rating": Rating}
            reviews.append(mydict)
        return render_template('results.html', reviews=reviews[0:(len(reviews) - 1)])

    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(port = 8008)









