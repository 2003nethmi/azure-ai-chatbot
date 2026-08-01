from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# Azure AI Foundry Target Endpoint සහ Key (Managed Deployment එක සඳහා)
# Screenshot එකට අනුව Target Endpoint base URL එක:
AZURE_OPENAI_ENDPOINT = os.getenv(
    "AZURE_OPENAI_ENDPOINT", 
    "https://nirashasathmini-4408-resource.services.ai.azure.com/managed-deployments/gpt-4o-mini/v1"
)
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")

# OpenAI Base Client එක initialize කිරීම (Managed Endpoint v1 path එකට)
client = OpenAI(
    base_url=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_KEY
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "")
    
    if not user_message:
        return jsonify({"response": "කරුණාකර පණිවිඩයක් ඇතුළත් කරන්න."})

    try:
        # Request එක යැවීම (model parameter එක 'gpt-4o-mini' ලෙස pass කරන්න)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant hosted on Microsoft Azure."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=300
        )
        
        bot_response = response.choices[0].message.content
        return jsonify({"response": bot_response})

    except Exception as e:
        print("Error details:", str(e))
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)