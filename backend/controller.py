from flask import Flask, request, jsonify
from flask_cors import CORS
from image_agent import analyze_image
from text_agent import analyze_description
from reverse_image_search import search_web_image
import json

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from your mobile app

@app.route('/submit', methods=['POST'])
def submit():
    title = request.form.get('title')
    description = request.form.get('description')
    image = request.files.get('image')  # This will be the uploaded image

    if image:
        image.save(f"./uploads/{image.filename}")
    
    print(f"Title: {title}")
    print(f"Description: {description}")

    print(analyze_image('./uploads/clock.jpg'))

    print(analyze_description(description))

    print(search_web_image('./uploads/clock.jpg'))

    return {'status': 'success'}, 200

@app.route('/updateAppraisal', methods=['POST'])
def update_appraisal():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON received'}), 400

    try:
        with open('../app/past_appraisals.json', 'w') as f:
            json.dump(data, f, indent=2)
        return jsonify({'status': 'Appraisal data updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)