"""
Vercel serverless handler for Smart Parking System
Wraps the Flask app for Vercel deployment
"""

import sys
import os

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Vercel WSGI handler
def handler(event, context):
    """
    Vercel serverless function handler
    """
    try:
        # Import the WSGI handler
        from vercel_wsgi import handle_wsgi_event
        return handle_wsgi_event(app, event, context)
    except ImportError:
        # Fallback for local testing
        return {
            'statusCode': 500,
            'body': 'vercel-wsgi not installed. Install with: pip install vercel-wsgi'
        }

# For local testing
if __name__ == "__main__":
    app.run(debug=True, port=5000)
