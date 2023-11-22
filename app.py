from flask import Flask, render_template
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# CSV 파일 읽기
df = pd.read_csv('crime.csv')

# 나이를 10단위로 그룹화
df['age_group'] = pd.cut(df['age'], bins=range(0, 110, 10), right=False, labels=range(0, 100, 10))

# 필요한 열만 선택
selected_columns = ['age_group', 'race', 'is_violent_recid', 'is_recid']

# 그룹별 평균 계산
grouped_data = df[selected_columns].groupby(['age_group', 'race']).mean().reset_index()

# 시각화 함수
def plot_to_base64_image():
    plt.figure(figsize=(12, 8))

    # is_violent_recid 시각화
    plt.subplot(2, 1, 1)
    sns.barplot(x='age_group', y='is_violent_recid', hue='race', data=grouped_data)
    plt.title('Mean of is_violent_recid by Age Group and Race')

    # is_recid 시각화
    plt.subplot(2, 1, 2)
    sns.barplot(x='age_group', y='is_recid', hue='race', data=grouped_data)
    plt.title('Mean of is_recid by Age Group and Race')

    plt.tight_layout()

    # 그래프를 이미지로 변환하여 base64로 인코딩
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    return base64.b64encode(image_stream.read()).decode('utf-8')

# 라우팅 및 데이터 전송
@app.route('/')
def index():
    # HTML 템플릿 렌더링
    image_data = plot_to_base64_image()
    return render_template('index.html', image_data=image_data)

if __name__ == '__main__':
    app.run(debug=True)
