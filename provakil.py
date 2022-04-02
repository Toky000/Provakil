import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sys

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}
list_of_items = []
try:
    url = sys.argv[1]
except Exception as e:
    print("no url defined/found error in url, terminating program.")
    sys.exit()
try:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    trs = soup.findAll('tr')
    for tr in trs:
        tds = tr.findAll('td')
        if not tds[0].has_attr('colspan'):
            case = tds[1].find('a').text.split("/")
            item_dict = { 
                'item_no': tds[0].text.strip(), 
                'case_type': case[0].strip(),
                'case_id': case[1].strip(),
                'case_year': case[2].strip(),
                'bench': [soup.find('center').find('center').find(text=True, recursive=False).text.strip()],
                'petitioner': tds[2].find(text=True, recursive=False).text.strip(),
                'respondent': str(tds[2]).split("<br/>")[-1].replace("</td>", ""),
                'advocate': tds[3].text.strip(),
                'dated': datetime.today().strftime('%d-%m-%Y')
            }
            list_of_items.append(item_dict)
    print(list_of_items)

except:
    print('unexpected error occured, terminating the program')

'''Command to run:
(for ubuntu) python3 provakil.py https://pvkl.co/bhCA
(for windows) python provakil.py https://pvkl.co/bhCA
Challenges:
getting text with ignoring child text
ignoring selective child text
find element using attribute
ignoring element from list based on attribute

Libraries:
import requests
from bs4 import BeautifulSoup
from datetime import datetime # to get current date and time
import sys # for parameterization'''