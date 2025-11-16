# Tích Hợp Disease Prediction Service vào React Frontend

## 1. Tạo Service Helper

Tạo file `src/services/diseaseService.js`:

```javascript
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3000/api';

class DiseaseService {
  /**
   * Dự đoán bệnh từ triệu chứng
   */
  async predictDisease(symptoms) {
    try {
      const response = await axios.post(`${API_BASE_URL}/disease/predict`, {
        trieuChung: symptoms
      });
      return response.data;
    } catch (error) {
      console.error('Error predicting disease:', error);
      throw error;
    }
  }

  /**
   * Lấy danh sách triệu chứng
   */
  async getSymptoms() {
    try {
      const response = await axios.get(`${API_BASE_URL}/disease/symptoms`);
      return response.data.data || [];
    } catch (error) {
      console.error('Error getting symptoms:', error);
      return [];
    }
  }

  /**
   * Lấy danh sách bệnh
   */
  async getDiseases() {
    try {
      const response = await axios.get(`${API_BASE_URL}/disease/list`);
      return response.data.data || [];
    } catch (error) {
      console.error('Error getting diseases:', error);
      return [];
    }
  }
}

export default new DiseaseService();
```

## 2. Component Chọn Triệu Chứng

Tạo file `src/components/SymptomSelector.jsx`:

```jsx
import React, { useState, useEffect } from 'react';
import diseaseService from '../services/diseaseService';

const SymptomSelector = ({ onSymptomsChange }) => {
  const [allSymptoms, setAllSymptoms] = useState([]);
  const [selectedSymptoms, setSelectedSymptoms] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadSymptoms();
  }, []);

  const loadSymptoms = async () => {
    try {
      const symptoms = await diseaseService.getSymptoms();
      setAllSymptoms(symptoms);
    } catch (error) {
      console.error('Error loading symptoms:', error);
    } finally {
      setLoading(false);
    }
  };

  const toggleSymptom = (symptom) => {
    let newSelected;
    if (selectedSymptoms.includes(symptom)) {
      newSelected = selectedSymptoms.filter(s => s !== symptom);
    } else {
      newSelected = [...selectedSymptoms, symptom];
    }
    setSelectedSymptoms(newSelected);
    onSymptomsChange(newSelected);
  };

  const filteredSymptoms = allSymptoms.filter(symptom =>
    symptom.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return <div className="text-center">Đang tải danh sách triệu chứng...</div>;
  }

  return (
    <div className="symptom-selector">
      <h3 className="text-lg font-semibold mb-3">Chọn triệu chứng</h3>
      
      {/* Search bar */}
      <input
        type="text"
        placeholder="Tìm kiếm triệu chứng..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        className="w-full px-4 py-2 border rounded-lg mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />

      {/* Selected symptoms */}
      {selectedSymptoms.length > 0 && (
        <div className="mb-4">
          <p className="text-sm text-gray-600 mb-2">
            Đã chọn ({selectedSymptoms.length}):
          </p>
          <div className="flex flex-wrap gap-2">
            {selectedSymptoms.map(symptom => (
              <span
                key={symptom}
                className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm flex items-center gap-2 cursor-pointer hover:bg-blue-200"
                onClick={() => toggleSymptom(symptom)}
              >
                {symptom}
                <span className="text-blue-600">×</span>
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Symptom list */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2 max-h-96 overflow-y-auto">
        {filteredSymptoms.map(symptom => (
          <button
            key={symptom}
            onClick={() => toggleSymptom(symptom)}
            className={`px-3 py-2 rounded-lg text-sm transition-colors ${
              selectedSymptoms.includes(symptom)
                ? 'bg-blue-500 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            {symptom}
          </button>
        ))}
      </div>
    </div>
  );
};

export default SymptomSelector;
```

## 3. Component Hiển Thị Kết Quả

Tạo file `src/components/PredictionResult.jsx`:

```jsx
import React from 'react';

const PredictionResult = ({ prediction }) => {
  if (!prediction) return null;

  const { du_doan, cac_benh_khac } = prediction;

  return (
    <div className="prediction-result bg-white rounded-lg shadow-lg p-6">
      {/* Dự đoán chính */}
      <div className="main-prediction mb-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-2xl font-bold text-gray-800">
            {du_doan.benh}
          </h3>
          <span className="text-3xl font-bold text-blue-600">
            {(du_doan.do_tin_cay * 100).toFixed(0)}%
          </span>
        </div>

        <div className="mb-4">
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all duration-500"
              style={{ width: `${du_doan.do_tin_cay * 100}%` }}
            />
          </div>
        </div>

        <div className="space-y-4">
          <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
            <h4 className="font-semibold text-gray-800 mb-2">Mô tả:</h4>
            <p className="text-gray-700">{du_doan.mo_ta}</p>
          </div>

          <div className="bg-yellow-50 border-l-4 border-yellow-500 p-4 rounded">
            <h4 className="font-semibold text-gray-800 mb-2">Khuyến cáo:</h4>
            <p className="text-gray-700">{du_doan.khuyen_cao}</p>
          </div>
        </div>
      </div>

      {/* Các dự đoán khác */}
      {cac_benh_khac && cac_benh_khac.length > 0 && (
        <div className="other-predictions">
          <h4 className="text-lg font-semibold text-gray-800 mb-3">
            Các khả năng khác:
          </h4>
          <div className="space-y-2">
            {cac_benh_khac.map((item, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <span className="text-gray-700">{item.benh}</span>
                <span className="text-gray-600 font-medium">
                  {(item.do_tin_cay * 100).toFixed(0)}%
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Disclaimer */}
      <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
        <p className="text-sm text-red-800">
          <strong>Lưu ý:</strong> Kết quả dự đoán này chỉ mang tính chất tham khảo.
          Vui lòng đến gặp bác sĩ để được chẩn đoán và điều trị chính xác.
        </p>
      </div>
    </div>
  );
};

export default PredictionResult;
```

## 4. Page Component Chính

Tạo file `src/pages/DiseasePrediction.jsx`:

```jsx
import React, { useState } from 'react';
import SymptomSelector from '../components/SymptomSelector';
import PredictionResult from '../components/PredictionResult';
import diseaseService from '../services/diseaseService';

const DiseasePrediction = () => {
  const [selectedSymptoms, setSelectedSymptoms] = useState([]);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handlePredict = async () => {
    if (selectedSymptoms.length === 0) {
      setError('Vui lòng chọn ít nhất một triệu chứng');
      return;
    }

    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      const result = await diseaseService.predictDisease(selectedSymptoms);
      
      if (result.success) {
        setPrediction(result);
      } else {
        setError(result.message || 'Không thể dự đoán bệnh');
      }
    } catch (err) {
      setError('Lỗi kết nối đến server. Vui lòng thử lại sau.');
      console.error('Prediction error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedSymptoms([]);
    setPrediction(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            Dự Đoán Bệnh AI
          </h1>
          <p className="text-gray-600">
            Chọn triệu chứng để nhận dự đoán bệnh từ AI
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          {/* Left column - Symptom selector */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <SymptomSelector onSymptomsChange={setSelectedSymptoms} />

            {/* Action buttons */}
            <div className="mt-6 flex gap-3">
              <button
                onClick={handlePredict}
                disabled={loading || selectedSymptoms.length === 0}
                className="flex-1 bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
              >
                {loading ? 'Đang dự đoán...' : 'Dự đoán bệnh'}
              </button>

              <button
                onClick={handleReset}
                className="px-6 py-3 bg-gray-200 text-gray-700 rounded-lg font-semibold hover:bg-gray-300 transition-colors"
              >
                Làm mới
              </button>
            </div>

            {/* Error message */}
            {error && (
              <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-red-800">{error}</p>
              </div>
            )}
          </div>

          {/* Right column - Results */}
          <div>
            {loading && (
              <div className="bg-white rounded-lg shadow-lg p-6 text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                <p className="text-gray-600">Đang phân tích triệu chứng...</p>
              </div>
            )}

            {!loading && prediction && (
              <PredictionResult prediction={prediction} />
            )}

            {!loading && !prediction && !error && (
              <div className="bg-white rounded-lg shadow-lg p-6 text-center text-gray-500">
                <p>Chọn triệu chứng và nhấn "Dự đoán bệnh" để xem kết quả</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default DiseasePrediction;
```

## 5. Cấu Hình Environment Variables

Tạo file `.env`:

```
REACT_APP_API_URL=http://localhost:3000/api
```

## 6. Sử Dụng trong App

Trong `App.js`:

```jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import DiseasePrediction from './pages/DiseasePrediction';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/disease-prediction" element={<DiseasePrediction />} />
        {/* ... các routes khác */}
      </Routes>
    </Router>
  );
}

export default App;
```

## 7. Custom Hook (Optional)

Tạo file `src/hooks/useDiseasePrediction.js`:

```jsx
import { useState } from 'react';
import diseaseService from '../services/diseaseService';

export const useDiseasePrediction = () => {
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const predict = async (symptoms) => {
    if (!symptoms || symptoms.length === 0) {
      setError('Vui lòng chọn triệu chứng');
      return;
    }

    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      const result = await diseaseService.predictDisease(symptoms);
      
      if (result.success) {
        setPrediction(result);
        return result;
      } else {
        throw new Error(result.message || 'Không thể dự đoán bệnh');
      }
    } catch (err) {
      const errorMessage = err.response?.data?.message || err.message || 'Lỗi không xác định';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setPrediction(null);
    setError(null);
    setLoading(false);
  };

  return {
    prediction,
    loading,
    error,
    predict,
    reset
  };
};
```

## 8. Tailwind CSS Configuration

Nếu dùng Tailwind CSS, đảm bảo đã cài đặt:

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

## 9. Example với Context API (Advanced)

Tạo `src/contexts/DiseaseContext.jsx`:

```jsx
import React, { createContext, useContext, useState } from 'react';
import diseaseService from '../services/diseaseService';

const DiseaseContext = createContext();

export const DiseaseProvider = ({ children }) => {
  const [symptoms, setSymptoms] = useState([]);
  const [predictions, setPredictions] = useState([]);

  const addPrediction = async (selectedSymptoms) => {
    const result = await diseaseService.predictDisease(selectedSymptoms);
    if (result.success) {
      setPredictions(prev => [{
        id: Date.now(),
        symptoms: selectedSymptoms,
        result: result,
        timestamp: new Date()
      }, ...prev]);
    }
    return result;
  };

  return (
    <DiseaseContext.Provider value={{
      symptoms,
      setSymptoms,
      predictions,
      addPrediction
    }}>
      {children}
    </DiseaseContext.Provider>
  );
};

export const useDisease = () => useContext(DiseaseContext);
```

## Lưu Ý

1. **CORS**: Đảm bảo backend đã enable CORS cho frontend domain
2. **Error Handling**: Luôn handle errors từ API calls
3. **Loading States**: Hiển thị loading state khi gọi API
4. **Validation**: Validate input trước khi gửi request
5. **Responsive**: Đảm bảo UI responsive trên mọi thiết bị