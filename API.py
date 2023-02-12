 # Refference https://www.youtube.com/watch?v=ae62pHnBdAg&ab_channel=BorntoDev

import tweepy
import unittest
import csv
import pandas
from datetime import *  #เอามาทำเวลา
from geopy.geocoders import Nominatim 
import configparser

class Twitter_API():

    def __init__(self,query,lang,since,until):
        config = configparser.ConfigParser()
        config.read('config.ini')

        consumer_key = config['Twitter_API']['consumer_key']
        consumer_key_secret = config['Twitter_API']['consumer_key_secret']

        access_token = config['Twitter_API']['access_token']
        access_token_secret = config['Twitter_API']['access_token_secret']

        self.query = query
        self.lang = lang  #ภาษา th,en
        self.count = 50
        self.since = datetime.strptime(str(since) + " 00:00:00","%Y-%m-%d %H:%M:%S")
        until = datetime.strptime(str(until),"%Y-%m-%d") + timedelta(days = 1)
        self.until = str(until).split(" ")[0]
        self.tweet_mode = "extended"
        self.result_type = "mixed"
        self.auth = tweepy.OAuthHandler(consumer_key,consumer_key_secret)
        self.auth.set_access_token(access_token,access_token_secret)
        self.api = tweepy.API(self.auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
        #self.api = tweepy.API(self.auth,wait_on_rate_limit=True)
        # Write file .csv for checking and record infor
        fieldnames = ['time', 'places', 'tweet']
        self.csvfile = open('C:\\Users\\User\\Documents\\GitHub\\API_Search\\Data\\'+ str(query)+'_Data.csv', 'a', newline='', encoding="utf-8")
        self.writer = csv.DictWriter( self.csvfile, fieldnames=fieldnames )
        self.writer.writeheader()

    def search(self): #Function search word timezone ไม่ห้เหลื่อมกัน 
        start = 0    
        maxId = -1
        Inmediat = 0  
        Stop = True
        while(Stop):
            try:
                if (maxId <= 0 and Inmediat<1):
                    data = self.api.search(q=self.query,
                                        lang=self.lang,
                                        count=self.count,
                                        tweet_mode=self.tweet_mode,
                                        result_type=self.result_type,
                                        until = self.until)
                else:
                    if Inmediat >= 1:
                        data = self.api.search(q=self.query,
                                        lang=self.lang,
                                        count=self.count,
                                        tweet_mode=self.tweet_mode,
                                        result_type=self.result_type,
                                        max_id = str( maxId - 38555555555555 -555555555 - (100000000*Inmediat)),
                                        until = self.until)

                        print(start)
                        start += 1
                        Inmediat +=1
        
                    else:
                        data = self.api.search(q=self.query,
                                        lang=self.lang,
                                        count=self.count,
                                        tweet_mode=self.tweet_mode,
                                        result_type=self.result_type,
                                        max_id = str( maxId - 38555555555555),
                                        until = self.until)
                self.write_csv(data,self.query)

                if(len(data)==0):
                    continue
                maxId = data[-1].id
                start += 1
                Stop = self.write_csv(data,self.query)

            except:
                Inmediat +=1
                start += 1
                
                if start >= 10:
                    Stop = False
        print(start)
        self.csvfile.close()
        print("Finish all of tweet are ",start)

    #Write file csv 
    def write_csv(self, data,query):
        for infor in data:
            data_created_at = datetime.strptime(str(infor.created_at),"%Y-%m-%d %H:%M:%S")
            if( data_created_at < self.since):    #ตัวที่สร้างมาถ้ามีค่าน้อยกว่าขอบเขตเวลาที่ต้องการ มันจะเฟล
                return False

            if(  (not infor.retweeted) and ("RT @" not in infor.full_text)  ):
                self.writer.writerow( {'time': str(infor.created_at), 'places': infor.user.location, 'tweet':infor.full_text} )
        return True

if __name__ == "__main__":

    obj = Twitter_API("ดาว","th","2023-02-10","2023-02-11")
    obj.search()