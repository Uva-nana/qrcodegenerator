from flask import Flask, request, render_template, flash
import qrcode
import os
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

# Validate the entered URL
def is_valid_url(url):
    url = url.strip()
    if not url.lower().startswith(('http://', 'https://')):
        return "❌ Please include http:// or https:// at the beginning."
    
    pattern = re.compile(
        r'^(https?://)'
        r'([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'
        r'(:\d+)?'
        r'(/.*)?$'
    )
    if not pattern.match(url):
        return "❌ Invalid URL format!"
    return True

@app.route('/', methods=['GET', 'POST'])
def showqr():
    if request.method == 'POST':
        url = request.form['url'].strip()
        size = int(request.form['size'])  # Get selected QR size
        validation_result = is_valid_url(url)

        if validation_result != True:
            flash(validation_result)
            return render_template('qrform.html')

        # Create QR code with selected size
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=size,
            border=4
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')

        # Save to static folder
        path = os.path.join('static', 'qr.png')
        img.save(path)

        return render_template('result.html', url=url, image_path=path)

    return render_template('qrform.html')

if __name__ == '__main__':
    app.run(debug=True)
