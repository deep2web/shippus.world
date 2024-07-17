from flask import Flask, send_from_directory, request  # Import request
from flask_restx import Api, Resource, fields
from flask_swagger_ui import get_swaggerui_blueprint
import os
import pymupdf
import random
import string
from google.cloud import storage

# Initialize Flask app
app = Flask(__name__)
api = Api(app, version='1.0', title='API für Paketlabel', description='Eine API zum Hochladen und Verarbeiten von Paketlabels')

# Configure storage bucket
storage_client = storage.Client()
bucket_name = 'your-bucket-name'  # Replace with your actual bucket name
bucket = storage_client.bucket(bucket_name)

# Define upload and processed folders
UPLOAD_FOLDER = './uploads'
PROCESSED_FOLDER = './processed'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# Swagger UI setup
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

# Define parser for file uploads
upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type='file', required=True)

# Upload endpoint
@api.route('/upload')
class Upload(Resource):
    @api.expect(upload_parser)
    def post(self):
        # Get the file from the request data
        file = request.files['file']  # Access the file from the request data

        if file.filename == '':
            return 'No file selected', 400

        # Check if the file is a PDF
        if not file.filename.lower().endswith('.pdf'):
            return 'Only PDF files are allowed', 400

        # Generate 5 random letters
        random_letters = ''.join(random.choice(string.ascii_letters) for i in range(5))

        # Add random letters to the filename
        filename = file.filename.replace('.pdf', f'-{random_letters}.pdf')

        print(f"Received file with filename: {file.filename}")
        print(f"New filename: {filename}")

        # Save the file to the temporary upload folder
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(f"File saved to: {os.path.join(app.config['UPLOAD_FOLDER'], filename)}")

        # Process the file
        process_file(filename)

        # Upload the processed file to Cloud Storage
        blob = bucket.blob(filename.replace(".pdf", "-4x6.pdf"))
        blob.upload_from_filename(os.path.join(app.config['PROCESSED_FOLDER'], filename.replace(".pdf", "-4x6.pdf")))

        # Return success message
        return 'File processed and uploaded to Cloud Storage successfully', 200

# File processing function
def process_file(filename):
    origfile = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # GLS-to-4x6 processing
    doc = pymupdf.open(origfile)  # open document
    page = doc[0]  # get the 1st page of the document
    page.set_cropbox(pymupdf.Rect(21, 101, 277, 250))  # set a cropbox for the page
    doc.save(origfile.replace(".pdf", "-1.pdf"))

    doc = pymupdf.open(origfile)  # open document
    page = doc[0]  # get the 1st page of the document
    page.set_cropbox(pymupdf.Rect(318.7, 55.4, 575.3, 279.29))  # set a cropbox for the page
    doc.save(origfile.replace(".pdf", "-2.pdf"))

    doc_a = pymupdf.open(origfile.replace(".pdf", "-1.pdf"))  # open the 1st document
    doc_b = pymupdf.open(origfile.replace(".pdf", "-2.pdf"))  # open the 2nd document

    doc_a.insert_pdf(doc_b)  # merge the docs
    doc_a.save(origfile.replace(".pdf", "-1+2.pdf"))  # save the merged document with a new filename

    # Open the document
    doc = pymupdf.open(origfile.replace(".pdf", "-1+2.pdf"))

    # Create a new empty document
    new_doc = pymupdf.open()

    # Iterate through the document page by page
    for i in range(0, len(doc), 2):
        # Create a new page in the new document
        page = new_doc.new_page(-1, width=287.76978417266184, height=431.65467625899277)

        # Add the current page
        rect = pymupdf.Rect(15.88, 10, 271.88, 159)
        page.show_pdf_page(rect, doc, i)

        # Add the next page
        rect = pymupdf.Rect(15.58, 159, 272.18, 382.89)
        page.show_pdf_page(rect, doc, i + 1)

    # Save the new document
    new_doc.save(os.path.join(app.config['PROCESSED_FOLDER'], filename.replace(".pdf", "-4x6.pdf")))

    # Cleanup temporary files
    os.remove(origfile.replace(".pdf", "-1.pdf"))  # cleanup
    os.remove(origfile.replace(".pdf", "-2.pdf"))  # cleanup
    os.remove(origfile.replace(".pdf", "-1+2.pdf"))  # cleanup

    # Delete the original file from the upload folder
    os.remove(origfile)

# Download endpoint
@api.route('/download/<filename>')
class Download(Resource):
    def get(self, filename):
        # Download the file from Cloud Storage
        blob = bucket.blob(filename)
        blob.download_to_filename(os.path.join(app.config['PROCESSED_FOLDER'], filename))

        # Return the downloaded file
        return send_from_directory(app.config['PROCESSED_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
