import os
import requests
import pandas as pd 
import selenium
from bs4 import BeautifulSoup 
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import time 



def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    ###########################
    #connect with Mars News website
    mars_news_url = "https://redplanetscience.com"
    news_response = requests.get(mars_news_url)
    browser.visit(mars_news_url)

    #create variable for soup results
    mars_news_hmtl = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(mars_news_hmtl, "html.parser")
    #print(soup.prettify())
    results = soup.find_all(class_= "col-md-8")
    latest_result = results[0]
    news_title = latest_result.find(class_= "content_title").text
   #print(news_title)
    news_p = latest_result.find(class_= 'article_teaser_body').text
    #print(news_p)
    #print('-------------------')
    latest_news = {"news_title":news_title, "news_p":news_p}
    
    #browser.quit()
    time.sleep(2)
    #############################################
    #Visit the url for the Featured Space Image site here.
    #Use splinter to navigate the site and find the image url for the current Featured Mars Image 
    space_images_url = "https://spaceimages-mars.com/"
    images_response = requests.get(space_images_url)
    browser.visit(space_images_url)

    space_images_hmtl = browser.html
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(space_images_hmtl, "html.parser")
    #print(soup.prettify())

    result = soup.find(class_="headerimage fade-in")
    featured_image_url = space_images_url + result['src']
    #print(featured_image_url)
    
    #browser.quit()
    time.sleep(2)
    ###########################################
    #Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet 
    #including Diameter, Mass, etc
    mars_facts_url = "https://galaxyfacts-mars.com"
    mars_facts_response = requests.get(mars_facts_url)

    mars_facts_tables = pd.read_html(mars_facts_url)
    #mars_facts_tables
    mars_profile_table = mars_facts_tables[1]
    mars_profile_table.rename(columns={0:"Mars Facts"}, inplace = True)
    mars_profile_table.set_index(["Mars Facts"], inplace = True)
    mars_profile_table.index.name = None
    #mars_profile_table
    
    #Use Pandas to convert the data to a HTML table string.
    mars_profile_html_table = mars_profile_table.to_html(classes = "table table-condensed table-striped table-bordered ", header= False)

    ##############################################
    #Visit the astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
    #You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image
    mars_images_url = "https://marshemispheres.com/"
    browser.visit(mars_images_url)
    mars_images_hmtl = browser.html
    soup = BeautifulSoup(mars_images_hmtl, "html.parser")
    #print(soup.prettify())

    #This list will contain one dictionary for each hemisphere.
    hemisphere_image_urls = []

    hemispheres = soup.find_all(class_= "description")

    for hemisphere in hemispheres:
        #find and click the link to the hemisphere
        link = (hemisphere.find('a')['href'])
        browser.visit('https://marshemispheres.com/' + link)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        #find image url & title
        img_url = soup.find(class_= "wide-image")['src']
        title = soup.find('h2', class_ = "title").text
        title = title.split()
        #print(title[0] + " " + title[1])
        #print(img_url)
    
        #Append the dictionary with the image url string and the hemisphere title to a list.
        dict = {"title" : title[0] + " " + title[1], "img_url": mars_images_url + img_url}
        hemisphere_image_urls.append(dict)
        
        #browser.quit()
        time.sleep(2)
        ##############################################
    #return results
    
    # create dict for results
    scrape_results = {"latest_news": latest_news, "featured_image_url": featured_image_url, 
          "mars_profile_html_table":mars_profile_html_table,
           "hemisphere_image_urls":hemisphere_image_urls}
    
    #return scrape_results
    return scrape_results
    
    browser.quit()