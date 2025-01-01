from flask import Flask, request, jsonify, render_template
import requests
from flask_cors import CORS
import logging
import json

# Initialize Flask app and configure logging
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"]}})
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/query', methods=['POST'])
def query_llama():
    try:
        # Get and validate the request data
        data = request.get_json()
        if not data or 'question' not in data:
            logger.error("Invalid request data received")
            return jsonify({'error': 'Invalid request. Please provide a question.'}), 400

        question = data['question']
        logger.info(f"Received question: {question}")

        # Prepare the request to Ollama
        ollama_url = 'http://localhost:11434/api/generate'
        ollama_payload = {
            "model": "llama2",  # Make sure this matches your installed model
            "prompt": question,
            "stream": False
        }

        # Make the request to Ollama
        logger.info("Sending request to Ollama")
        response = requests.post(
            ollama_url,
            json=ollama_payload,
            timeout=30  # Add timeout to prevent hanging
        )

        # Check for successful response
        if response.status_code == 200:
            try:
                result = response.json()
                # Extract the response text from Ollama's response
                response_text = result.get('response', '')
                logger.info("Successfully received response from Ollama")
                return jsonify({
                    'response': response_text,
                    'status': 'success'
                })
            except json.JSONDecodeError as e:
                logger.error(f"Failed to decode Ollama response: {e}")
                return jsonify({'error': 'Failed to decode AI response'}), 500
        else:
            logger.error(f"Ollama returned status code: {response.status_code}")
            return jsonify({'error': f'AI service returned status code: {response.status_code}'}), 500

    except requests.exceptions.ConnectionError:
        logger.error("Failed to connect to Ollama service")
        return jsonify({'error': 'Failed to connect to AI service. Is Ollama running?'}), 503
    except requests.exceptions.Timeout:
        logger.error("Request to Ollama timed out")
        return jsonify({'error': 'Request to AI service timed out'}), 504
    except requests.exceptions.RequestException as e:
        logger.error(f"Request to Ollama failed: {str(e)}")
        return jsonify({'error': f'Request to AI service failed: {str(e)}'}), 500
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500


@app.route('/algorithm', methods=['POST'])
def explain_algorithm():
    try:
        data = request.get_json()
        if not data or 'algorithm' not in data:
            return jsonify({'error': 'Please provide an algorithm name'}), 400

        algorithm_name = data['algorithm']
        prompt = f"Explain the {algorithm_name} algorithm with code examples in Python."

        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                "model": "llama2",
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            return jsonify({
                'response': result.get('response', ''),
                'status': 'success'
            })
        else:
            return jsonify({'error': 'Failed to get response from AI service'}), 500

    except Exception as e:
        logger.error(f"Error in algorithm explanation: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/debug', methods=['POST'])
def debug_code():
    try:
        data = request.get_json()
        if not data or 'code' not in data:
            return jsonify({'error': 'Please provide code to debug'}), 400

        code = data['code']
        prompt = f"Debug this code and explain any issues:\n{code}"

        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                "model": "llama2",
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            return jsonify({
                'response': result.get('response', ''),
                'status': 'success'
            })
        else:
            return jsonify({'error': 'Failed to get response from AI service'}), 500

    except Exception as e:
        logger.error(f"Error in code debugging: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/optimize', methods=['POST'])
def optimize_code():
    try:
        data = request.get_json()
        if not data or 'code' not in data:
            return jsonify({'error': 'Please provide code to optimize'}), 400

        code = data['code']
        prompt = f"Optimize this code and explain the improvements:\n{code}"

        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                "model": "llama2",
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            return jsonify({
                'response': result.get('response', ''),
                'status': 'success'
            })
        else:
            return jsonify({'error': 'Failed to get response from AI service'}), 500

    except Exception as e:
        logger.error(f"Error in code optimization: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/practice', methods=['GET', 'POST'])
def practice_problems():
    try:
        prompt = "Suggest 5 programming practice problems with hints and difficulty levels."

        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                "model": "llama2",
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            return jsonify({
                'response': result.get('response', ''),
                'status': 'success'
            })
        else:
            return jsonify({'error': 'Failed to get response from AI service'}), 500

    except Exception as e:
        logger.error(f"Error getting practice problems: {str(e)}")
        return jsonify({'error': str(e)}), 500


# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Resource not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Add configuration for better debugging
    app.config['JSON_SORT_KEYS'] = False
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

    # Print the available routes
    print("Available routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule.methods} {rule}")

    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)