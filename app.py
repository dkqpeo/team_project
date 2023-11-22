from flask import Flask, render_template
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# Matplotlib을 사용하여 그래프 생성
def generate_plot():
    plt.figure(figsize=(6, 4))
    plt.plot([1, 2, 3, 4], [10, 15, 25, 30])
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Example Plot')
    
    # 그래프 이미지를 BytesIO 객체에 저장
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    
    # base64로 인코딩하여 이미지 데이터 생성
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return plot_url

# Flask 라우트 설정
@app.route('/')
def index():
    plot = generate_plot()
    return render_template('index.html', plot=plot)

if __name__ == '__main__':
    app.run(debug=True)
