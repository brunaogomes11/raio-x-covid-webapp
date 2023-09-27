# Start Server
from app.covid import classificar_imagem, transform_imagem
import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'app/static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    dir = os.listdir(app.config['UPLOAD_FOLDER'])
    for i in range(0, len(dir)):
        os.remove(app.config['UPLOAD_FOLDER']+dir[i])
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        imagem = request.files.get('file')
        if not imagem:
            return
        filename = secure_filename("uploads/"+imagem.filename)
        imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        resultado = classificar_imagem(imagem)
        if resultado == 0:
            resultado = 'Resultado: Covid'
        elif resultado == 1:
            resultado = 'Resultado: PNEUMONIA não detectada e COVID não detectado'
        elif resultado == 2:
            resultado = 'Resultado: Pneumonia'
        return render_template('result.html', result=resultado, filename=filename)
    return render_template('index.html')

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='/uploads/' + filename), code=301)

@app.route("/uploadImage", methods=['GET','POST'])
def imageUpload():
    uploaded_file = request.files.get('uploaded_file')
    if uploaded_file:
        resultado = classificar_imagem(uploaded_file)
        if resultado == 0:
            resultado = 'Resultado: Covid'
        elif resultado == 1:
            resultado = 'Resultado: Pneumonia não detectada e Covid não detectado'
        elif resultado == 2:
            resultado = 'Resultado: Pneumonia'
    return {"message": resultado}

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
    
