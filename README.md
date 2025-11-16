# Hệ Thống Dự Đoán Bệnh - Disease Prediction Service

## Tổng Quan
Service AI dự đoán bệnh dựa trên triệu chứng, sử dụng Machine Learning (Random Forest).

## Cấu Trúc Project
```
disease-prediction-service/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── ml_model.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── prediction.py
│   │   └── training.py
│   └── utils/
│       ├── __init__.py
│       └── data_processor.py
├── data/
│   ├── raw/
│   │   └── disease_symptoms.csv
│   └── processed/
├── models/
│   └── saved/
├── requirements.txt
├── train_model.py
├── run.py
└── README.md
```

## Cài Đặt

### 1. Tạo môi trường ảo
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate  # Windows
```

### 2. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### 3. Train model
```bash
python train_model.py
```

### 4. Chạy API
```bash
python run.py
```

## API Endpoints

### 1. POST /api/predict
Dự đoán bệnh dựa trên triệu chứng

**Request:**
```json
{
  "trieu_chung": ["sốt", "ho", "đau đầu"]
}
```

**Response:**
```json
{
  "success": true,
  "du_doan": {
    "benh": "Cảm cúm",
    "do_tin_cay": 0.92,
    "mo_ta": "Bệnh nhiễm trùng đường hô hấp",
    "khuyen_cao": "Nên đi khám bác sĩ nếu triệu chứng kéo dài"
  },
  "cac_benh_khac": [
    {"benh": "Viêm họng", "do_tin_cay": 0.65},
    {"benh": "Cảm lạnh", "do_tin_cay": 0.58}
  ]
}
```

### 2. POST /api/train
Train lại model (chỉ admin)

**Request:**
```json
{
  "admin_key": "your-secret-key"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Model đã được train thành công",
  "metrics": {
    "accuracy": 0.94,
    "f1_score": 0.93
  }
}
```

### 3. GET /api/symptoms
Lấy danh sách triệu chứng có sẵn

**Response:**
```json
{
  "success": true,
  "trieu_chung": ["sốt", "ho", "đau đầu", "buồn nôn", ...]
}
```

## Tích Hợp Vào TL-Medic

### Backend (Node.js/Express)
```javascript
const axios = require('axios');

async function predictDisease(symptoms) {
  const response = await axios.post('http://localhost:5000/api/predict', {
    trieu_chung: symptoms
  });
  return response.data;
}
```

### Frontend (React)
```javascript
const predictDisease = async (symptoms) => {
  const response = await fetch('http://localhost:5000/api/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ trieu_chung: symptoms })
  });
  return await response.json();
};
```

## Ghi Chú
- Model sử dụng Random Forest Classifier
- Dataset mẫu bao gồm 41 bệnh phổ biến
- Có thể thêm dữ liệu để cải thiện độ chính xác
- Kết quả chỉ mang tính tham khảo, không thay thế chẩn đoán y tế