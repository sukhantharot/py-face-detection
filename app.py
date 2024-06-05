from flask import Flask, request, jsonify, send_file
import main
import os

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello Flask'

@app.route('/detection_face', methods=['POST'])
def detection_face():
    # Get image URL and save path from request data
    image_url = request.json.get('image_url')
    save_dir = request.json.get('save_dir')
    padding = request.json.get('padding', 10)  # Default padding to 10 if not provided

    if not image_url or not save_dir:
        return jsonify({'error': 'Missing required data (image_url, save_dir)'}), 400

    # Create the save directory if it does not exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    try:
        # Download the image and extract faces with padding
        main.download_and_extract_faces(image_url, save_dir, padding)

        face_images = sorted(os.listdir(save_dir))
        if face_images:
          first_face_image_path = os.path.join(save_dir, face_images[0])
          return send_file(first_face_image_path, mimetype='image/jpeg')
        return jsonify({'message': 'Faces extracted and saved successfully'}), 200

    except Exception as e:
        print(f"Error during face extraction: {e}")
        return jsonify({'error': 'An error occurred during processing'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Adjust port as needed
