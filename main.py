import sys
import os.path
import config
import value
from amazon.api import AmazonAPI
from twilio.rest import TwilioRestClient

amazon = AmazonAPI(config.amazon_key, config.amazon_secret, config.amazon_tag)
twilio = TwilioRestClient(config.twilio_sid, config.twilio_token) 

def getProduct(productName):
  try:
    product = amazon.search_n(1, Keywords=productName, SearchIndex='All')
    return product
  except:
    print ("Product not found")
    sys.exit()

def getPriceStatus(price1, price2, product):
  if (price1 > product):
    return 1  # When current deal is cheaper than last purchase
  elif (price2 > product):
    return 2  # When current deal is cheaper than yesterday deal
  else:
    return 0

def isValidPrice(num):
  try:
    float(num)
    return True
  except ValueError:
    return False
    
def getLastPrice(product):
  if (os.path.exists('price_values.txt')):
    file = open('price_values.txt')
    lines = file.readlines()
    last_price = float(lines[-1])
  else:
    last_price = product
  return last_price
  
def sendMessage(status, product, lastPrice):
  product_name = product[0].title
  product_price = (product[0].price_and_currency)[0]
  
  if (status == 1):
    message = twilio.messages.create(body="The current price on Amazon for " 
              + product_name + " $" + str(product_price) + " is lower than your last purchase: $"
              + value.price, from_=config.from_number, to=config.to_number)
  elif (status == 2):
    message = twilio.messages.create(body="The current price on Amazon for " 
              + product_name + " $" + str(product_price) + " is lower than yesterday price: $"
              + str(lastPrice), from_=config.from_number, to=config.to_number)
    



# --------------------------------------------------------

name = value.name
price = value.price

product = getProduct(value.name)
product_price = (product[0].price_and_currency)[0]

print ("Best match: " + product[0].title)

if isValidPrice(price):
  price = float(price)
else:
  price = product_price
    
lastPrice = getLastPrice(product_price)
status = getPriceStatus(price, lastPrice, product_price)

if (status != 0):
  if (status == 1):
    print ("The current price on Amazon: " + "$" 
           + str(product_price) + " is lower than your last purchase!")
    sendMessage(1, product, lastPrice)
  elif (status == 2):
    print ("The current price on Amazon: " + "$" 
           + str(product_price) + " is lower than yesterday price $" + str(lastPrice))
    sendMessage(2, product, lastPrice)
    
  outputFile = open('price_values.txt', 'a')
  outputFile.write(str(product_price) + '\n')
  outputFile.close()
else:
  print ("Nothing to report")
  
  




  
