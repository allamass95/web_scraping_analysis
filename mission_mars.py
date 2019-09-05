

from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import time 
import pandas as pd

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return(Browser('chrome', **executable_path, headless=False))


def scrape():
    
    dictionary={}
    
    url='https://mars.nasa.gov/news/'
    response=requests.get(url)

    soup=bs(response.text,'html.parser')

    container=soup.find_all('div',class_='slide')


    news_title=container[0].find_all('div',class_='content_title')[0].a.text.strip()
    news_p=container[0].find_all('div',class_='rollover_description_inner')[0].text.strip()
    
    dictionary['title']=news_title
    dictionary['paragraph']=news_p
    
    
    
    
    
    browser=init_browser()
    
    mars_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(mars_url)
    time.sleep(3)
    
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(3)
    
    browser.click_link_by_partial_text('more info')
    time.sleep(3)
    
    browser.click_link_by_partial_text('.jpg')
    time.sleep(3)

    html = browser.html
    soup = bs(html, 'html.parser')

    featured_image_url=soup.body.img['src']
    
    dictionary['image_url']=featured_image_url
    
    
    
    
    
    
    time.sleep(3)
    twitter_url='https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
   
    html = browser.html
    soup = bs(html, 'html.parser')
    time.sleep(3)
    twitter=soup.find_all('div',class_='js-tweet-text-container')[1].p
    time.sleep(2)
    for i in twitter:
    
        mars_weather=i
        dictionary['weather']=mars_weather
        break
       
    
    
    
    
    
    space_url='https://space-facts.com/mars/'
    browser.visit(space_url)
    time.sleep(2)
    data=pd.read_html(space_url)[0]
    data=data.rename(columns={'Mars - Earth Comparison':''})
    data=data.set_index('')
    data=data.to_dict()
    dictionary['Mars_Earth']=data    
        
    
    
    
    
    
    
    astrology_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(astrology_url)
    
    html = browser.html
    soup = bs(html, 'html.parser')
    
    partial_link=soup.find_all('div',class_='description')
    
    list_link=[]   
    for i in partial_link:
            list_link.append(i.a.h3.text)
    for i in range(4):
    
        #initiate browser
        browser.visit(astrology_url)
    
    #print title
            
        title=list_link[i]
    
    # press link button
        browser.click_link_by_partial_text(list_link[i])
    
    # parse new webpage
        html = browser.html
        soup = bs(html, 'html.parser')
    
    #print img_url
        img_url=soup.find_all('div',class_='content')[0].dl.a['href']
    
    #set up dictionaries and append to list
        
        dictionary['img_url']=soup.find_all('div',class_='content')[0].dl.a['href']
        dictionary['name']=list_link[i]
        
    
    
    browser.quit()
    return(dictionary)




