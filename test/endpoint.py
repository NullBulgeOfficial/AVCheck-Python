import os
import logging
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from avcheck import AvCheckClient
from avcheck.exceptions import (
    AvCheckException,
    ApiKeyMissingException,
    InvalidResponseException,
    InvalidInputException,
    TaskNotFoundException,
    EngineNotFoundException
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB limit

# Initialize AvCheckClient
api_key = os.getenv("AVCHECK_API_KEY")
client = AvCheckClient(api_key)

def scan_file(file_path, detection_threshold=0):
    file_name = os.path.basename(file_path)
    try:
        # Create a new task (file scan)
        new_task_id = client.create_new_task(task_type="file", file_path=file_path)
        logger.info(f"New Task ID: {new_task_id}")

        # Get task data
        task_data = client.get_task_data(new_task_id)
        logger.info("Task Data retrieved successfully.")

        # Check if total detections exceed the threshold
        if client.is_detected(task_data, detection_threshold):
            logger.warning(f"File '{file_name}' exceeds detection threshold.")
            return False

        return True

    except (ApiKeyMissingException, InvalidInputException, InvalidResponseException,
            TaskNotFoundException, EngineNotFoundException, AvCheckException) as e:
        logger.error(f"An error occurred during file scan: {e}")
        return False

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = secure_filename(file.filename)
        file_ext = os.path.splitext(filename)[1].lower()
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Save the file temporarily
        file.save(file_path)

        # Scan the file if it's an executable or installer
        if file_ext in ['.exe', '.msi']:
            logger.info(f"Scanning file: {filename}")
            if not scan_file(file_path, detection_threshold=0):
                os.remove(file_path)
                return jsonify({"error": "File contains malware and was rejected."}), 400

        # Move the file to the final destination
        final_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.rename(file_path, final_path)
        logger.info(f"File uploaded successfully: {filename}")

        return jsonify({"message": "File uploaded successfully", "filename": filename}), 200

    return jsonify({"error": "File upload failed"}), 500

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)