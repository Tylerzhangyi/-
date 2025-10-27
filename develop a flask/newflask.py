from flask import Flask, render_template
import os
import mimetypes
import base64
from http.server import BaseHTTPRequestHandler
import io
from flask import request

# 创建Flask应用
app = Flask(__name__)

# 不同人物的个人信息字典
profiles = {
    "kobe": {
        "name": "科比·布莱恩特",
        "age": "41岁（1978-2020）",
        "hobby": "篮球、写作、投资",
        "profession": "NBA传奇球星",
        "nickname": "黑曼巴",
        "position": "得分后卫",
        "photo_url": "/static/images/avator.jpg",
        "brief": "科比·布莱恩特，NBA历史上最伟大的球员之一，被誉为'黑曼巴'。职业生涯20年全部效力于洛杉矶湖人队，获得5次NBA总冠军、2次总决赛MVP、1次常规赛MVP。以其无与伦比的竞争精神、精湛的技术和坚韧的意志力著称。退役后投身商业和创作，著有《曼巴精神》等作品，并凭借动画短片《亲爱的篮球》获得奥斯卡奖。",
        "experiences": [
            {
                "title": "洛杉矶湖人队",
                "period": "1996年 - 2016年",
                "description": "NBA职业篮球运动员 - 得分后卫",
                "details": "5次NBA总冠军、2次总决赛MVP、1次常规赛MVP、18次全明星、4次全明星MVP"
            },
            {
                "title": "高中篮球",
                "period": "1992年 - 1996年",
                "description": "劳尔梅里恩高中 - 宾夕法尼亚州",
                "details": "高中四年总得分2883分，创下宾州东南区历史纪录"
            },
            {
                "title": "商业投资",
                "period": "2016年 - 2020年",
                "description": "Bryant Stibel投资公司创始人",
                "details": "投资多个科技公司，包括阿里巴巴、BodyArmor等"
            }
        ],
        "skills": [
            {"name": "得分能力", "score": 100, "level": "传奇级"},
            {"name": "关键球处理", "score": 100, "level": "传奇级"},
            {"name": "防守", "score": 85, "level": "顶级"},
            {"name": "领导力", "score": 100, "level": "传奇级"},
            {"name": "商业投资", "score": 75, "level": "优秀"},
            {"name": "创作写作", "score": 75, "level": "优秀"}
        ]
    },
    "jordan": {
        "name": "迈克尔·乔丹",
        "age": "61岁（1963-）",
        "hobby": "篮球、高尔夫、商业",
        "profession": "NBA传奇球星",
        "nickname": "飞人",
        "position": "得分后卫",
        "photo_url": "/static/images/avator.jpg",
        "brief": "迈克尔·乔丹，被誉为篮球史上最伟大的球员。职业生涯获得6次NBA总冠军、6次总决赛MVP、5次常规赛MVP。以其无与伦比的空中技巧、竞争精神和商业头脑著称。退役后成为夏洛特黄蜂队老板，并建立了强大的商业帝国。",
        "experiences": [
            {
                "title": "芝加哥公牛队",
                "period": "1984年 - 1993年, 1995年 - 1998年",
                "description": "NBA职业篮球运动员 - 得分后卫",
                "details": "6次NBA总冠军、6次总决赛MVP、5次常规赛MVP、14次全明星、3次全明星MVP"
            },
            {
                "title": "华盛顿奇才队",
                "period": "2001年 - 2003年",
                "description": "NBA职业篮球运动员 - 得分后卫",
                "details": "第二次复出，为奇才队效力两个赛季"
            },
            {
                "title": "夏洛特黄蜂队",
                "period": "2010年 - 至今",
                "description": "球队老板",
                "details": "收购黄蜂队，成为NBA历史上第一位黑人球队老板"
            }
        ],
        "skills": [
            {"name": "空中技巧", "score": 100, "level": "传奇级"},
            {"name": "关键球", "score": 100, "level": "传奇级"},
            {"name": "防守", "score": 95, "level": "传奇级"},
            {"name": "领导力", "score": 100, "level": "传奇级"},
            {"name": "商业头脑", "score": 90, "level": "顶级"},
            {"name": "品牌建设", "score": 100, "level": "传奇级"}
        ]
    },
    "curry": {
        "name": "斯蒂芬·库里",
        "age": "36岁（1988-）",
        "hobby": "篮球、高尔夫、家庭",
        "profession": "NBA现役球星",
        "nickname": "萌神",
        "position": "控球后卫",
        "photo_url": "/static/images/avator.jpg",
        "brief": "斯蒂芬·库里，现代篮球三分革命的引领者。以其精准的三分投射和出色的控球技术著称。职业生涯获得4次NBA总冠军、1次总决赛MVP、2次常规赛MVP。改变了现代篮球的打法，被誉为'三分王'。",
        "experiences": [
            {
                "title": "金州勇士队",
                "period": "2009年 - 至今",
                "description": "NBA职业篮球运动员 - 控球后卫",
                "details": "4次NBA总冠军、1次总决赛MVP、2次常规赛MVP、10次全明星、1次全明星MVP"
            },
            {
                "title": "戴维森学院",
                "period": "2006年 - 2009年",
                "description": "大学篮球运动员",
                "details": "带领戴维森学院闯入NCAA八强，创造历史"
            },
            {
                "title": "商业代言",
                "period": "2013年 - 至今",
                "description": "品牌代言人",
                "details": "与Under Armour合作，推出个人签名鞋系列"
            }
        ],
        "skills": [
            {"name": "三分投射", "score": 100, "level": "传奇级"},
            {"name": "控球技术", "score": 95, "level": "顶级"},
            {"name": "无球跑动", "score": 90, "level": "顶级"},
            {"name": "团队合作", "score": 95, "level": "顶级"},
            {"name": "商业价值", "score": 85, "level": "优秀"},
            {"name": "社交媒体", "score": 80, "level": "优秀"}
        ]
    },
    "lebron": {
        "name": "勒布朗·詹姆斯",
        "age": "39岁（1984-）",
        "hobby": "篮球、商业、慈善",
        "profession": "NBA现役球星",
        "nickname": "小皇帝",
        "position": "小前锋",
        "photo_url": "/static/images/avator.jpg",
        "brief": "勒布朗·詹姆斯，现役NBA最伟大的球员之一。以其全面的技术和出色的身体素质著称。职业生涯获得4次NBA总冠军、4次总决赛MVP、4次常规赛MVP。不仅在球场上表现出色，在场外也是成功的商人和慈善家。",
        "experiences": [
            {
                "title": "洛杉矶湖人队",
                "period": "2018年 - 至今",
                "description": "NBA职业篮球运动员 - 小前锋",
                "details": "1次NBA总冠军、1次总决赛MVP，帮助湖人队重返巅峰"
            },
            {
                "title": "克利夫兰骑士队",
                "period": "2003年 - 2010年, 2014年 - 2018年",
                "description": "NBA职业篮球运动员 - 小前锋",
                "details": "1次NBA总冠军、1次总决赛MVP，为家乡带来首个总冠军"
            },
            {
                "title": "迈阿密热火队",
                "period": "2010年 - 2014年",
                "description": "NBA职业篮球运动员 - 小前锋",
                "details": "2次NBA总冠军、2次总决赛MVP，与韦德、波什组成三巨头"
            }
        ],
        "skills": [
            {"name": "全面技术", "score": 100, "level": "传奇级"},
            {"name": "身体素质", "score": 95, "level": "顶级"},
            {"name": "篮球智商", "score": 100, "level": "传奇级"},
            {"name": "领导力", "score": 95, "level": "顶级"},
            {"name": "商业头脑", "score": 90, "level": "顶级"},
            {"name": "慈善事业", "score": 85, "level": "优秀"}
        ]
    }
}

@app.route("/")
def index():
    """首页 - 直接显示科比简历HTML"""
    with open("index1.html", "r", encoding="utf-8") as f:
        return f.read()

@app.route('/<filename>')
def serve_file(filename):
    """使用wfile底层方式提供文件，只使用Python标准库"""
    if os.path.exists(filename):
        # 使用open和read读取文件
        with open(filename, 'rb') as f:
            file_content = f.read()
        
        # 使用Python标准库的mimetypes模块获取Content-Type
        content_type, _ = mimetypes.guess_type(filename)
        if content_type is None:
            content_type = 'application/octet-stream'
        
        # 创建自定义响应类，使用wfile
        class FileResponse:
            def __init__(self, data, content_type):
                self.data = data
                self.content_type = content_type
                self.status_code = 200
                self.headers = {
                    'Content-Type': content_type,
                    'Content-Length': str(len(data)),
                    'Cache-Control': 'no-cache'
                }
            
            def __call__(self, environ, start_response):
                # 设置响应头
                headers = [(k, v) for k, v in self.headers.items()]
                start_response(f'{self.status_code} OK', headers)
                
                # 使用wfile方式返回数据
                return [self.data]
        
        return FileResponse(file_content, content_type)
    else:
        return "File not found", 404

@app.route("/kobe")
def kobe():
    """科比·布莱恩特简历"""
    return render_template('index.html', profile=profiles['kobe'])

@app.route("/jordan")
def jordan():
    """迈克尔·乔丹简历"""
    return render_template('index.html', profile=profiles['jordan'])

@app.route("/curry")
def curry():
    """斯蒂芬·库里简历"""
    return render_template('index.html', profile=profiles['curry'])

@app.route("/lebron")
def lebron():
    """勒布朗·詹姆斯简历"""
    return render_template('index.html', profile=profiles['lebron'])

@app.route("/hello")
def hello():
    """Hello页面"""
    return "Hello World!"

@app.route("/login", methods=["GET"])
def login_get():
    """登录页面 - GET请求"""
    return '<form method="post" action="/login"><input name="username" placeholder="用户名" /><input type="submit" value="登录"/></form>'

@app.route("/login", methods=["POST"])
def login_post():
    """登录处理 - POST请求"""
    return '登录成功！欢迎回来！'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002, debug=True)
