"""
File chạy Flask API server
Chạy: python run.py
"""

import os
from app import create_app

# Lấy môi trường từ biến môi trường
config_name = os.getenv('FLASK_ENV', 'development')

# Tạo app
app = create_app(config_name)

if __name__ == '__main__':
    print("="*60)
    print("DISEASE PREDICTION API SERVER")
    print("="*60)
    print(f"Environment: {config_name}")
    print(f"Server: http://localhost:5000")
    print("="*60)
    print("\nAvailable endpoints:")
    print("  - GET  /              : API info")
    print("  - GET  /health        : Health check")
    print("  - POST /api/predict   : Dự đoán bệnh")
    print("  - GET  /api/symptoms  : Danh sách triệu chứng")
    print("  - GET  /api/diseases  : Danh sách bệnh")
    print("  - POST /api/train     : Train model (admin)")
    print("  - GET  /api/model-info: Thông tin model")
    print("="*60)
    print("\nĐang khởi động server...\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )