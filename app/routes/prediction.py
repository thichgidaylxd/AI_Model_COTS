from flask import Blueprint, request, jsonify, current_app
from app.models import DiseasePredictor
from app.utils import DiseaseInfo
from app.config import Config

prediction_bp = Blueprint('prediction', __name__)

# Khởi tạo predictor (sẽ được load khi app start)
predictor = None


def init_predictor():
    """Khởi tạo predictor khi app start"""
    global predictor
    if predictor is None:
        # Tạo config object
        config = Config()
        config.init_app(None)
        
        predictor = DiseasePredictor(config)
        try:
            predictor.load_model()
        except FileNotFoundError:
            print("WARNING: Model chưa được train. Hãy chạy train_model.py trước.")


@prediction_bp.route('/predict', methods=['POST'])
def predict():
    """
    API dự đoán bệnh
    
    Body:
    {
        "trieu_chung": ["sốt", "ho", "đau đầu"]
    }
    """
    try:
        # Khởi tạo predictor nếu chưa có
        init_predictor()
        
        if predictor is None or predictor.model is None:
            return jsonify({
                'success': False,
                'error': 'Model chưa được train. Vui lòng liên hệ admin.'
            }), 503
        
        # Validate request
        data = request.get_json()
        if not data or 'trieu_chung' not in data:
            return jsonify({
                'success': False,
                'error': 'Thiếu trường "trieu_chung" trong request'
            }), 400
        
        symptoms = data['trieu_chung']
        
        if not isinstance(symptoms, list) or len(symptoms) == 0:
            return jsonify({
                'success': False,
                'error': 'Trường "trieu_chung" phải là mảng và không được rỗng'
            }), 400
        
        # Dự đoán
        predictions = predictor.predict(symptoms)
        
        if not predictions:
            return jsonify({
                'success': False,
                'message': 'Không thể dự đoán bệnh với các triệu chứng này',
                'khuyen_cao': 'Vui lòng bổ sung thêm triệu chứng hoặc đi khám bác sĩ'
            }), 200
        
        # Lấy thông tin chi tiết cho dự đoán chính
        main_prediction = predictions[0]
        disease_name = main_prediction['benh']
        disease_details = DiseaseInfo.get_info(disease_name)
        
        response = {
            'success': True,
            'du_doan': {
                'benh': disease_name,
                'do_tin_cay': main_prediction['do_tin_cay'],
                'mo_ta': disease_details['mo_ta'],
                'khuyen_cao': disease_details['khuyen_cao']
            }
        }
        
        # Thêm các dự đoán phụ nếu có
        if len(predictions) > 1:
            response['cac_benh_khac'] = predictions[1:]
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Lỗi server: {str(e)}'
        }), 500


@prediction_bp.route('/symptoms', methods=['GET'])
def get_symptoms():
    """
    API lấy danh sách tất cả triệu chứng có sẵn
    """
    try:
        # Khởi tạo predictor nếu chưa có
        init_predictor()
        
        if predictor is None:
            return jsonify({
                'success': False,
                'error': 'Chưa thể lấy danh sách triệu chứng'
            }), 503
        
        symptoms = predictor.data_processor.get_all_symptoms()
        
        return jsonify({
            'success': True,
            'trieu_chung': symptoms,
            'so_luong': len(symptoms)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Lỗi server: {str(e)}'
        }), 500


@prediction_bp.route('/diseases', methods=['GET'])
def get_diseases():
    """
    API lấy danh sách tất cả bệnh có trong hệ thống
    """
    try:
        init_predictor()
        
        if predictor is None or predictor.model is None:
            return jsonify({
                'success': False,
                'error': 'Model chưa sẵn sàng'
            }), 503
        
        diseases = predictor.model.classes_.tolist()
        
        # Thêm thông tin chi tiết cho mỗi bệnh
        diseases_info = []
        for disease in diseases:
            info = DiseaseInfo.get_info(disease)
            diseases_info.append({
                'ten_benh': disease,
                'mo_ta': info['mo_ta']
            })
        
        return jsonify({
            'success': True,
            'benh': diseases_info,
            'so_luong': len(diseases)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Lỗi server: {str(e)}'
        }), 500