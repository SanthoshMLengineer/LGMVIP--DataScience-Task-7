from os.path import join,isdir
from os import makedirs,listdir,getcwd
from os import remove,scandir

from flask import Flask, request

from flask import jsonify

from recognize_digits import predict_digit
from logging_utils import logger


app = Flask(__name__)
app.secret_key = "super secret key"

path = getcwd()

# file Upload
UPLOAD_FOLDER = join(
				     path,
				     "input_images"
				     )

# Make directory if "uploads" folder not exists
if not isdir(UPLOAD_FOLDER):
    makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# allow files of a specific type
ALLOWED_EXTENSIONS_IMAGE = set(['jpg','png','jpeg'])


# function to check the file extension of image
def allowed_file_image(filename):
    '''
    This function helps to check extension 
    of file image
    Parameters
    -----------
    	filename : str
    		file name with extension
    Returns
    --------
    	True if file having required extention
    '''
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in \
           ALLOWED_EXTENSIONS_IMAGE


@app.route('/recogniseDigits', methods=['GET', 'POST'])
def recognise_digits():
	"""
	This function helps to predict disease.
	Parameters
	----------
		file : object
	Returns
	-----------
		Disease name : str
		Treatment : str
	"""
	if request.method == 'POST':
		if 'file' not in request.files:
			logger.warning("file not found")
			return jsonify(
						   response="file not found",
						   status=404,
						   mimetype='application/json'
						   )

		file = request.files['file']

		if file.filename == '':
			logger.warning("file not found")
			return jsonify(
				 		   response="file not found",
				 		   status=404,
				 		   mimetype='application/json'
				 		   )

		for images in scandir(UPLOAD_FOLDER):
			remove(images.path)


		if file and allowed_file_image(file.filename):

			filename = "input_image.png"
			file.save(join(app.config['UPLOAD_FOLDER'], 
						   filename
						   )
					 )
			logger.info("file saved")
			prediction = predict_digit(filename)
			output_string = prediction[0]
			probability = prediction[1]
			logger.info('prediction successful')
			return jsonify(
				response=str(output_string),
				probability=str(probability),
			    status=200,
			    mimetype='application/json'
				)

		else:
			logger.warning('allowed format of file is jpg,png')
			return jsonify(
			            response="allowed format of file is jpg,png",
				        status=400,
				        mimetype='application/json'
			        )

		

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,
    	debug=True,threaded=True)



