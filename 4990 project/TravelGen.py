from flask import Flask, request, jsonify, render_template
from openai import OpenAI

# Global configuration
API_KEY = "AIzaSyCcdFlnejJo3zVBaKTre4bdYfphKOe7_Aw"
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

# Initialize the OpenAI client
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def index():
    """
    Serve the frontend HTML page.
    """
    return render_template('TravelFront.html')

@app.route('/generate-itinerary', methods=['POST'])
def generate_itinerary():
    """
    API endpoint to generate a travel itinerary.
    """
    data = request.get_json()
    if not data or 'vacay_description' not in data:
        return jsonify({"error": "vacay_description is required"}), 400
    
    vacation_description = data['vacay_description']
    travel_prompt = "Generate a travel itinerary for my next vacation: " + vacation_description
    
    try:
        response = client.chat.completions.create(
            model="gemini-1.5-flash",
            n=1,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": travel_prompt}
            ]
        )
        
        itinerary = response.choices[0].message.content
        return jsonify({"travel_prompt": itinerary})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
