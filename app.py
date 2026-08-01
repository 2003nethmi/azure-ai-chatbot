from flask import Flask, render_template, request, jsonify
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
import os

app = Flask(__name__)

# Azure AI Foundry Endpoint එක (v1 කෑලි නැතුව Endpoint URL එක)
ENDPOINT = os.getenv(
    "AZURE_OPENAI_ENDPOINT", 
    "https://nirashasathmini-4408-resource.services.ai.azure.com/managed-deployments/gpt-4o-mini"
)
API_KEY = os.getenv("AZURE_OPENAI_KEY")

# Official Azure Inference Client එක initialize කිරීම
client = ChatCompletionsClient(
    endpoint=ENDPOINT,
    credential=AzureKeyCredential(API_KEY)
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
        response = client.complete(
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