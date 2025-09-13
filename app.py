from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename
import os
from gan_model import generate_synthetic_image
from utils import preprocess_image, allowed_file, evaluate_image, get_image_metadata
from classifier import predict_disease

UPLOAD_FOLDER = 'static/uploads'
GENERATED_FOLDER = 'static/generated'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['GENERATED_FOLDER'] = GENERATED_FOLDER
app.secret_key = 'your_secret_key'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        disease = request.form.get('disease')
        file = request.files.get('image')
        if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            preprocessed_img = preprocess_image(filepath)
            metadata = get_image_metadata(filepath)
            health_issue = predict_disease(preprocessed_img)
            gen_img_path = generate_synthetic_image(preprocessed_img, disease, app.config['GENERATED_FOLDER'])
            fid, ssim = evaluate_image(preprocessed_img, gen_img_path)
            return render_template('result.html',
                                   gen_img=gen_img_path,
                                   fid=fid,
                                   ssim=ssim,
                                   metadata=metadata,
                                   health_issue=health_issue)
        else:
            flash('Invalid file type or no file uploaded.')
            return redirect(request.url)
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['GENERATED_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
