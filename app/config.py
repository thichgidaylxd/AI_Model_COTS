import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    """Cấu hình cơ bản cho ứng dụng"""
    
    # Flask config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Model config
    MODEL_DIR = BASE_DIR / 'models' / 'saved'
    MODEL_PATH = MODEL_DIR / 'disease_model.pkl'
    VECTORIZER_PATH = MODEL_DIR / 'vectorizer.pkl'
    LABEL_ENCODER_PATH = MODEL_DIR / 'label_encoder.pkl'
    
    # Data config
    DATA_DIR = BASE_DIR / 'data'
    RAW_DATA_DIR = DATA_DIR / 'raw'
    PROCESSED_DATA_DIR = DATA_DIR / 'processed'
    DATASET_PATH = RAW_DATA_DIR / 'disease_symptoms.csv'
    
    # Training config
    TEST_SIZE = 0.2
    RANDOM_STATE = 42
    N_ESTIMATORS = 100
    
    # API config
    ADMIN_KEY = os.environ.get('ADMIN_KEY') or 'admin-secret-key-2024'
    MAX_PREDICTIONS = 3  # Số lượng dự đoán trả về
    MIN_CONFIDENCE = 0.3  # Độ tin cậy tối thiểu
    
    # CORS config
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    @staticmethod
    def init_app(app):
        """Khởi tạo thư mục cần thiết"""
        Config.MODEL_DIR.mkdir(parents=True, exist_ok=True)
        Config.DATA_DIR.mkdir(parents=True, exist_ok=True)
        Config.RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
        Config.PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)


class DevelopmentConfig(Config):
    """Cấu hình cho môi trường development"""
    DEBUG = True


class ProductionConfig(Config):
    """Cấu hình cho môi trường production"""
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}