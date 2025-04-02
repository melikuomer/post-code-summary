from flask import Flask, request

app = Flask(__name__)
import os
from pre_commit_hooks.ui import generate_html
from pre_commit_hooks.client import App
client = App(api_key=os.getenv('GOOGLE_API_KEY') or "")


@app.route('/generateReport', methods=['POST'])
def generate_report():
    print("selam",str(request.get_json()))
    artifact = client.run(str(request.get_json()))
    print(artifact.model_dump_json())
    return generate_html(artifact)

if __name__ == '__main__':
    app.run(port=3000)
