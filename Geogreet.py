from datetime import date, datetime
import socket
from urllib import request
import geoip2.database as g
from . data import Afrik
from datetime import datetime


def infos_ip(ip)->dict:
    reader = g.Reader('GeoLite2-City.mmdb')
    response = reader.city(ip)
    data={}
    data["iso_code"]=response.country.iso_code
    data["country"]=response.country.name
    data["names"]=response.country.names['zh-CN']
    data["subdiv_name"]=response.subdivisions.most_specific.name
    data["subdiv_iso_code"]=response.subdivisions.most_specific.iso_code
    data["city"]=response.city.name
    data["postal"]=response.postal.code
    data["latitude"]=response.location.latitude
    data["longitude"]=response.location.longitude
    data["isp"]=response.traits.isp
    return data
               

def visitor_ip_address(request): 
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def check(ip)->bool:
    try:
        socket.inet_aton(ip)
        ip_valid = True
    except socket.error:
        ip_valid = False
    return ip_valid


def period(l:int):
    return "matin" if l>=0%24 and l<=11%24 else "aprem" if l>=12%24 and l<=17%24  else "soir" 


def greeT(request)->str:
    if check(visitor_ip_address(request))==True: ip=visitor_ip_address(request)
    else: ip="void"
    __ = {}
    try:
       data=infos_ip(ip)
       __["ip"]=visitor_ip_address(request)
       __["country"], __["city"] = data["country"], data["city"] if data["city"]==data["subdiv_name"] else (data["subdiv_name"], data["city"])
       if not data["country"] in Afrik.keys():
           __["greeting"]=Afrik["default"]["English"]
       else:
           if "aprem" in Afrik[data["country"]].keys():
               __["greeting"]=Afrik[data["country"]][period(datetime.now().hour)]
           else: __["greeting"]=Afrik[data["country"]]["matin"]
    except:
        __["greeting"], __["country"], __["city"] = Afrik["default"]["English"], None, None
    return __

    