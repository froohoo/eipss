
# Main routine to collect user selections and input then call the various functions.



import sqlite3 as sql
from eipdevice import eipdevice
import json
from ipaddr import IPv4Network
from time import sleep

dbfile = "eipss.sqlite"

def newscan(netstr):
    net = IPv4Network(netstr)
    print net
    for address in list(net)[1:-1]:
        print ("Scanning ", address)
        device = eipdevice(str(address),str(address))
        device.scan()
        if device.prop == None:
            print("No eip Device found at ", address)
            continue
        properties = device.prop.enip.CIP.list_identity.CPF.item[0].identity_object
        for item,value in properties.iteritems():
            print ("%s : %s " % (item,value))
        print("-----------------------------------------------")
        dbcur.execute('''INSERT INTO devices (sin_addr, status_word,
               vendor_id,  product_name, sin_port,
               state, version, device_type, sin_family,
               serial_number, prodct_code, product_revision)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''', 
               [properties.sin_addr,
               properties.status_word,
               properties.vendor_id,
               properties.product_name,
               properties.sin_port,
               properties.state,
               properties.version,
               properties.device_type,
               properties.sin_family,
               properties.serial_number,
               properties.product_code,
               properties.product_revision])
        sleep(1)
        print 'commit'
        db.commit()

try:
    db = sql.connect(dbfile)
    dbcur = db.cursor()
    db.execute('''CREATE TABLE IF NOT EXISTS devices (sin_addr TEXT, status_word TEXT,
               extra_array TEXT, vendor_id INTEGER, 
                product_name TEXT, sin_port INTEGER,
               state INTEGER, version INTEGER, device_type INTEGER, sin_family INTEGER,
               serial_number INTEGER, prodct_code INTEGER, product_revision INTEGER)
    ''')
except:
    print "Unable to connect or create device database. Do you have write permissions on this directory?"
print ("Ethernet Industrial Protocol Subnet Scanner\n\n\n\n")

mode = None
while True:
    mode = raw_input(" 1.Scan a New Subnet\n 2.Re-Scan Previous Subnet \n 3.Visualize previously scanned Subnet \n Slection:")
    if mode == '': quit()
    if mode == '1': 
        
        while True:
            targetnetwork = raw_input("Please enter the network in the following format: network/mask (i.e. 192.168.1.0/24")
            if IPv4Network(targetnetwork): newscan(targetnetwork)
            else:break
            
            
            
        
        
    
    
    





