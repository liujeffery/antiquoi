from flask import Flask, request, jsonify
from flask_cors import CORS
import json, requests, os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

AGENT_WEBHOOKS = {
    "image": "http://localhost:5100/webhook",
    "text": "http://localhost:5200/webhook",
    "reverse": "http://localhost:5300/webhook"
}

@app.route('/submit', methods=['POST'])
def submit():
    title = request.form.get('title')
    description = request.form.get('description')
    image = request.files.get('image')
    image_path = None

    if image:
        image_path = os.path.join(UPLOAD_FOLDER, image.filename)
        image.save(image_path)

    print(f"Title: {title}")
    print(f"Description: {description}")

    # Prepare payloads
    try:
        # Send webhook POSTs
        res1 = requests.post(AGENT_WEBHOOKS["image"], json={"image_path": "./uploads/upload.jpg"})
        res2 = requests.post(AGENT_WEBHOOKS["text"], json={"description": description})
        res3 = requests.post(AGENT_WEBHOOKS["reverse"], json={"image_path": "./uploads/upload.jpg"})

        print("Response 1:", res1.text)
        print("Response 2:", res2.text)
        print("Response 3:", res3.text)

        # Parse responses
        response1 = res1.text.strip('`').replace('```json', '').replace('```', '').strip().replace("json", "")
        response2 = res2.text.strip('`').replace('```json', '').replace('```', '').strip().replace("json", "")

        data1 = json.loads(response1)
        data2 = json.loads(response2)
        data3 = json.loads(res3.text)

        price1 = (data1['Max price'] + data1['Min price']) / 2
        price2 = (data2['Max price'] + data2['Min price']) / 2

        average_price = (price1 + price2) / 2 + data3['average_price']
        to_return = data1 if abs(average_price - price1) < abs(average_price - price2) else data2

        converted = {
            "items": [
                {
                    "item": to_return["Item"],
                    "description": to_return["Description"],
                    "max_price": to_return["Max price"],
                    "min_price": to_return["Min price"],
                    "condition": to_return["Condition"].capitalize()
                }
            ]
        }

        with open('../app/past_appraisals.json', 'w') as f:
            json.dump(converted, f, indent=2)

        return {'status': 'success'}, 200

    except Exception as e:
        print(f"Webhook Error: {e}")
        return jsonify({'error': str(e)}), 500

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
