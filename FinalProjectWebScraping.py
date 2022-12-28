from bs4 import BeautifulSoup

import requests

import mysql.connector

import time

cnx = mysql.connector.connect(user='root', password='@lexander8891',
                              host='127.0.0.1',
                              database='infoDB')

cursor = cnx.cursor(buffered=True)

print("Please enter your brand: ")

brand = input()

url = 'https://www.truecar.com/used-cars-for-sale/listings/' + brand + "/?page=1"

#https://www.truecar.com/used-cars-for-sale/listings/acura/?page=3

print()
print("Please wait for data gathering.")

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}

webpage = requests.get(url, headers=headers)

soup = BeautifulSoup(webpage.text, 'html.parser')

results = soup.find_all("div", class_ = "card-content vehicle-card-body order-3 vehicle-card-carousel-body")


for i in range(1,20):
    #extract features from html page
    for result in results:
        vehicleMileage = result.find("div", attrs ={'class':"truncate text-xs", 'data-test':"vehicleMileage"}).text
        vehiclePrice = result.find("div", attrs ={'class':"heading-3 my-1 font-bold", 'data-qa':"Heading", 'data-test':"vehicleCardPricingBlockPrice"}).text
        mileage = int(vehicleMileage.split()[0].replace(",", ""))
        #print(mileage)
        price = int(vehiclePrice.replace(",", "").replace("$", ""))
        vehicleCardYearMakeModel =result.find("div", attrs ={'class':"vehicle-card-header w-full", 'data-test':"vehicleCardYearMakeModel"})
        YearMake = int(vehicleCardYearMakeModel.find("span", attrs ={'class':"vehicle-card-year text-xs"}).text)
        Model = vehicleCardYearMakeModel.find("span", attrs ={'class':"truncate"}).text
        #No accidents, 2 Owners, Personal use
        vehicleCardCondition =result.find("div", attrs ={'class':"vehicle-card-location mt-1 text-xs", 'data-test':"vehicleCardCondition"}).text
        lst = vehicleCardCondition.split(',')
        numOfAccidents = 0 if lst[0][0]=='N' else int(lst[0][0])
        numOfOwners = int(lst[1][1])
        currentUse = lst[2]
        cursor.execute("INSERT INTO cars VALUES(\'%s\', \'%i\', \'%i\', \'%i\', \'%s\', \'%i\', \'%i\', \'%s\')" %(brand, mileage, price, YearMake, Model, numOfAccidents, numOfOwners, currentUse))
        cnx.commit()
    url = url[:-1] + f"{i+1}"
    time.sleep(6)
    webpage = requests.get(url, headers=headers)
    soup = BeautifulSoup(webpage.text, 'html.parser')
    results = soup.find_all("div", class_ = "card-content vehicle-card-body order-3 vehicle-card-carousel-body")



"""
CREATE TABLE cars(
brand varchar(20),
mileage int, 
price int,
yearMake int,
model varchar(20),
numOfAccidents int,
numOfOwners int,
currentUse varchar(255)
);
"""

cnx.close()
