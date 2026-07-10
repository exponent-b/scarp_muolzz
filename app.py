### 메인
from flask import Flask, render_template, request, send_file, redirect
from scrapper import search_incruit, saramin_incruit ## scrapper.py에서 search_incruit 함수 받음
from file import save_to_csv

app = Flask(__name__)

db = {}
page = 5

@app.route('/')
def hello_world():
    return render_template("index.html") # html호출

@app.route("/search")
def search():
    keyword = request.args.get("key") # 입력값을 받음

    if keyword == "":
        return redirect("/")

    if keyword in db:
        jobs = db[keyword]

    else:
        jobs1 = search_incruit(keyword, page)
        jobs2 = saramin_incruit(keyword, page)
        jobs = jobs1 + jobs2
        db[keyword] = jobs


    return render_template("search.html", jobs = enumerate(jobs), keyword=keyword, count = len(jobs)) # search.html로 보냄


@app.route("/file")
def file():
    keyword = request.args.get("key")

    if keyword == "":
        return redirect("/")

    if keyword in db:
        jobs = db[keyword]
    else:
        jobs1 = search_incruit(keyword, page)
        jobs2 = saramin_incruit(keyword, page)
        jobs = jobs1 + jobs2
        db[keyword] = jobs

        
    save_to_csv(jobs)
    return send_file("./downloads.csv", as_attachment=True)
    

if __name__ == '__main__':
    app.run()