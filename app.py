from flask import Flask, request, render_template, flash
import qrcode
import os
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

# Function to validate URL with strict checks
def is_valid_url(url):
    # Check if the URL starts with http:// or https://
    if not url.lower().startswith(('http://', 'https://')):
        return "❌ HTTP/HTTPS missing! Please include http:// or https:// at the beginning."

    # Disallow localhost or private IPs
    blocked_keywords = ['localhost', '127.', '192.168.', '10.', '::1']
    if any(block in url for block in blocked_keywords):
        return "❌ Localhost or private IPs are not allowed."

    # Ensure the URL is a valid domain or IP using regex
    pattern = re.compile(
        r'^(https?://)'                         # http:// or https://
        r'([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'        # Domain name like example.com
        r'(:\d+)?'                               # Optional port
        r'(/.*)?$'                               # Optional path
    )
    if not bool(pattern.match(url)):
        return "❌ Invalid URL format!"

    return True  # URL is valid

@app.route('/', methods=['GET', 'POST'])
def showqr():
    if request.method == 'POST':
        url = request.form['url'].strip()
        validation_result = is_valid_url(url)

        if validation_result != True:
            print("The URL is not valid")
            flash(validation_result)
            return render_template('qrform.html')
        else:
            print("The URL is valid")

        # If URL is valid, generate QR Code
        img = qrcode.make(url)
        path = os.path.join('static', 'qr.png')
        img.save(path)
        return render_template('result.html', url=url, image_path=path)

    return render_template('qrform.html')

if __name__ == '__main__':
    app.run(debug=True)
