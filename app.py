from flask import Flask, request, render_template
import qrcode
import os #inbuilt libraries

app = Flask(__name__)

@app.route('/qr', methods=['GET', 'POST'])
def showqr():
    if request.method == 'POST':
        url = request.form['url']
        img = qrcode.make(url)
        path = os.path.join('static', 'qr.png')
        img.save(path)
        return render_template('result.html', url=url, image_path=path)
    return render_template('qrform.html')

if __name__ == '__main__':
    app.run(debug=True)
