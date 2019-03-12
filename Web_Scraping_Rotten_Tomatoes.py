#!/usr/bin/env python
# coding: utf-8

# In[5]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
option = webdriver.ChromeOptions()
option.add_argument(" — incognito")

movie_id = input("Enter a movieID from rotten tomatoes:\n ")
driver = webdriver.Chrome('C:\\Users\\HP\\Downloads\\chromedriver.exe') ### PLEASE CHANGE THE PATH OF CHROMEDRIVER ********* ##
driver.get("https://www.rottentomatoes.com/m/"+movie_id)

# Q1
def getData(movie_id):

    data=[] 
    # your code here
    # click view all
    view_all = driver.find_element_by_css_selector("a[href='/m/"+ movie_id +"/reviews/']") # make universal
    view_all.click()
    
    reviews_element = driver.find_elements_by_xpath("//div[@class='the_review']")
    reviews = [x.text for x in reviews_element]
    
    date_element =driver.find_elements_by_xpath("//div[@class='review_date subtle small']")
    date = [x.text for x in date_element]
    
    stars_element=driver.find_elements_by_xpath("//div[@class='small subtle']")
    stars=[x.text for x in stars_element]
    for i in range(len(stars)):
        if "/" not in stars[i]:
            stars[i]="None"
    data=[]
    for i in range(len(date)):
        data.append((date[i],reviews[i],stars[i].split(" ")[-1]))      
        
    return data

#Q2
def plot_data(data):
    # fill your code here
    rating=[]
    review_factor=[]
    for i in data:
        rating.append((i[2],i[0].split(" ")[2]))  

    for i in rating:
        if "/" in i[0]:
            review_factor.append((i[0].split("/"),i[1]))               
        else:
            review_factor.append("None")                              #list of list with output as [['3', '5'],['3', '5']]
    #print(review_factor)
    review_factor1 = []
    for i in review_factor:
        if i!= "None":
            review_factor1.append((float(i[0][0])*(1/float(i[0][1])) , (int(i[1]))))        #Convert to 0 to 1 scale        
    
    df = pd.DataFrame(review_factor1, columns=['score','year'])
    k=df.groupby('year')['score'].mean()
    plt.axes()
    k.plot(kind='bar')
    plt.title("Average Review of "+movie_id+" per Year")
    plt.xlabel("Year of Review")
    plt.ylabel("Average review on the sacle of 0 to 1")
    plt.figure(figsize=(10,5))
    
    
# Q3
def getFullData(movie_id):
    data=[]
    # fill your code here 
    # Find reviews of the first page seperately as the url is quite different from other urls
    reviews_element = driver.find_elements_by_xpath("//div[@class='the_review']")
    reviews = [x.text for x in reviews_element]
    
    date_element =driver.find_elements_by_xpath("//div[@class='review_date subtle small']")
    date = [x.text for x in date_element]
    
    stars_element=driver.find_elements_by_xpath("//div[@class='small subtle']")
    stars=[x.text for x in stars_element]
    for i in range(len(stars)):
        if "/" not in stars[i]:
            stars[i]="None"
            
    list_information=[]
    for i in range(len(date)):
        list_information.append((date[i],reviews[i],stars[i].split(" ")[-1]))
    
    max_page_num = driver.find_elements_by_xpath("//span[@class='pageInfo']")                    # get total number of pages length
    max_page_num = [x.text for x in max_page_num]
    max_page_num = int(max_page_num[0].split(" ")[-1])
    
    data=[]
    #Links of web pages to crawl
    for i in range(1,max_page_num):
        url="https://www.rottentomatoes.com/m/"+movie_id+"/reviews/?page="+str(i+1)+"&sort="
        driver.get(url)  
        # Contain elements of one page at a time
        reviews_element = driver.find_elements_by_xpath("//div[@class='the_review']")
        reviews = [x.text for x in reviews_element]                                           
        
        date_element =driver.find_elements_by_xpath("//div[@class='review_date subtle small']")
        date = [x.text for x in date_element]
        
        stars_element=driver.find_elements_by_xpath("//div[@class='small subtle']")
        stars=[x.text for x in stars_element]
        for i in range(len(stars)):
            if "/" not in stars[i]:
                stars[i]="None"             
        # print out all the titles.
        for i in range(len(reviews)):
            data.append((date[i],reviews[i],stars[i].split(":")[-1]))  
    data=list_information + data                  # Add first page results here
    driver.close()
    return data   

if __name__ == "__main__":

    # Test 1
    data=getData(movie_id)
    print("\nFirst Page Reviews:\n ",data,"\n")
    
    # Test 2
    plot_data(data)
    
    # Test 3
    data=getFullData(movie_id)
    print("Total Reviews: ",len(data),"\nFirst Review:\n", data[0],"\nLast Review:", data[-1],"\n")
    plot_data(data)

