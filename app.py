# import dependencies
from flask import Flask, jsonify, render_template, redirect
import pymongo
import os
import requests
import pandas as pd 
import selenium
from bs4 import BeautifulSoup 
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

#impot the scrape function
import scrape

# Create an app, being sure to pass __name__
app = Flask(__name__)

#################################################
# Database Setup
#################################################
# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database & collection. Will create one if not already available.
db = client.mission_to_mars

#################################################
# Flask Routes
#################################################

# Define what to do when a user hits the homepage / index route
# Create a root route / that will query your Mongo database and pass the mars data 
# into an HTML template to display the data.

@app.route("/")
def index():
    data = db.collection.find_one()
    # Return the template with the mars data passed in
    return render_template('index.html', data=data)

#################################################
# Define scrape route
@app.route("/scrape")
def scrape_info():
    #run scrape function
    data = scrape.scrape()

    # Update the Mongo database using update and upsert=True
    db.collection.update({}, data, upsert=True)

    # Redirect back to home page
    return redirect("/")






if __name__ == "__main__":
    app.run(debug=True)

