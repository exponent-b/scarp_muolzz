### 메인
from flask import Flask, render_template, request
from scrapper import search_incruit ## scrapper.py에서 search_incruit 함수 받음

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html") # html호출

@app.route("/search")
def search():
    keyword = request.args.get("key") # 입력값을 받음
    #print(keyword)
    jobs = search_incruit(keyword)
    # print(jobs)
    return render_template("search.html", jobs = enumerate(jobs)) # search.html로 보냄


if __name__ == '__main__':
    app.run(debug=True)