from flask import Flask, render_template, request, jsonify
from openai import AzureOpenAI
import os

app = Flask(__name__)

# Azure OpenAI Base Endpoint (අගට /openai/v1... කෑලි නැතුව)
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://nirashasathmini-4408-resource.services.ai.azure.com/openai/v1/chat/completions")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME", "gpt-4o-mini")

# Azure OpenAI Client initialize කිරීම
client = AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_KEY,
    api_version="2024-02-15-preview"
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
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
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
        # Exact Exception message එක UI එකට Return කිරීම
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)