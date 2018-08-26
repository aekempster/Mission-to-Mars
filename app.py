#import dependencies
from flask import Flask, render_template
import scrape
import pymongo


# create Flask app
app = Flask(__name__)

# Mongo Connection
client = pymongo.MongoClient()
db = client.mars_db
collection = db.mars_data_entries

@app.route("/")
def home():
    mars_data = list(db.collection.find())[0]
    return  render_template('index.html', mars_data=mars_data)

@app.route("/scrape")
def web_scrape():
    db.collection.remove({})
    mars_data = scrape.scrape()
    db.collection.insert_one(mars_data)
    return  render_template('scrape.html')

if __name__ == "__main__":
    app.run(debug=True)
