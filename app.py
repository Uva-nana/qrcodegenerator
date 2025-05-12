from flask import Flask, request, render_template, flash
import qrcode
import os
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

def is_valid_url(url):
    # Must start with http:// or https://
    if not url.startswith(('http://', 'https://')):
        return False

    # Disallow localhost or private IPs
    blocked_keywords = ['localhost', '127.', '192.168.', '10.', '::1']
    if any(block in url for block in blocked_keywords):
        return False

    # Very basic pattern for valid domain URLs
    pattern = re.compile(
        r'^https?://'                         # http:// or https://
        r'([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'     # Domain name like example.com
        r'(:\d+)?'                            # Optional port
        r'(/.*)?$'                            # Optional path
    )
    return pattern.match(url)

@app.route('/', methods=['GET', 'POST'])
def showqr():
    if request.method == 'POST':
        url = request.form['url'].strip()

        if not is_valid_url(url):
            flash("❌ Invalid URL! Please enter a valid public URL like https://example.com")
            return render_template('qrform.html')

        img = qrcode.make(url)
        path = os.path.join('static', 'qr.png')
        img.save(path)
        return render_template('result.html', url=url, image_path=path)

    return render_template('qrform.html')

if __name__ == '__main__':
    app.run(debug=True)
