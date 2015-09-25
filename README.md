# Price_Alert

This script gets the price of a product from Amazon.com and sends out SMS notification if it finds a good deal.

## How does this work?

* It uses Amazon Product Advertising API to get the product's price.
* If the current price is lower that last purchase's price or yesterday's price, through Twilio, it sends out a text message to the indicated phone numbers.
* It is scheduled to run on every morning by a Cron job.

## Setup

1. Install all [the dependencies](https://github.com/yoavaviram/python-amazon-simple-product-api) for the Amazon API wraper.

2. Install Twilio module: `pip install twilio`

3. Create a new `config.py` file in same directory:
  ```
  # config.py
  # Amazon credentials:
  amazon_key = 'YOUR_AMAZON_KEY'
  amazon_secret = 'YOUR_AMAZON_SECRET_KEY'
  amazon_tag = 'YOUR_AMAZON_ASSOC_TAG'
  
  # Twilio credentials:
  twilio_sid = 'YOUR_TWILIO_SID'
  twilio_token = 'YOUR_TWILIO_TOKEN'
  
  # Phone numbers:
  from_number = '+1 YOUR_TWILIO_PHONE_NUM'
  to_number = '+1 YOUR_PHONE_NUM'
  ```
4. Create a new `value.py` file in the same directory:
  ```
  # value.py
  # Enter your product name here:
  name = 'rapsberry pi'
  
  # Enter the price for this product from your last purchase:
  price = '34.99'
  ```
  
5. Execute the script: `python3 main.py`.

To set up the cron job:

1. Type in `which python3` to get the directory of python3.

2. `crontab -e`

3. This cron job executes the script everyday at 7:30 AM and print the result to a log file:
```
30 7 * * * cd /YOUR_PATH ; /PYTHON3_PATH  main.py > /YOUR_PATH/repport.log 2>&1
```

## Sample output:

```
Best match: Optimum Nutrition Serious Mass, Chocolate, 12 Pound
The current price on Amazon: $47.99 is lower than your last purchase!

Best match: Optimum Nutrition Serious Mass, Chocolate, 12 Pound
The current price on Amazon: $47.99 is lower than yesterday price $51.99
```

