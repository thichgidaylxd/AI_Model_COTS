import pandas as pd
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from pathlib import Path


class DataProcessor:
    """Class xử lý dữ liệu cho model"""
    
    def __init__(self, dataset_path):
        self.dataset_path = Path(dataset_path)
        self.mlb = MultiLabelBinarizer()

    def prepare_data_text_format(self):
        """Chuẩn hóa dữ liệu thành dạng text để dùng cho mô hình NLP"""
        df = self.load_data()

        # Chuẩn hóa triệu chứng
        df["symptoms_list"] = df["trieu_chung"].apply(
            lambda x: [s.strip().lower() for s in x.split(";")]
        )

        # Ghép triệu chứng thành chuỗi
        df["text"] = df["symptoms_list"].apply(lambda lst: " ; ".join(lst))

        X_text = df["text"].tolist()
        y_labels = df["benh"].tolist()

        return X_text, y_labels


        
    def load_data(self):
        """Đọc dữ liệu từ CSV"""
        try:
            df = pd.read_csv(self.dataset_path)
            return df
        except FileNotFoundError:
            raise FileNotFoundError(f"Không tìm thấy file dataset: {self.dataset_path}")
    
    def prepare_data(self):
        """Chuẩn bị dữ liệu cho training"""
        df = self.load_data()
        
        # Tách triệu chứng thành list
        df['trieu_chung_list'] = df['trieu_chung'].apply(
            lambda x: [s.strip().lower() for s in x.split(';')]
        )
        
        # Tạo tập hợp tất cả triệu chứng
        all_symptoms = set()
        for symptoms in df['trieu_chung_list']:
            all_symptoms.update(symptoms)
        
        print(f"Tổng số triệu chứng: {len(all_symptoms)}")
        print(f"Tổng số bệnh: {len(df)}")
        
        # Mở rộng dữ liệu bằng cách tạo các tổ hợp triệu chứng
        expanded_data = []
        
        for _, row in df.iterrows():
            benh = row['benh']
            symptoms_list = row['trieu_chung_list']
            
            # Thêm bản ghi với tất cả triệu chứng
            expanded_data.append({
                'benh': benh,
                'trieu_chung_list': symptoms_list
            })
            
            # Tạo nhiều biến thể để đảm bảo đủ dữ liệu cho stratified split
            # Tạo tổ hợp 80% triệu chứng
            if len(symptoms_list) >= 4:
                n_symptoms_80 = max(3, int(len(symptoms_list) * 0.8))
                for _ in range(3):
                    subset = list(np.random.choice(symptoms_list, n_symptoms_80, replace=False))
                    expanded_data.append({
                        'benh': benh,
                        'trieu_chung_list': subset
                    })
            
            # Tạo tổ hợp 60% triệu chứng
            if len(symptoms_list) >= 5:
                n_symptoms_60 = max(3, int(len(symptoms_list) * 0.6))
                for _ in range(2):
                    subset = list(np.random.choice(symptoms_list, n_symptoms_60, replace=False))
                    expanded_data.append({
                        'benh': benh,
                        'trieu_chung_list': subset
                    })
        
        expanded_df = pd.DataFrame(expanded_data)
        
        # Chuyển đổi triệu chứng thành vector
        X = self.mlb.fit_transform(expanded_df['trieu_chung_list'])
        y = expanded_df['benh'].values
        
        return X, y, list(all_symptoms)
    
    def get_all_symptoms(self):
        """Lấy danh sách tất cả triệu chứng"""
        df = self.load_data()
        all_symptoms = set()
        
        for symptoms_str in df['trieu_chung']:
            symptoms = [s.strip().lower() for s in symptoms_str.split(';')]
            all_symptoms.update(symptoms)
        
        return sorted(list(all_symptoms))
    
    def transform_symptoms(self, symptoms_list):
        """Chuyển đổi danh sách triệu chứng thành vector"""
        # Chuẩn hóa triệu chứng
        symptoms_normalized = [s.strip().lower() for s in symptoms_list]
        return self.mlb.transform([symptoms_normalized])


class DiseaseInfo:
    """Class chứa thông tin về các bệnh"""
    
    DISEASE_DESCRIPTIONS = {
        'Cảm cúm': {
            'mo_ta': 'Bệnh nhiễm virus cúm, lây qua đường hô hấp',
            'khuyen_cao': 'Nghỉ ngơi, uống nhiều nước, đi khám nếu sốt cao kéo dài'
        },
        'Cảm lạnh': {
            'mo_ta': 'Nhiễm virus đường hô hấp trên, thường tự khỏi',
            'khuyen_cao': 'Nghỉ ngơi, uống nước ấm, giữ ấm cơ thể'
        },
        'Viêm họng': {
            'mo_ta': 'Viêm nhiễm vùng họng do vi khuẩn hoặc virus',
            'khuyen_cao': 'Súc miệng nước muối, uống nhiều nước, đi khám nếu không giảm'
        },
        'Viêm amidan': {
            'mo_ta': 'Viêm tuyến amidan, thường do vi khuẩn streptococcus',
            'khuyen_cao': 'Cần đi khám để được kê kháng sinh nếu do vi khuẩn'
        },
        'Viêm phổi': {
            'mo_ta': 'Nhiễm trùng phổi nghiêm trọng',
            'khuyen_cao': 'Cần đi khám ngay, có thể cần nhập viện điều trị'
        },
        'Viêm phế quản': {
            'mo_ta': 'Viêm đường dẫn khí phế quản',
            'khuyen_cao': 'Nghỉ ngơi, uống nhiều nước, tránh khói bụi'
        },
        'Sốt xuất huyết': {
            'mo_ta': 'Bệnh do virus dengue qua muỗi vằn',
            'khuyen_cao': 'Cần đi khám ngay, theo dõi số lượng tiểu cầu'
        },
        'Sốt rét': {
            'mo_ta': 'Bệnh nhiễm ký sinh trùng plasmodium qua muỗi anopheles',
            'khuyen_cao': 'Cần điều trị thuốc chống sốt rét ngay'
        },
        'Viêm gan A': {
            'mo_ta': 'Nhiễm virus viêm gan A, lây qua đường tiêu hóa',
            'khuyen_cao': 'Nghỉ ngơi, ăn nhẹ, tránh rượu bia, đi khám để theo dõi'
        },
        'Viêm gan B': {
            'mo_ta': 'Nhiễm virus viêm gan B, lây qua máu và dịch cơ thể',
            'khuyen_cao': 'Cần điều trị dài hạn, theo dõi chức năng gan định kỳ'
        },
        'Tiêu chảy': {
            'mo_ta': 'Rối loạn tiêu hóa với phân lỏng',
            'khuyen_cao': 'Bù nước điện giải, ăn nhẹ, đi khám nếu kéo dài hoặc có máu'
        },
        'Nhiễm khuẩn đường ruột': {
            'mo_ta': 'Nhiễm trùng đường tiêu hóa do vi khuẩn',
            'khuyen_cao': 'Bù nước, vệ sinh thực phẩm, đi khám để được kê kháng sinh'
        },
        'Viêm dạ dày': {
            'mo_ta': 'Viêm niêm mạc dạ dày',
            'khuyen_cao': 'Ăn uống điều độ, tránh cay nóng, căng thẳng'
        },
        'Loét dạ dày': {
            'mo_ta': 'Tổn thương niêm mạc dạ dày tạo vết loét',
            'khuyen_cao': 'Cần điều trị thuốc, thay đổi chế độ ăn uống'
        },
        'Viêm ruột thừa': {
            'mo_ta': 'Viêm ruột thừa, có thể vỡ gây nguy hiểm',
            'khuyen_cao': 'Cần đi cấp cứu ngay, có thể phải phẫu thuật'
        },
        'Sỏi mật': {
            'mo_ta': 'Sỏi trong túi mật hoặc đường mật',
            'khuyen_cao': 'Đi khám để đánh giá, có thể cần phẫu thuật'
        },
        'Viêm đường tiết niệu': {
            'mo_ta': 'Nhiễm trùng đường tiết niệu',
            'khuyen_cao': 'Uống nhiều nước, đi khám để được kê kháng sinh'
        },
        'Sỏi thận': {
            'mo_ta': 'Sỏi trong thận hoặc đường tiết niệu',
            'khuyen_cao': 'Uống nhiều nước, giảm đau, đi khám để xử lý sỏi'
        },
        'Tiểu đường': {
            'mo_ta': 'Rối loạn chuyển hóa đường trong máu',
            'khuyen_cao': 'Cần điều trị dài hạn, kiểm soát đường huyết'
        },
        'Huyết áp cao': {
            'mo_ta': 'Tăng huyết áp động mạch',
            'khuyen_cao': 'Theo dõi huyết áp, điều chỉnh lối sống, dùng thuốc theo chỉ định'
        },
        'Thiếu máu': {
            'mo_ta': 'Giảm hồng cầu hoặc hemoglobin trong máu',
            'khuyen_cao': 'Bổ sung sắt, vitamin, tìm nguyên nhân'
        },
        'Viêm khớp': {
            'mo_ta': 'Viêm các khớp trong cơ thể',
            'khuyen_cao': 'Giảm đau, vật lý trị liệu, tránh vận động quá sức'
        },
        'Gout': {
            'mo_ta': 'Viêm khớp do lắng đọng acid uric',
            'khuyen_cao': 'Hạn chế đạm động vật, rượu bia, dùng thuốc hạ acid uric'
        },
        'Viêm da': {
            'mo_ta': 'Viêm nhiễm da do nhiều nguyên nhân',
            'khuyen_cao': 'Giữ vệ sinh da, tránh gạch, đi khám da liễu'
        },
        'Dị ứng da': {
            'mo_ta': 'Phản ứng dị ứng trên da',
            'khuyen_cao': 'Tìm và tránh tác nhân dị ứng, dùng thuốc kháng histamine'
        },
        'Zona': {
            'mo_ta': 'Bệnh do virus herpes zoster tái hoạt',
            'khuyen_cao': 'Cần điều trị thuốc kháng virus sớm, giảm đau'
        },
        'Thủy đậu': {
            'mo_ta': 'Bệnh nhiễm virus varicella-zoster',
            'khuyen_cao': 'Cách ly, giảm ngứa, tránh gãi, uống nhiều nước'
        },
        'Quai bị': {
            'mo_ta': 'Bệnh nhiễm virus mumps',
            'khuyen_cao': 'Nghỉ ngơi, ăn mềm, chườm ấm vùng sưng'
        },
        'Sởi': {
            'mo_ta': 'Bệnh nhiễm virus sởi, lây lan nhanh',
            'khuyen_cao': 'Cách ly, nghỉ ngơi, theo dõi biến chứng'
        },
        'Rubella': {
            'mo_ta': 'Bệnh rubella (sởi Đức)',
            'khuyen_cao': 'Nghỉ ngơi, cách ly, đặc biệt nguy hiểm với phụ nữ mang thai'
        },
        'Tay chân miệng': {
            'mo_ta': 'Bệnh do virus Coxsackie, thường gặp ở trẻ em',
            'khuyen_cao': 'Giữ vệ sinh, ăn mềm mát, theo dõi sốt cao'
        },
        'Viêm màng não': {
            'mo_ta': 'Viêm màng bao não, rất nguy hiểm',
            'khuyen_cao': 'Cấp cứu ngay lập tức, cần điều trị tích cực'
        },
        'COVID-19': {
            'mo_ta': 'Bệnh nhiễm virus SARS-CoV-2',
            'khuyen_cao': 'Cách ly, theo dõi SpO2, đi khám nếu khó thở'
        },
        'Viêm xoang': {
            'mo_ta': 'Viêm niêm mạc xoang mũi',
            'khuyen_cao': 'Xông mũi, súc rửa mũi nước muối, thuốc kháng sinh nếu cần'
        },
        'Hen phế quản': {
            'mo_ta': 'Bệnh hen suyễn mạn tính',
            'khuyen_cao': 'Tránh tác nhân kích ứng, dùng thuốc theo chỉ định'
        },
        'Lao phổi': {
            'mo_ta': 'Nhiễm vi khuẩn lao Mycobacterium tuberculosis',
            'khuyen_cao': 'Cần điều trị kháng sinh đặc hiệu kéo dài 6-9 tháng'
        },
        'Viêm màng phổi': {
            'mo_ta': 'Viêm màng bao phổi',
            'khuyen_cao': 'Cần điều trị nguyên nhân, giảm đau, theo dõi'
        },
        'Rối loạn tiêu hóa': {
            'mo_ta': 'Các triệu chứng tiêu hóa không đặc hiệu',
            'khuyen_cao': 'Điều chỉnh chế độ ăn, giảm stress, đi khám nếu kéo dài'
        },
        'Trĩ': {
            'mo_ta': 'Giãn tĩnh mạch vùng hậu môn',
            'khuyen_cao': 'Ăn nhiều chất xơ, vệ sinh sạch sẽ, tránh ngồi lâu'
        },
        'Táo bón': {
            'mo_ta': 'Khó đại tiện, phân cứng',
            'khuyen_cao': 'Ăn nhiều rau xanh, uống nhiều nước, vận động'
        },
        'Rối loạn lo âu': {
            'mo_ta': 'Rối loạn tâm lý với lo âu quá mức',
            'khuyen_cao': 'Tham vấn tâm lý, thư giãn, có thể cần thuốc'
        }
    }
    
    @classmethod
    def get_info(cls, disease_name):
        """Lấy thông tin về bệnh"""
        return cls.DISEASE_DESCRIPTIONS.get(disease_name, {
            'mo_ta': 'Không có thông tin chi tiết',
            'khuyen_cao': 'Nên đi khám bác sĩ để được tư vấn'
        })