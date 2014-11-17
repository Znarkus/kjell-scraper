#
# import http.cookiejar, urllib.request
# cj = http.cookiejar.CookieJar()
# opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
#
# r = opener.open("http://example.com/")

import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import xlsxwriter
import os
import argparse

parser = argparse.ArgumentParser(description='Hämta lagerstatus för alla butiker och exportera till XLSX')
parser.add_argument('url', help='URL till produkt')

args = parser.parse_args()

# url = 'http://www.kjell.com/sortiment/dator-kringutr-adaptrar/dvi/dvi-till-hdmi/hdmi-dvi-kabel-20-m-p98381'
# url = 'http://www.kjell.com/sortiment/dator-kringutrustning/kablar-adaptrar/dvi/dvi-till-hdmi/hdmi-dvi-kabel-15-m-p98380'
# url = 'http://z.markushedlund.se/dump.php';

# requests_cache.install_cache('demo_cache')
s = requests.Session()
s.headers.update({
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36',
    'Origin':urlparse(args.url).netloc,
    'Referer':args.url
})

r = s.get(args.url)
soup = BeautifulSoup(r.text)
productName = soup.select('.info-container h1')[0].string
stores = []

for option in soup.select('select.storesList option'):
    if (option['value'].isdigit() and int(option['value']) > 0):
        # print(option['value'])
        stores.append({
            'id': int(option['value']),
            'lat': option['data-lat'],
            'long': option['data-long'],
            'name': option.string.strip()
        })

# print(r.text)

# cookies = r.cookies
# cookies['SelectedStore'] = 25
# cookies['FilterInStockSelectedStore'] = 25
# table = PrettyTable(['Product', 'City', 'Stock'])
# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook(os.path.basename(args.url) + '.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write(0, 0, 'Name')
worksheet.write(0, 1, 'Store')
worksheet.write(0, 2, 'Stock')
worksheet.write(0, 3, 'Lat')
worksheet.write(0, 4, 'Long')
remove = ['Slutsåld, utgått ur sortiment', 'N/A']
row = 1

for i, store in enumerate(stores):
    s.cookies['SelectedStore'] = str(store['id'])
    s.cookies['FilterInStockSelectedStore'] = str(store['id'])

    r = s.post(
        args.url,
        {'param':store['name'], 'changeStore':'true'},
        headers={'X-Requested-With':'XMLHttpRequest'}
    )

    soup = BeautifulSoup(r.text)
    storeStock = soup.select('#StockStatus .store')[1]
    stockAmount = storeStock.select('.amount')
    stores[i]['stockAmount'] = stockAmount[0]['data-title'] if stockAmount else 'N/A'
    # storeStock.select('.amount')

    if store['stockAmount'] not in remove:
        print(productName + ': ' + store['name'] + ' – ' + store['stockAmount'])

        # table.add_row([productName, store['name'], store['stockAmount']])
        worksheet.write(row, 0, productName)
        worksheet.write(row, 1, store['name'])
        worksheet.write(row, 2, store['stockAmount'])
        worksheet.write(row, 3, store['lat'])
        worksheet.write(row, 4, store['long'])
        row += 1


# sys.setrecursionlimit(1500)
# print(table)
workbook.close()