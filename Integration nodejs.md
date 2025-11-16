# Tích Hợp Disease Prediction Service vào Backend Node.js/Express

## 1. Cài Đặt Axios (nếu chưa có)

```bash
npm install axios
```

## 2. Tạo Service Helper

Tạo file `services/diseasePredictor.js`:

```javascript
const axios = require('axios');

const DISEASE_PREDICTION_API = process.env.DISEASE_PREDICTION_API || 'http://localhost:5000';

class DiseasePredictionService {
  /**
   * Dự đoán bệnh từ triệu chứng
   * @param {Array<string>} symptoms - Mảng triệu chứng
   * @returns {Promise<Object>} Kết quả dự đoán
   */
  async predictDisease(symptoms) {
    try {
      const response = await axios.post(
        `${DISEASE_PREDICTION_API}/api/predict`,
        { trieu_chung: symptoms },
        {
          headers: { 'Content-Type': 'application/json' },
          timeout: 10000 // 10 giây
        }
      );
      return response.data;
    } catch (error) {
      console.error('Error predicting disease:', error.message);
      throw new Error('Không thể dự đoán bệnh. Vui lòng thử lại sau.');
    }
  }

  /**
   * Lấy danh sách tất cả triệu chứng
   * @returns {Promise<Array<string>>} Danh sách triệu chứng
   */
  async getAllSymptoms() {
    try {
      const response = await axios.get(
        `${DISEASE_PREDICTION_API}/api/symptoms`,
        { timeout: 5000 }
      );
      return response.data.success ? response.data.trieu_chung : [];
    } catch (error) {
      console.error('Error getting symptoms:', error.message);
      return [];
    }
  }

  /**
   * Lấy danh sách tất cả bệnh
   * @returns {Promise<Array<Object>>} Danh sách bệnh
   */
  async getAllDiseases() {
    try {
      const response = await axios.get(
        `${DISEASE_PREDICTION_API}/api/diseases`,
        { timeout: 5000 }
      );
      return response.data.success ? response.data.benh : [];
    } catch (error) {
      console.error('Error getting diseases:', error.message);
      return [];
    }
  }

  /**
   * Kiểm tra health của service
   * @returns {Promise<boolean>} True nếu service đang hoạt động
   */
  async checkHealth() {
    try {
      const response = await axios.get(
        `${DISEASE_PREDICTION_API}/health`,
        { timeout: 3000 }
      );
      return response.data.status === 'healthy';
    } catch (error) {
      return false;
    }
  }
}

module.exports = new DiseasePredictionService();
```

## 3. Tạo Routes trong Express

Tạo file `routes/disease.js`:

```javascript
const express = require('express');
const router = express.Router();
const diseasePredictor = require('../services/diseasePredictor');

/**
 * POST /api/disease/predict
 * Dự đoán bệnh từ triệu chứng
 */
router.post('/predict', async (req, res) => {
  try {
    const { trieuChung } = req.body;

    // Validate input
    if (!trieuChung || !Array.isArray(trieuChung) || trieuChung.length === 0) {
      return res.status(400).json({
        success: false,
        message: 'Vui lòng cung cấp danh sách triệu chứng'
      });
    }

    // Gọi AI service
    const prediction = await diseasePredictor.predictDisease(trieuChung);

    return res.status(200).json(prediction);

  } catch (error) {
    console.error('Disease prediction error:', error);
    return res.status(500).json({
      success: false,
      message: 'Lỗi khi dự đoán bệnh',
      error: error.message
    });
  }
});

/**
 * GET /api/disease/symptoms
 * Lấy danh sách triệu chứng
 */
router.get('/symptoms', async (req, res) => {
  try {
    const symptoms = await diseasePredictor.getAllSymptoms();
    
    return res.status(200).json({
      success: true,
      data: symptoms
    });
  } catch (error) {
    console.error('Get symptoms error:', error);
    return res.status(500).json({
      success: false,
      message: 'Lỗi khi lấy danh sách triệu chứng'
    });
  }
});

/**
 * GET /api/disease/list
 * Lấy danh sách bệnh
 */
router.get('/list', async (req, res) => {
  try {
    const diseases = await diseasePredictor.getAllDiseases();
    
    return res.status(200).json({
      success: true,
      data: diseases
    });
  } catch (error) {
    console.error('Get diseases error:', error);
    return res.status(500).json({
      success: false,
      message: 'Lỗi khi lấy danh sách bệnh'
    });
  }
});

module.exports = router;
```

## 4. Đăng Ký Routes trong App

Trong file `app.js` hoặc `index.js`:

```javascript
const express = require('express');
const diseaseRoutes = require('./routes/disease');

const app = express();

// Middleware
app.use(express.json());

// Routes
app.use('/api/disease', diseaseRoutes);

// ...các routes khác

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

## 5. Tích Hợp với Database (Sequelize)

Ví dụ lưu kết quả dự đoán vào database:

```javascript
// models/PredictionHistory.js
module.exports = (sequelize, DataTypes) => {
  const PredictionHistory = sequelize.define('PredictionHistory', {
    id: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true
    },
    nguoi_dung_id: {
      type: DataTypes.INTEGER,
      allowNull: false
    },
    trieu_chung: {
      type: DataTypes.JSON, // Lưu array triệu chứng
      allowNull: false
    },
    benh_du_doan: {
      type: DataTypes.STRING,
      allowNull: false
    },
    do_tin_cay: {
      type: DataTypes.FLOAT,
      allowNull: false
    },
    ket_qua_day_du: {
      type: DataTypes.JSON, // Lưu toàn bộ response từ AI
      allowNull: true
    }
  }, {
    tableName: 'lich_su_du_doan',
    timestamps: true,
    createdAt: 'ngay_tao',
    updatedAt: 'ngay_cap_nhat'
  });

  return PredictionHistory;
};

// Sử dụng trong controller
router.post('/predict-and-save', async (req, res) => {
  try {
    const { userId, trieuChung } = req.body;

    // Dự đoán bệnh
    const prediction = await diseasePredictor.predictDisease(trieuChung);

    if (prediction.success) {
      // Lưu vào database
      await PredictionHistory.create({
        nguoi_dung_id: userId,
        trieu_chung: trieuChung,
        benh_du_doan: prediction.du_doan.benh,
        do_tin_cay: prediction.du_doan.do_tin_cay,
        ket_qua_day_du: prediction
      });
    }

    return res.status(200).json(prediction);

  } catch (error) {
    console.error('Error:', error);
    return res.status(500).json({
      success: false,
      message: 'Lỗi khi xử lý dự đoán'
    });
  }
});
```

## 6. Environment Variables

Thêm vào file `.env`:

```
DISEASE_PREDICTION_API=http://localhost:5000
```

## 7. Health Check Middleware

Kiểm tra AI service trước khi xử lý request:

```javascript
// middleware/checkAIService.js
const diseasePredictor = require('../services/diseasePredictor');

async function checkAIService(req, res, next) {
  const isHealthy = await diseasePredictor.checkHealth();
  
  if (!isHealthy) {
    return res.status(503).json({
      success: false,
      message: 'Dịch vụ dự đoán bệnh tạm thời không khả dụng'
    });
  }
  
  next();
}

module.exports = checkAIService;

// Sử dụng
router.post('/predict', checkAIService, async (req, res) => {
  // ... xử lý
});
```

## 8. Example Usage - Full Flow

```javascript
// Controller hoàn chỉnh
const diseaseController = {
  async predictDisease(req, res) {
    try {
      const { userId, symptoms } = req.body;

      // 1. Validate
      if (!symptoms || symptoms.length === 0) {
        return res.status(400).json({
          success: false,
          message: 'Vui lòng cung cấp triệu chứng'
        });
      }

      // 2. Gọi AI service
      const prediction = await diseasePredictor.predictDisease(symptoms);

      // 3. Lưu vào database (nếu cần)
      if (userId && prediction.success) {
        await PredictionHistory.create({
          nguoi_dung_id: userId,
          trieu_chung: symptoms,
          benh_du_doan: prediction.du_doan.benh,
          do_tin_cay: prediction.du_doan.do_tin_cay,
          ket_qua_day_du: prediction
        });
      }

      // 4. Trả về kết quả
      return res.status(200).json({
        success: true,
        data: prediction
      });

    } catch (error) {
      console.error('Disease prediction error:', error);
      return res.status(500).json({
        success: false,
        message: 'Lỗi server',
        error: error.message
      });
    }
  }
};

module.exports = diseaseController;
```

## Lưu Ý Quan Trọng

1. **Error Handling**: Luôn wrap các calls đến AI service trong try-catch
2. **Timeout**: Set timeout hợp lý cho các request (5-10s)
3. **Retry Logic**: Có thể implement retry logic nếu service tạm thời không khả dụng
4. **Caching**: Cache danh sách triệu chứng và bệnh để giảm calls
5. **Logging**: Log tất cả requests đến AI service để debug
6. **Rate Limiting**: Implement rate limiting nếu cần