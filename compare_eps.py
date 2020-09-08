import re
import requests
from bs4 import BeautifulSoup
import csv

dic = {}
file_name = 'file.txt'
file = open(file_name, 'r')
count = 0
for item in file:
    
    item = item.replace('\n', '')
    id = item.split(',')[0]
    namad = item.split(',')[1]

    url = f'http://www.tsetmc.com/loader.aspx?ParTree=151311&i={id}'


    html_data = requests.get(url).text
    csecval = re.search(r"CSecVal='(\d+)", html_data).group(1)
    i = re.search(r'i=(\d+)', url).group(1)

    sector_pe = re.search(r"SectorPE='(.*?)'", html_data).group(1)
    estimated_eps = re.search(r"EstimatedEPS='(.*?)'", html_data).group(1)


    d = []
    while not d:
        data = requests.get('http://www.tsetmc.com/tsev2/data/instinfodata.aspx', params={'i': i, 'c': csecval}).text
        d = data.split(';')

    try:
        pe = float(d[0].split(',')[3]) / float(estimated_eps)
        ratio = float(pe) / float(sector_pe)

        count += 1
        print(f"{count}")
       
    except Exception:
        pass

    
    dic[namad] = sector_pe, pe, ratio, estimated_eps
sort_orders = sorted(dic.items(), key=lambda x: x[1][2])

ratio_file = open(f'{file_name}.csv', 'a')
writer = csv.writer(ratio_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
writer.writerow(["namad","group p/e","p/e","p/e ratio", "eps", "url"])

for i in sort_orders:
    content = [str(i[0]),str(i[1][0]),str(i[1][1]),str(i[1][2]),str(i[1][3])]
    writer.writerow(content)
print("FILE CREATED")
    