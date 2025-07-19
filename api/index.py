import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    # Try to import the simplified Vercel app first
    from app_vercel import app
    application = app
    
except ImportError as e:
    # If that fails, try the original app
    try:
        from app import app
        application = app
    except ImportError as e2:
        # If both fail, create a minimal Flask app
        from flask import Flask, jsonify
        
        app = Flask(__name__)
        
        @app.route('/')
        def index():
            return jsonify({
                'status': 'error',
                'message': f'Import failed: {str(e)} | {str(e2)}',
                'note': 'Car Store application could not be imported'
            })
        
        @app.route('/test')
        def test():
            return jsonify({
                'status': 'minimal',
                'message': 'Minimal Flask app is running',
                'import_error': str(e)
            })
        
        application = app

except Exception as e:
    # Catch any other errors
    from flask import Flask, jsonify
    
    app = Flask(__name__)
    
    @app.route('/')
    def error():
        return jsonify({
            'status': 'error',
            'message': f'Application error: {str(e)}',
            'type': type(e).__name__
        })
    
    application = app

# Export for Vercel
def handler(event, context):
    return application

if __name__ == "__main__":
    application.run(debug=True)