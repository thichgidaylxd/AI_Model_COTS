"""
Script test API endpoints
Chạy sau khi đã start server: python test_api.py
"""

import requests
import json

BASE_URL = 'http://localhost:5000'


def test_health():
    """Test health check endpoint"""
    print("\n" + "="*60)
    print("TEST 1: Health Check")
    print("="*60)
    
    response = requests.get(f'{BASE_URL}/health')
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")


def test_get_symptoms():
    """Test lấy danh sách triệu chứng"""
    print("\n" + "="*60)
    print("TEST 2: Lấy danh sách triệu chứng")
    print("="*60)
    
    response = requests.get(f'{BASE_URL}/api/symptoms')
    print(f"Status: {response.status_code}")
    data = response.json()
    
    if data['success']:
        print(f"Số lượng triệu chứng: {data['so_luong']}")
        print(f"10 triệu chứng đầu tiên: {data['trieu_chung'][:10]}")
    else:
        print(f"Error: {data.get('error')}")


def test_get_diseases():
    """Test lấy danh sách bệnh"""
    print("\n" + "="*60)
    print("TEST 3: Lấy danh sách bệnh")
    print("="*60)
    
    response = requests.get(f'{BASE_URL}/api/diseases')
    print(f"Status: {response.status_code}")
    data = response.json()
    
    if data['success']:
        print(f"Số lượng bệnh: {data['so_luong']}")
        print(f"\n5 bệnh đầu tiên:")
        for disease in data['benh'][:5]:
            print(f"  - {disease['ten_benh']}: {disease['mo_ta']}")
    else:
        print(f"Error: {data.get('error')}")


def test_predict_flu():
    """Test dự đoán cảm cúm"""
    print("\n" + "="*60)
    print("TEST 4: Dự đoán bệnh - Triệu chứng cảm cúm")
    print("="*60)
    
    payload = {
        "trieu_chung": ["sốt", "ho", "đau đầu", "mệt mỏi"]
    }
    
    print(f"Input: {json.dumps(payload, ensure_ascii=False)}")
    
    response = requests.post(
        f'{BASE_URL}/api/predict',
        json=payload,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"\nStatus: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")


def test_predict_covid():
    """Test dự đoán COVID-19"""
    print("\n" + "="*60)
    print("TEST 5: Dự đoán bệnh - Triệu chứng COVID-19")
    print("="*60)
    
    payload = {
        "trieu_chung": ["sốt", "ho", "khó thở", "mất vị giác", "mất khứu giác"]
    }
    
    print(f"Input: {json.dumps(payload, ensure_ascii=False)}")
    
    response = requests.post(
        f'{BASE_URL}/api/predict',
        json=payload,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"\nStatus: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")


def test_predict_dengue():
    """Test dự đoán sốt xuất huyết"""
    print("\n" + "="*60)
    print("TEST 6: Dự đoán bệnh - Triệu chứng sốt xuất huyết")
    print("="*60)
    
    payload = {
        "trieu_chung": ["sốt cao", "đau đầu", "đau cơ", "nổi ban"]
    }
    
    print(f"Input: {json.dumps(payload, ensure_ascii=False)}")
    
    response = requests.post(
        f'{BASE_URL}/api/predict',
        json=payload,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"\nStatus: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")


def test_predict_gastritis():
    """Test dự đoán viêm dạ dày"""
    print("\n" + "="*60)
    print("TEST 7: Dự đoán bệnh - Triệu chứng viêm dạ dày")
    print("="*60)
    
    payload = {
        "trieu_chung": ["đau bụng", "buồn nôn", "đầy hơi", "ợ nóng"]
    }
    
    print(f"Input: {json.dumps(payload, ensure_ascii=False)}")
    
    response = requests.post(
        f'{BASE_URL}/api/predict',
        json=payload,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"\nStatus: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")


def test_model_info():
    """Test lấy thông tin model"""
    print("\n" + "="*60)
    print("TEST 8: Thông tin model")
    print("="*60)
    
    response = requests.get(f'{BASE_URL}/api/model-info')
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")


def main():
    """Chạy tất cả tests"""
    print("\n" + "="*60)
    print("DISEASE PREDICTION API - TEST SUITE")
    print("="*60)
    print(f"Testing server at: {BASE_URL}")
    
    try:
        # Test các endpoints
        test_health()
        test_get_symptoms()
        test_get_diseases()
        test_predict_flu()
        test_predict_covid()
        test_predict_dengue()
        test_predict_gastritis()
        test_model_info()
        
        print("\n" + "="*60)
        print("TẤT CẢ TESTS ĐÃ HOÀN TẤT!")
        print("="*60 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n" + "="*60)
        print("LỖI: Không thể kết nối đến server!")
        print("Hãy đảm bảo server đang chạy: python run.py")
        print("="*60 + "\n")


if __name__ == '__main__':
    main()