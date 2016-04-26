import requests
from bs4 import BeautifulSoup

def check(tel):
    url = 'http://dslchecker.bt.com/adsl/adslchecker.TelephoneNumberOutput' # Set destination URL here
    r = requests.post(url, data={'TelNo': tel})
    soup = BeautifulSoup(r.content, 'html.parser')

    trs = soup.findAll("tr")
    for tr in trs:
        tds = tr.findAll("td")
        match = False
        if(len(tds) > 8):
    	 continue 
        for td in tds:
            if (match and td.text != '--' and not is_number(td.text)):
                if (td.text != 'Waiting list'):
                    print('Change detected')
                    return 'It looks like the status of fibre broadband has changed! http://dslchecker.bt.com';
                
        	if td.text in ("FTTC Range A (Clean)", "FTTC Range B (Impacted)"):
        		match = True
                
    print ('executed')    
    return 'No change.'

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


