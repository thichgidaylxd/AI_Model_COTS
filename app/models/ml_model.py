import joblib
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, f1_score, accuracy_score
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression

from app.utils.data_processor import DataProcessor


class DiseasePredictor:
    """Model TF-IDF + Logistic Regression (One-vs-Rest)"""

    def __init__(self, config):
        self.config = config
        self.data_processor = DataProcessor(config.DATASET_PATH)
        self.vectorizer = None
        self.label_binarizer = None
        self.model = None

    def train(self):
        print("Đang load & xử lý dữ liệu...")
        X_text, y_labels = self.data_processor.prepare_data_text_format()

        # TF-IDF cho danh sách triệu chứng
        print("Đang vector hóa triệu chứng bằng TF-IDF...")
        self.vectorizer = TfidfVectorizer(
            analyzer="word",
            ngram_range=(1, 2),
            min_df=2
        )
        X = self.vectorizer.fit_transform(X_text)

        # MultiLabel binarizer
        print("Mã hóa nhãn bệnh...")
        self.label_binarizer = MultiLabelBinarizer()
        y = self.label_binarizer.fit_transform(y_labels)

        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=self.config.TEST_SIZE,
            random_state=self.config.RANDOM_STATE
        )

        # Logistic Regression phù hợp multi-label + sparse
        print("Đang train model Logistic Regression...")
        self.model = OneVsRestClassifier(
            LogisticRegression(max_iter=300)
        )
        self.model.fit(X_train, y_train)

        # Evaluate
        print("Đang đánh giá model...")
        y_pred = self.model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')

        print("\n===== EVALUATION =====")
        print("Accuracy:", round(acc, 4))
        print("F1-score:", round(f1, 4))
        print(classification_report(y_test, y_pred, zero_division=0))

        return {"accuracy": float(acc), "f1": float(f1)}

    def predict(self, symptoms_list):
        if self.model is None:
            raise ValueError("Model chưa load!")

        # Chuẩn hóa và chuyển thành dạng TF-IDF input
        text_input = " ".join([s.lower().strip() for s in symptoms_list])

        X = self.vectorizer.transform([text_input])
        probs = self.model.predict_proba(X)[0]

        classes = self.label_binarizer.classes_
        sorted_idx = np.argsort(probs)[::-1]

        results = []
        for i in sorted_idx[:self.config.MAX_PREDICTIONS]:
            if probs[i] >= self.config.MIN_CONFIDENCE:
                results.append({
                    "benh": classes[i],
                    "do_tin_cay": float(round(probs[i], 3))
                })

        return results

    def save_model(self):
        joblib.dump(self.model, self.config.MODEL_PATH)
        joblib.dump(self.vectorizer, self.config.VECTORIZER_PATH)
        joblib.dump(self.label_binarizer, self.config.LABEL_ENCODER_PATH)
        print("Đã lưu model!")

    def load_model(self):
        self.model = joblib.load(self.config.MODEL_PATH)
        self.vectorizer = joblib.load(self.config.VECTORIZER_PATH)
        self.label_binarizer = joblib.load(self.config.LABEL_ENCODER_PATH)
        print("Đã load model thành công!")
