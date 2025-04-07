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

    response1 = analyze_image('./uploads/clock.jpg')
    repsonse2 = analyze_description(description)
    response3 = search_web_image('./uploads/clock.jpg')

    cleaned_response1 = response1.strip('`').replace('```json', '').replace('```', '').strip().replace("json", "")
    cleaned_response2 = repsonse2.strip('`').replace('```json', '').replace('```', '').strip().replace("json", "")

    response_data1 = json.loads(cleaned_response1)
    response_data2 = json.loads(cleaned_response2)

    price1 = (response_data1['Max price'] + response_data1['Min price']) / 2
    price2 = (response_data2['Max price'] + response_data2['Min price']) / 2

    average_price = (price1 + price2) / 2 + response3
    to_return = ""

    if abs(average_price - price1) < abs(average_price - price2):
        print("Price 1 is closer to the average price.")
        to_return = cleaned_response1
    else:
        print("Price 2 is closer to the average price.")
        to_return = cleaned_response2

    parsed = json.loads(to_return)
    converted = {
        "items": [
            {
                "item": parsed["Item"],
                "description": parsed["Description"],
                "max_price": parsed["Max price"],
                "min_price": parsed["Min price"],
                "condition": parsed["Condition"].capitalize()
            }
        ]
    }

    try:
        with open('../app/past_appraisals.json', 'w') as f:
            json.dump(converted, f, indent=2)
    except Exception as e:
        print(f"Error writing to file: {e}")
        return jsonify({'error': 'Failed to write appraisal data'}), 500

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