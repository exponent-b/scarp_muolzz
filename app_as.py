### 메인
from flask import Flask, render_template, request
from scrapper_as import search_incruit, saramin_incruit ## scrapper.py에서 search_incruit 함수 받음

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html") # html호출

@app.route("/search")
def search():
    keyword = request.args.get("key") # 입력값을 받음

    #print(keyword)
    
    jobs1 = search_incruit(keyword)
    jobs2 = saramin_incruit(keyword)
    jobs = jobs1 + jobs2
    # jobs1.extend(jobs2) >>jobs1로 한다
    # print(jobs1)
    return render_template("search.html", jobs = enumerate(jobs), keyword=keyword, count = len(jobs)) # search.html로 보냄

if __name__ == '__main__':
    app.run(debug=True)