from bs4 import BeautifulSoup
import re

soup = BeautifulSoup(open('findme.txt'), "html.parser")

#for email in soup.find_all('table'):
#    print email



def get_table_data():
    data = []
    table = soup.find('table')
    table_body = table.find('tbody')

    rows = table_body.find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        tmp = []
        for col in cols:
            if col.find('a'):
                stuff = col.find('a')['href']
                try:
                    result = re.match('^mailto:(.*)', stuff)
                    tmp.append(result.group(1).strip('\n'))
                    continue
                except:
                    tmp.append(stuff.strip('\n'))
                    continue
            else:
                tmp.append(col.text.strip('\n'))

                    
        data.append(tmp)

    return data

def write_table_data(table_list):
    f = open('creators.csv', 'a')
    for row in table_list:
        #a row is a record, remove newlines and write to csv
        tmp = [x.replace('\n', '').encode('utf-8') for x in row]
        line = "|".join(tmp)
        f.write(line + '\n')

        


data = get_table_data()
write_table_data(data)
