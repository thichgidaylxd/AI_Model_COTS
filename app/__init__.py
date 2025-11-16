from flask import Flask, send_from_directory
from flask_cors import CORS
from app.config import config
import os

def create_app(config_name='default'):
    """Factory function để tạo Flask app"""
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Enable CORS cho TẤT CẢ routes và origins
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": False
        }
    })
    
    # Register blueprints
    from app.routes.prediction import prediction_bp, init_predictor
    from app.routes.training import training_bp
    
    app.register_blueprint(prediction_bp, url_prefix='/api')
    app.register_blueprint(training_bp, url_prefix='/api')
    
    # Initialize predictor after app is created
    with app.app_context():
        init_predictor()
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return {'status': 'healthy', 'service': 'Disease Prediction API'}, 200
    
    @app.route('/')
    def index():
        return {
            'message': 'Disease Prediction API',
            'version': '1.0.0',
            'endpoints': {
                'predict': '/api/predict',
                'train': '/api/train',
                'symptoms': '/api/symptoms',
                'test': '/test'
            }
        }, 200
    
    # Serve test page
    @app.route('/test')
    def test_page():
        """Serve test.html page"""
        return send_from_directory('.', 'test.html')
    
    return app