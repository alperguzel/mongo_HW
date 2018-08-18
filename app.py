# import necessary libraries
from flask import Flask, render_template, redirect
import scrape_mars
import pymongo

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.mars_db

# create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    # Find data
    information = db.news_mars.find_one(sort=[('_id', pymongo.DESCENDING)])

    # return template and data
    return render_template("index.html", info=information)

@app.route("/scrape")
def scrape():

    mars = scrape_mars.scrape()

    # Store results into a dictionary

    # info = {
    #     "title" : mars["last_news_title"],
    #     "paragraph" : mars["last_news_p"],
    #     "image" : mars["image"],
    #     "weather" : mars["weather"],
    #     "table" : mars["info_table"],
    #     "hems" : mars["hemisphere"]
    # }
    
    
    # Insert forecast into database
    collection = db.news_mars
    collection.insert_one(mars)

    # Redirect back to home page
    return redirect("http://localhost:5000/", code=302)



if __name__ == "__main__":
    app.run(debug=True)
