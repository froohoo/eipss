'''
Created on Apr 9, 2017

@author: Forrest Edwards

'''

from cpppo.server import enip
from cpppo.server.enip import client
from dotdict import dotdict


class eipdevice:
    'Ethernet IP Device Object'
    
    def __init__(self, name, host ):
        self.name = name
        self.sin_addr = host
        self.prop = None
    
    def scan(self):
        timeout         = 1.0
        addr            = self.sin_addr
        with client.client( host=addr, udp=True, broadcast=True ) as conn:
            conn.list_identity( timeout = timeout )
            while True:
                response,elapsed= client.await( conn, timeout=timeout )
                if response:
                    self.prop = response
                else:
                    break # No response (None) w'in timeout or EOF ({})
