# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd 
import datetime as dt

def scrape_all():
   # Initiate headless driver for deployment
   browser = Browser("chrome", executable_path="chromedriver", headless=True)
   news_title, news_paragraph = mars_news(browser)
   Cerberus_image=Hemi_image("Cerberus Hemisphere Enhanced")
   Schiaparelli_image=Hemi_image("Schiaparelli Hemisphere Enhanced")
   Syrtis_image=Hemi_image("Syrtis Major Hemisphere Enhanced")
   Valles_image=Hemi_image("Valles Marineris Hemisphere Enhanced")
  
   # Run all scraping functions and store results in dictionary
   data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now(),
      "Cerberus_image":Cerberus_image,
      "Schiaparelli_image":Schiaparelli_image,
      "Syrtis_image":Syrtis_image,
      "Valles_image":Valles_image,
    }
   browser.quit()
   return data

def mars_news(browser):

   # Visit the mars nasa news site
   url = 'https://mars.nasa.gov/news/'
   browser.visit(url)
   
   # Optional delay for loading the page
   browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

   # Convert the browser html to a soup object and then quit the browser
   html = browser.html
   news_soup = BeautifulSoup(html, 'html.parser')
   
   # Add try/except for error handling
   try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
   except AttributeError:
        return None, None
   
   return news_title, news_p

# "### Featured Images"

def featured_image(browser):

  # Visit URL
  url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
  browser.visit(url)


  # Find and click the full image button
  full_image_elem = browser.find_by_id('full_image')
  full_image_elem.click()


  # Find the more info button and click that
  browser.is_element_present_by_text('more info', wait_time=1)
  more_info_elem = browser.find_link_by_partial_text('more info')
  more_info_elem.click()


  # Parse the resulting html with soup
  html = browser.html
  img_soup = BeautifulSoup(html, 'html.parser')


  # Find the relative image url
  try:
     # find the relative image url
     img_url_rel = img_soup.select_one('figure.lede a img').get("src")

  except AttributeError:
     return None


  # Use the base URL to create an absolute URL
  img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
  return (img_url)

def mars_facts():
     #try:
    # use 'read_html" to scrape the facts table into a dataframe
   df = pd.read_html('http://space-facts.com/mars/')[0]
 #except BaseException:
   #return None
   #Assign columns and set index of dataframe
   df.columns=['Description', 'Mars']
   df.set_index('Description', inplace=True)
    
    # Convert dataframe into HTML format, add bootstrap
   return df.to_html()

def Hemi_image(name):
    
  # Visit URL
  url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
  browser = Browser("chrome", executable_path="chromedriver", headless=True)
  browser.visit(url)


  # Find and click the title link
  Hemi_image = browser.find_link_by_partial_text(name)
  Hemi_image.click()
 
    # Find the open button and click that
  Hemi_image1 = browser.find_by_id('wide-image-toggle')
  Hemi_image1.click()

  # Parse the resulting html with soup
  html = browser.html
  soup = BeautifulSoup(html, 'html.parser')

  
  # Find the relative image url
  try:
     # find the relative image url
     img_url_1 = soup.find('img', {"class":"wide-image"})['src']

  except AttributeError:
     return None


  # Use the base URL to create an absolute URL
  img_url1=f'https://astrogeology.usgs.gov{img_url_1}'
  return (img_url1)



if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())