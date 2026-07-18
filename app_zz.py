### 메인
from flask import Flask, render_template, request, send_file, redirect
from scrap_muol import search_musinsa, search_olive
from scrap_zz import search_zigzag
from file import save_to_csv
from concurrent.futures import ThreadPoolExecutor


app = Flask(__name__)


def get_products(keyword, sites):

    products = []


    with ThreadPoolExecutor(max_workers=3) as executor:

        futures = []


        if "무신사" in sites:
            futures.append(executor.submit(search_musinsa, keyword))

        if "올리브영" in sites:
            futures.append(executor.submit(search_olive, keyword, 7))

        if "지그재그" in sites:
            futures.append(executor.submit(search_zigzag, keyword))

        for future in futures:
            products += future.result()


    return products

db = {}

@app.route('/')
def hello_world():
    return render_template("index.html") # html호출

@app.route("/search")
def search():

    keyword = request.args.get("key")
    sites = request.args.getlist("site")

    if not keyword:
        return redirect("/")

    # 체크박스 아무것도 선택 안 했을 때 전체 검색
    if not sites:
        sites = ["무신사", "올리브영", "지그재그"]

    key = keyword + str(sites)

    if key in db:
        products = db[key]

    else:
        products = get_products(keyword, sites)
        db[key] = products

    # 가격 낮은 순 정렬
    products = sorted(products, key=lambda x: x["price"])

    return render_template(
        "search_zz.html",
        products=enumerate(products),
        keyword=keyword,
        count=len(products),
        sites=sites
    )



@app.route("/file")
def file():

    keyword = request.args.get("keyword")
    sites = request.args.getlist("site")

    key = keyword + str(sites)


    if key in db:
        products = db[key]

    else:
        products = get_products(keyword, sites)
        db[key] = products


    save_to_csv(products)

    return send_file(
        "downloads.csv",
        as_attachment=True,
        download_name="products.csv"
    )
    

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False # 안 씀
    )