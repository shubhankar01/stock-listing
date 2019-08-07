import requests, zipfile, io, redis, csv, datetime
from bs4 import BeautifulSoup
from datetime import date

def redis_conn():
    return redis.Redis.from_url('redis://127.0.0.1:6379',db=0,charset='utf-8', decode_responses=True)

def fetch_details_from_bse():
    bse_page = requests.get("https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx")
    bse_content = BeautifulSoup(bse_page.content,'lxml')
    zip_file_link = bse_content.body.find(id = "ContentPlaceHolder1_btnhylZip")['href']
    zip_file = requests.get(zip_file_link)
    z = zipfile.ZipFile(io.BytesIO(zip_file.content))
    z.extractall('zips')
    return str('zips' + '/' + z.namelist()[0])

def update_redis():
    r_conn = redis_conn()
    r_conn.flushall()
    bse_details = fetch_details_from_bse()
    csv_values = csv.DictReader(open(bse_details, 'r'))
    for item in csv_values:
        r_conn.hmset(item['SC_NAME'].rstrip(), dict(item))

def get_top_ten_stocks():
    update_redis()
    r_conn = redis_conn()
    result = []
    stocks = r_conn.keys('*')
    for stock in stocks:
        result.append(r_conn.hgetall(stock))
    result = sorted(result, key=lambda x: (float(x['PREVCLOSE'])-float(x['CLOSE']))/float(x['LAST']))
    return result[0:10]

def get_stock_by_name(stock_name):
    r_conn = redis_conn()
    return r_conn.hgetall(stock_name)
