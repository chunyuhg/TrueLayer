# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 00:24:22 2018

@author: User
"""
import sys
import json
import requests
import re
from bs4 import BeautifulSoup
from argparse import ArgumentParser

#check the url is valid
def url_validator(url):
    if(type(url) != str):return False
    if re.match('https?://(?:www)?(?:[\w-]{2,255}(?:\.\w{2,6}){1,2})(?:/[\w&%?#-]{1,300})?',url):
        return True
    else:
        return False

#get the attribute tag
def get_tag_contens(soup,tag_name,tag_class=None):
    try:
        if(tag_class == None):
            content=(soup.find(tag_name).text)
        else:
            content=(soup.find(tag_name,attrs={'class':tag_class}).text)
        if tag_class != 'hnuser':
            content=content.split(' ')[0]     
            content=content.split('.')[0]
        return content 
    except:
        return str(None)

#check the num is digit
def is_digit(num):
    if(str.isdigit(str(num)) and int(num) >= 0):
        return int(num)
    else:return 0
    
if __name__ == "__main__":
    
    #argument description
    parser =ArgumentParser(prog = "posts1",usage = "posts n",
                           description="post the hackernews in json format")
    #add the argument n
    parser.add_argument("--posts",            
                        help="posts how many posts to print. A positive integer <= 100",
                        dest='n',
                        type=int)
    
    arg=parser.parse_args()

    if(arg.n <= 0 or arg.n >100):
        print('n should be a positive integer and bigger than 0.')       
        sys.exit()
    
    #get the input
    n = arg.n
    
    #hacker news url
    hacker_news="https://news.ycombinator.com/"
    nextpage_href="news"
    
    while 1:
        #check internet connection 
        page = requests.get(hacker_news + nextpage_href)        
        
        if(page.status_code != requests.codes.ok):break
    
        soup = BeautifulSoup(page.text,'html.parser')        
        
        #get the webpage titles
        titles = soup.find_all('a',attrs={'class':'storylink'},href=True, text=True)
        
        #get the posts' rank
        ranks = soup.find_all('span',attrs={'class':'rank'})
        
        subtext = soup.find_all('td',attrs={'class':'subtext'})

        num = n
        
        # if n>len(titles): input n is greater than the posts in current webpage
        if (n > len(titles)):
            num = len(titles)
    
        for i in range(0,num):
            title = titles[i].text
            href = titles[i].attrs['href']
            if (url_validator(href) == False):
               href = hacker_news + href
            author = get_tag_contens(subtext[i],'a',tag_class='hnuser')
            score = get_tag_contens(subtext[i],'span')
            score = is_digit(score)
            comment = str(subtext[i].find_all('a')[-1].text.split('\xa0')[0])
            comment = is_digit(comment)
            rank = ranks[i].text.split('.')[0]
            rank = is_digit(rank)

            js = json.dumps({
                           'title':title,
                           'url':href,
                           'author':author,
                           'points':score,
                           'comments':comment,
                           'rank':rank
                        },indent=4)
            print(js)
        
        #if n > len(titles): we need to get the next page's url 
        if(n > len(titles)):
            
            nextlink = soup.find('a',attrs={'class':'morelink'})
            
            #if there is no next page,then break
            if (nextlink==None):
                break
            else:
                nextpage_href = nextlink.attrs['href']
                n = n-len(titles)
        else :break    
         
  