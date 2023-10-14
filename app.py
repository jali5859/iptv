import xml.etree.ElementTree as ET
import requests
from flask import Flask, send_file

app = Flask(__name__)

def remove_channels_without_programs(url):
    # Send a GET request to download the XML file
    response = requests.get(url)
    response.raise_for_status()  # Raise exception for any HTTP error
    
    # Load the XML data
    root = ET.fromstring(response.content)
    
    # Find all channels
    channels = root.findall('.//channel')
    
    # Iterate over channels and check if they have any programs
    for channel in channels:
        programs = channel.findall('programme')
        
        # Remove the channel if it has no programs
        if len(programs) == 0:
            root.remove(channel)
    
    # Save the modified XML file
    modified_xml_data = ET.tostring(root)
    modified_file_path = 'EPG_modified.xml'
    with open(modified_file_path, 'wb') as file:
        file.write(modified_xml_data)
    
    return modified_file_path

@app.route('/epg')
def serve_epg():
    url = 'http://epg.url.com'
    modified_file_path = remove_channels_without_programs(url)
    
    # Serve the modified EPG file
    return send_file(modified_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5500)
