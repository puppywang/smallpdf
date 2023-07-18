# -*- coding: utf-8 -*-


from flask import Flask, request, send_file, render_template, render_template_string
from werkzeug.utils import secure_filename
import os
from handler import *
import idna


os.makedirs('uploads', exist_ok=True)
os.makedirs('tmp', exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

def secure_filename_with_chinese(filename):
    encoded_name = filename.encode('idna').decode()
    secure_name = secure_filename(encoded_name)
    return secure_name.encode().decode('idna')

@app.route('/upload', methods=['POST'])
def upload_file():
    quality = int(request.form.get('quality', 50))  # 从表单中获取 quality 参数，如果没有则默认为 50
    if 'file' not in request.files:
        return 'No file part in the request.', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file.', 400
    filename = secure_filename_with_chinese(file.filename)
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(pdf_path)
    image_paths, page_sizes = extract_images_from_pdf(pdf_path, quality)
    output_path = pdf_path.replace('.pdf', '_compressed.pdf')
    images_to_pdf(image_paths, output_path, page_sizes)
    # 删除临时文件
    for path in image_paths:
        os.remove(path)
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Iris 专用的 PDF 压缩器</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    background-color: #f0f0f0;
                }

                .container {
                    text-align: center;
                    background: #fff;
                    padding: 50px;
                    border-radius: 10px;
                    box-shadow: 0px 0px 10px 0px rgba(0,0,0,0.15);
                }

                a {
                    display: inline-block;
                    margin-top: 20px;
                    padding: 10px 20px;
                    background-color: #008CBA;
                    color: white;
                    text-decoration: none;
                }

                a:hover {
                    background-color: #007B9A;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>文件上传并压缩成功</h1>
                <a href="/download/{{ filename }}">点击这里下载《{{ filename }}》</a>
            </div>
        </body>
        </html>
    ''', filename=filename)

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_file(
        os.path.join(app.config['UPLOAD_FOLDER'], filename.replace('.pdf', '_compressed.pdf')),
        as_attachment=True,
    )

@app.route('/')
def upload_page():
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(port=5000)