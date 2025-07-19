import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    # Try to import the serverless-optimized app first
    from app_serverless import app
    application = app
    print("Successfully loaded serverless-optimized car store application")
    
except ImportError as e:
    print(f"Failed to import serverless app: {e}")
    try:
        # Fallback to original app
        from app import app
        application = app
        print("Loaded original car store application")
        
    except ImportError as e2:
        print(f"Failed to import original app: {e2}")
        # Create minimal fallback
        from flask import Flask, jsonify, render_template_string
        
        app = Flask(__name__)
        
        @app.route('/')
        def fallback():
            return jsonify({
                'status': 'fallback',
                'message': 'Car Store Application - Fallback Mode',
                'error': f'Import errors: {str(e)} | {str(e2)}',
                'note': 'Running in minimal mode due to import issues'
            })
        
        application = app

except Exception as e:
    print(f"Unexpected error: {e}")
    from flask import Flask, jsonify
    
    app = Flask(__name__)
    
    @app.route('/')
    def error():
        return jsonify({
            'status': 'error',
            'message': f'Application startup error: {str(e)}',
            'type': type(e).__name__
        })
    
    application = app

# Export for Vercel
if __name__ == "__main__":
    application.run(debug=True)