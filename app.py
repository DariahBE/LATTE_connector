from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/detect_language', methods=['POST'])
def detect_language():
    # Extract parameters from the request
    params = request.json
    command = ['python', 'detect_language.py']
    command += [f'--{key}={value}' for key, value in params.items()]
    
    # Run the language detector script
    result = subprocess.run(command, capture_output=True, text=True)
    return jsonify({'output': result.stdout, 'error': result.stderr})

@app.route('/extract_entities', methods=['POST'])
def extract_entities():
    # Extract parameters from the request
    params = request.json
    command = ['python', 'entity_extractor.py']
    command += [f'--{key}={value}' for key, value in params.items()]    
    # Run the entity extractor script
    result = subprocess.run(command, capture_output=True, text=True)
    return jsonify({'output': result.stdout, 'error': result.stderr})

@app.route('/')
def home():
    return "Hello world. Latteconnector is up and running"

if __name__ == '__main__':
    app.run(debug=True)
