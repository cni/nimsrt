#!/usr/bin/python
import urllib2

def hit_server(msg):
    urllib2.urlopen('http://127.0.0.1:8080', msg)

hit_server('test whooo')
hit_server(' whooo')
hit_server('test... whooo')

