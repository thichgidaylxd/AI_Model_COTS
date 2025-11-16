"""
Script để train model Disease Prediction
Chạy: python train_model.py
"""

from app.config import Config
from app.models import DiseasePredictor

def main():
    print("="*60)
    print("DISEASE PREDICTION MODEL TRAINING")
    print("="*60)
    
    # Khởi tạo config
    config = Config()
    config.init_app(None)
    
    # Khởi tạo predictor
    predictor = DiseasePredictor(config)
    
    # Train model
    print("\nBắt đầu quá trình training...\n")
    metrics = predictor.train()
    
    # Lưu model
    print("\nĐang lưu model...")
    predictor.save_model()
    
    print("\n" + "="*60)
    print("TRAINING HOÀN TẤT!")
    print("="*60)
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"F1-Score: {metrics['f1']:.4f}")

    print(f"\nModel đã được lưu tại: {config.MODEL_PATH}")
    print("\nBạn có thể chạy API server bằng lệnh: python run.py")
    print("="*60)

if __name__ == '__main__':
    main()