from flask import Blueprint, request, jsonify, current_app
from app.models import DiseasePredictor
from app.config import Config
import time

training_bp = Blueprint('training', __name__)


@training_bp.route('/train', methods=['POST'])
def train_model():
    """
    API để train lại model (chỉ admin)
    
    Body:
    {
        "admin_key": "your-secret-key"
    }
    """
    try:
        # Validate admin key
        data = request.get_json()
        if not data or 'admin_key' not in data:
            return jsonify({
                'success': False,
                'error': 'Thiếu admin_key'
            }), 401
        
        # Lấy admin key từ config
        config = Config()
        if data['admin_key'] != config.ADMIN_KEY:
            return jsonify({
                'success': False,
                'error': 'Admin key không hợp lệ'
            }), 403
        
        # Train model
        print("Bắt đầu train model...")
        start_time = time.time()
        
        predictor = DiseasePredictor(config)
        metrics = predictor.train()
        predictor.save_model()
        
        training_time = time.time() - start_time
        
        # Reload predictor trong prediction route
        from app.routes.prediction import init_predictor
        init_predictor()
        
        return jsonify({
            'success': True,
            'message': 'Model đã được train thành công',
            'metrics': metrics,
            'training_time': round(training_time, 2)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Lỗi khi train model: {str(e)}'
        }), 500


@training_bp.route('/model-info', methods=['GET'])
def get_model_info():
    """
    API lấy thông tin về model hiện tại
    """
    try:
        config = Config()
        config.init_app(None)
        
        predictor = DiseasePredictor(config)
        
        try:
            predictor.load_model()
            model_info = predictor.get_model_info()
            
            return jsonify({
                'success': True,
                'model_info': model_info,
                'model_path': str(config.MODEL_PATH)
            }), 200
            
        except FileNotFoundError:
            return jsonify({
                'success': False,
                'message': 'Model chưa được train'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Lỗi server: {str(e)}'
        }), 500