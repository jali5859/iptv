from flask import Flask, send_file

app = Flask(__name__)

@app.route('/tv')
def play():
    # Specify the filename of the m3u file
    file_path = 'tv.m3u'

    # Render the m3u file as a response
    return send_file(file_path, as_attachment=True)

@app.route('/epg')
def epgplay():
    # Specify the filename of the m3u file
    file_path = 'EPG.xml'

    # Render the m3u file as a response
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5500)
