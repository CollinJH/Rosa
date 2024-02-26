from flask import Flask, send_file, jsonify
from swiftclient import Connection
import requests

app = Flask(__name__)

swift_auth_url = 'YOUR_SWIFT_AUTH_URL'
swift_user = 'YOUR_SWIFT_USERNAME'
swift_key = 'YOUR_SWIFT_API_KEY'
swift_tenant_name = 'YOUR_SWIFT_TENANT_NAME'
swift_container_name = 'YOUR_SWIFT_CONTAINER_NAME'

conn = Connection(authurl=swift_auth_url,
                  user=swift_user,
                  key=swift_key,
                  auth_version='3',
                  os_options={"project_id": swift_tenant_name,
                              "user_id": swift_user,
                              "region_name": "YOUR_SWIFT_REGION_NAME"})

# Route to serve the image
@app.route('/image')
def serve_image():
    # Replace 'path_to_your_image.jpg' with the path to your image file
    image_path = 'static/test1.jpg'
    return send_file(image_path, mimetype='image/jpeg')

@app.route('/imageUrls')
def get_image_urls():
    image_urls = [
        "http://127.0.0.1:5000/static/test1.jpg",
        "http://127.0.0.1:5000/static/test3.JPG",
        "http://127.0.0.1:5000/static/test4.jpg"
    ]
    return jsonify(image_urls)

@app.route('/upload_image', methods=['POST'])
def upload_movie():
    if 'movie' not in requests.files:
        return jsonify({'error': 'No file part'}), 400

    file = requests.files['movie']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Upload the file to Swift
    try:
        conn.put_object(container=swift_container_name,
                        obj=file.filename,
                        contents=file.stream.read(),
                        content_type=file.content_type)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'File uploaded successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
