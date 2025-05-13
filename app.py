#Flask is a class , from flask Library we are importing FLask class, 
from flask import Flask, request, render_template, flash
import qrcode
import os
import re

app = Flask(__name__) # Iits like telling hey flask create a new web application 
app.secret_key = 'your_secret_key'  # Needed for flash messages

# Function to validate URL with strict checks
def is_valid_url(url):
    url = url.strip()
    print("Checking URL:", url)  # Debugging output

    # Check if the URL starts with http:// or https://
    if not url.lower().startswith(('http://', 'https://')):
        return "❌ Please include http:// or https:// at the beginning."  

    # Ensure the URL is a valid domain or IP using regex
    pattern = re.compile(
        r'^(https?://)'                         # http:// or https://
        r'([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'        # Domain name like example.com
        r'(:\d+)?'                               # Optional port
        r'(/.*)?$'                               # Optional path
    )
    if not pattern.match(url):
        return "❌ Invalid URL format!"

    return True  # URL is valid

@app.route('/', methods=['GET', 'POST'])
def showqr():
    if request.method == 'POST':
        url = request.form['url'].strip()
        validation_result = is_valid_url(url)

        if validation_result != True:
            flash(validation_result)
            return render_template('qrform.html')

        # Generate QR Code
        img = qrcode.make(url)
        path = os.path.join('static', 'qr.png')
        img.save(path)
        return render_template('result.html', url=url, image_path=path)

    return render_template('qrform.html')

if __name__ == '__main__':
    app.run(debug=True)
