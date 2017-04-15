'''
Created on Apr 12, 2017

Scans the ODVA vendor lookup site and finds matches for vendor CIP ID's, then stores them in the
vendor database for cross referencing vendor ID's from CIP response to member company names.

@author: Forrest Edwards
'''

import re                   #regular expressions
import requests             #html page retrieval
import sqlite3 as sql       #local db library

# Upper & lower limit of vendor ID's to scan
VMIN = 1
VMAX = 2000

# ODVA vendor lookup page 
site_URL = 'https://marketplace.odva.org/organizations/results'

# Open the local vendor database file and create a cursor
dbconn = sql.connect('vendor.sqlite')
dbcur = dbconn.cursor()

# Create the vendor table if it isn't already there
dbcur.execute('''CREATE TABLE IF NOT EXISTS vendors (vendor_id INTEGER PRIMARY KEY,
                  vendor_name TEXT)''')

# Scan the venodor ID's from VMIN to VMAX
for vendor_ID in range(VMIN,VMAX+1):
    #commit to DB once every 10 vendor ID"s
    if not(vendor_ID % 10 ):dbconn.commit()
    response = requests.get(site_URL, params={'q': str(vendor_ID) })
    #make sure we actually got a valid response
    if (response.status_code == 200):
    #Check to see if the vendor ID wasn't found in the ODVA databasae    
        if re.search ('No results matching the selected filters', response.text):
            print(str(vendor_ID) + " ... not found in ODVA Database")
            continue
        vendor_name = re.findall('organizations\S+?>(.*?)<', response.text)
        print "-----------------------------------------------------------"
        print ("%s: %s" % (str(vendor_ID),vendor_name[0]))
        print "-----------------------------------------------------------"
        dbcur.execute(''' INSERT OR REPLACE INTO vendors (vendor_id, vendor_name)
                      VALUES (?,?)''', (vendor_ID, vendor_name[0]))
        continue
    print("Error " + str(response.status_code))

#final commmit & close
dbconn.commit()
dbconn.close()

   
    