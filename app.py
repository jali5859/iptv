import xml.etree.ElementTree as ET
from flask import Flask, send_file
import requests

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

def download_m3u_file():
    url = 'http://url.com'
    filename = 'tv_original.m3u'
    response = requests.get(url)
    with open(filename, 'w') as f:
        f.write(response.text)

@app.route('/epg')
def serve_epg():
    url = 'https://epgurl.com'
    modified_file_path = remove_channels_without_programs(url)
    # Serve the modified EPG file
    return send_file(modified_file_path, as_attachment=True)

@app.route('/tv')
def generate_tv_m3u():
    download_m3u_file()
    serve_epg()
    m3u_file = 'tv_original.m3u'
    epg_file = 'EPG_modified.xml'
    
    # Load the m3u file
    with open(m3u_file, 'r') as f:
        m3u_data = f.readlines()

    # Load the EPG.xml file
    tree = ET.parse(epg_file)
    root = tree.getroot()

    # Extract the channel names from the EPG.xml file
    epg_channels = set()
    for programme in root.iter('programme'):
        channel_id = programme.attrib['channel']
        epg_channels.add(channel_id)

    # Filter the channels in the m3u file
    filtered_channels = []
    flag = False
    for line in m3u_data:
        if line.strip() == '#EXTM3U':
            filtered_channels.append(line)
        elif line.startswith('#EXTINF'):
            flag = True
            channel_id = line.split('tvg-id="')[1].split('"')[0].strip()
            if channel_id in epg_channels:
                filtered_channels.append(line)
            else:
                flag = False
        else:
            if flag:
                filtered_channels.append(line)

    # Write the filtered channels to a new m3u file
    with open('tv_new.m3u', 'w') as f:
        for line in filtered_channels:
            f.write(line)

    return send_file('tv_new.m3u', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5500)
