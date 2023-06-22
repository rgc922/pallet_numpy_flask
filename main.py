from flask import Flask, render_template, request, \
                    flash, get_flashed_messages, redirect

from werkzeug.utils import secure_filename

from PIL import Image

import numpy as np

import os



app = Flask(__name__)

### esto es para el Flask, sin esto genera error
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'


IMG_FOLDER = os.path.join('static', 'image')
app.config['UPLOAD_FOLDER'] = IMG_FOLDER



ALLOWED_EXT = {'jpg', 'jpeg', 'bmp', 'gif', 'tif', 'png'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


# def rgb_to_hex(r, g, b):
#     return '#{:02x}{:02x}{:02x}'.format(r, g, b)


@app.route("/", methods=['GET', 'POST'])
def home():
    
    if request.method == 'POST':

        ### check if the post request has the file

        if 'upfile' not in request.files:
            flash('No file part')
            print("Primer if")
            print(request.url)
            return redirect(request.url)


        file = request.files['upfile']  
        ### if the user does not select a file
        ### the browser submits an empty file without name
        if file.filename == '':
            flash('No selected file')
            return redirect (request.url)


        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'user_image.jpeg'))
            # file.save()
            ### pendiente para guardar la foto y mostrarla


            img = Image.open(file)

                    
            im_matrix = np.array(img)
         

            x_y = im_matrix.shape[0] * im_matrix.shape[1]

            reshape = np.reshape(im_matrix, (x_y, 3))

            
            unique, counts = np.unique(reshape, return_counts=True, axis=0)



            print("Primeros 10", unique[counts.argsort()][0:9])
            print()
            print("Ultimos 10 Estos son los mas comunes", unique[counts.argsort()][-10:-1])

            color_list = []

            for item in unique[counts.argsort()][-50:-1]:
                color_list.append(item)

            image = os.path.join(app.config['UPLOAD_FOLDER'], 'user_image.jpeg')
   
            return render_template('index.html', image=image, colors=color_list) 
                        
        else:
            flash('File not valid')
                        
            image = os.path.join(app.config['UPLOAD_FOLDER'], 'try_me.jpg')
            color_list = []
            return render_template('index.html', image=image, colors=color_list) 
    



    image = os.path.join(app.config['UPLOAD_FOLDER'], 'try_me.jpg')
    # print(type(image))
    color_list = []
    return render_template('index.html', image=image, colors=color_list) 



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True,use_reloader=False)