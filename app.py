from flask import Flask, request, render_template, flash
import qrcode
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

@app.route('/', methods=['GET', 'POST'])
def showqr():
    if request.method == 'POST':
        url = request.form['url'].strip()
        # Validate: must start with http:// or https://
        if not (url.startswith("http://") or url.startswith("https://")):
            flash("Invalid URL! Please include http:// or https://")
            return render_template('qrform.html')

        # Generate QR code
        img = qrcode.make(url)
        path = os.path.join('static', 'qr.png')
        img.save(path)
        return render_template('result.html', url=url, image_path=path)
    return render_template('qrform.html')

if __name__ == '__main__':
    app.run(debug=True)
