
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from urls import epg_url
import requests


def get_unique_channels(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise exception for any HTTP error
    
    # Load the XML data
    root = ET.fromstring(response.content)
    
    channels = set()
     
    for program in root.findall('programme'):
        channel = program.get('channel')
        channels.add(channel)
    
    return channels

def find_channels_with_ids(url, unique_ids):
    response = urlopen(url)
    xml_data = response.read()
    root = ET.fromstring(xml_data)
    
    for channel in root.findall('channel'):
        channel_id = channel.get('id')
        if channel_id in unique_ids:
            print(ET.tostring(channel, encoding='unicode'))


unique_channels = get_unique_channels(epg_url)
unique_channel_ids = set(channel.lower() for channel in unique_channels)  # Converting to lowercase for case-insensitive matching

lmx = find_channels_with_ids(epg_url, unique_channel_ids)
print(lmx)


