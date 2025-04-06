from flask import Flask, request
from flask_cors import CORS
from image_agent import analyze_image
from text_agent import analyze_description
from marketplace import generate_marketplace_text
import abc from ABC

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from your mobile app

# OLD CODE
# @app.route('/submit', methods=['POST'])
# def submit():
#     title = request.form.get('title')
#     description = request.form.get('description')
#     image = request.files.get('image')  # This will be the uploaded image
#
#     if image:
#         image.save(f"./uploads/{image.filename}")
#
#     print(f"Title: {title}")
#     print(f"Description: {description}")
#
#     print(analyze_image('./uploads/clock.jpg'))
#
#     print(analyze_description(description))
#
#     return {'status': 'success'}, 200


@app.route('/submit', methods=['POST'])
def submit():
    title = request.form.get('title')
    description = request.form.get('description')
    image = request.files.get('image')  # This will be the uploaded image

    if image:
        image.save(f"./uploads/{image.filename}")

    blackboard = Blackboard(user_image_directory=f"./uploads/{image.filename}",
        user_description=description,
        knowledge_sources=[]) # NEED TO ADD KNOWLEDGE SOURCE CLASSES


    return {'status': 'success'}, 200

class Blackboard:
    def __init__(self, user_image_directory, user_description, knowledge_sources):
        self.user_description = user_description
        self.user_image = user_image
        self.agent_data = {index: element for index, element in enumerate(knowledge_sources)}
        self.final_result = null

    def read_user_description(self):
        return self.user_description

    def read_user_image(self):
        return self.user_image

    def read_expert_data(self, key):
        try:
            return self.agent_data(key)
        except KeyError:
            print("Tried to access data from a nonexistent expert.")
        except:
            print("Something went wrong while trying to read blackboard agent data.")

    def update_agent_data(self, key, data):
        try:
            self.agent_data(key) = data
            return self.agent_data(key)
        except KeyError:
            print("Tried to access data from a nonexistent expert.")
        except:
            print("Something went wrong while trying to read blackboard agent data.")

        return self.agent_data

class KnowledgeSource(abc):
    @abstractmethod
    def get_expert_opinion(self):
        ...

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)