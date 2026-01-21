from flask import Flask, render_template, request, abort, send_file
import os

app = Flask(__name__)  

UPLOAD_FOLDER = 'data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/uploadfile", methods=['POST'])
def about():
    if request.method == 'POST':
            uploaded_files = request.files.getlist("file")
            for uploaded_file in uploaded_files:
                filename = uploaded_file.filename
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                uploaded_file.save(file_path)
            return "Файлы успешно загружены в папку 'data'!"

@app.route("/list")
def contact():
    path = "data"
    tree = dict(name=path, children=[])
    try: lst = os.listdir(path)
    except OSError:
        pass
    else:
        for name in lst:
            fn = os.path.join(path, name)
            if os.path.isdir(fn):
                tree['children'].append(make_tree(fn))
            else:
                tree['children'].append(dict(name=fn))
    return tree

@app.route("/download/<filename>")
def download_file(filename):
    path = "data"
    file_path = os.path.join(path, filename)
    
    if not os.path.exists(file_path):
        abort(404, description="Файл не найден")
        
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True) 