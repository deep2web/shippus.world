from flask import Flask, send_from_directory, request  # Import request
from flask_restx import Api, Resource, fields
from flask_swagger_ui import get_swaggerui_blueprint
import os
import pymupdf


app = Flask(__name__)
api = Api(app, version='1.0', title='API für Paketlabel', description='Eine API zum Hochladen und Verarbeiten von Paketlabels')

UPLOAD_FOLDER = './uploads'
PROCESSED_FOLDER = './processed'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be served at {SWAGGER_URL}/dist/
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "API für Paketlabel"
    },
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type='file', required=True)

@api.route('/upload')
class Upload(Resource):
    @api.expect(upload_parser)
    def post(self):
        # Get the file from the request data
        file = request.files['file']  # Access the file from the request data

        if file.filename == '':
            return 'No file selected', 400

        filename = file.filename
        print(f"Received file with filename: {filename}")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(f"File saved to: {os.path.join(app.config['UPLOAD_FOLDER'], filename)}")
        process_file(filename)
        return 'File processed successfully', 200


def process_file(filename):
    origfile = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    doc = pymupdf.open(origfile) # open document
    # ... rest of your processing code here ...
    # make sure to save the final file to the PROCESSED_FOLDER

@api.route('/download/<filename>')
class Download(Resource):
    def get(self, filename):
        return send_from_directory(app.config['PROCESSED_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)