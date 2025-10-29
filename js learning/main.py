from flask import Flask, render_template, jsonify, send_from_directory
import os

app = Flask(__name__)

# 获取当前文件所在目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    html_path = os.path.join(BASE_DIR, "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()

# 添加静态文件路由
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(BASE_DIR, filename)

@app.route("/student")
def get_students():
    # 返回JSON格式的学生数据
    students_data = {
        "data": [
            {"id": "tyler", "name": "Tyler", "info": "Tyler是张翼"},
            {"id": "mathew", "name": "Mathew", "info": "Mathew是人机"},
            {"id": "raymond", "name": "Raymond", "info": "Raymond是人机"}
        ]
    }
    return jsonify(students_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002, debug=True)