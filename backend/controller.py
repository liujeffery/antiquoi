from flask import Flask, request
from flask_cors import CORS
from image_agent import analyze_image
from text_agent import analyze_description

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

    return {'status': 'success'}, 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)