# -*- coding: utf-8 -*-
"""
@author: Manav
"""

import requests 
from bs4 import BeautifulSoup
import numpy as np
import smtplib
import csv 
import datetime
import pandas as pd  
def gogo(): 
    # the website we want to open     
    url='http://gogoanime.io/'
      
    #open with GET method 
    resp=requests.get(url) 
      
    #http_respone 200 means OK status 
    if resp.status_code==200: 
        print("Successfully opened the web page") 
      
        # we need a parser,Python's built-in HTML parser is enough . 
        soup=BeautifulSoup(resp.text,'html.parser')     
  
        # k is the list which contains all the text i.e news  
        today=[] 
        k=soup.find_all("p",{"class":"name"})
        urls=[]
        
        for i in k: 
            today.append(i.text)
            urls.append(str(i))
        
        for i in range(0,len(urls)):
            temp=urls[i].find('href')+6
            urls[i]=urls[i][temp:]
            
        for i in range(0,len(urls)):
            temp=urls[i].find('"')
            urls[i]=urls[i][:temp]
            urls[i]=url+urls[i][1:]
            
        time=[]    
        for i in range(0,len(urls)):
            time.append(datetime.datetime.now())
        
       
        List=list(zip(today,urls,time))
        
        store=pd.DataFrame(List)
        store.columns=['Anime','URL','Time']
      
        #Creates a csv of the new updates
        with open('Gogo.csv', 'r', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            for i in range(0,len(List)):
                wr.writerow(List[i])
        
        # message to be sent 
        message=""
        for i in range(0,len(List)):
            message=message+str(List[i][0])+":"+str(List[i][1])+"\n\n"

        TO = ['abc@gmail.com'] #,'xyz@gmail.com','mno@gmail.com'
        # creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com', 587)
        # start TLS for security 
        s.starttls() 
  
        # Authentication 
        s.login("sender@gmail.com", "YourPassword") 
        BODY='\r\n'.join(['To: %s' % TO,
        'From: %s' % "sender@gmail.com",
        'Subject: %s' % "Today's Anime Updates (Source: "+url+" , Last Updated At: "+ str(datetime.datetime.now().strftime('%A %d %B %Y Time: %H:%M'))+" )",
        '', message])
          
        # sending the mail 
        s.sendmail("sender@gmail.com", TO, BODY) 
        print("Successfully sent the mail")   
        # terminating the session 
        s.quit()            
    else: 
        print("Error") 

def anime():
    gogo()
          
anime()
