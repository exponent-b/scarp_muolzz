'''
무신사 올리브영

'''
import time
import requests
from playwright.sync_api import sync_playwright
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import urllib.parse

def search_musinsa(keyword):
    start_count = time.time()

    products = []
    goods_set = set()

    url = f"https://www.musinsa.com/category/104/goods?keyword={keyword}&keywordType=keyword&gf=A"

    with sync_playwright() as p:

        # browser = p.chromium.launch(headless=True) # render error
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox", 
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--no-zygote"
            ])
        page = browser.new_page()

        api_data = []

        def get_api(response):
            if "api.musinsa.com/api2/dp/v2/plp/goods" in response.url:
                # print("API 발견")

                try:
                    api_data.append(response.json())
                except:
                    pass

        page.on("response", get_api)

        page.goto(url)

        page.wait_for_timeout(800)

        for i in range(5):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(500)
            
        
        # count = 0
        for data in api_data:
            

            for item in data["data"]["list"]:
                # print(item.keys())
                goods_no = item["goodsNo"]

                if goods_no not in goods_set:
                    goods_set.add(goods_no)

                    products.append({
                        "site": "무신사",
                        "brand": item["brandName"],
                        "name": item["goodsName"],
                        "price": int(item["price"]),
                        "image": item["thumbnail"],
                        "link": "https://www.musinsa.com/products/" + str(goods_no)
                    })
                    # print(products)
                    # count += 1
                    
                if len(products) >= 150:
                    break
                
            if len(products) >= 150:
                break
                    
        
        browser.close()
    print(
        f"무신사 소요시간: {time.time()-start_count:.2f}초"
    )

    return products





def search_olive(keyword, page):
    start_time = time.time()   # 시작 시간 측정

    keyword = urllib.parse.quote(keyword)
    products = []
    

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled"
            ]
        )
        
        browser_page = browser.new_page(
            viewport={"width": 1280, "height": 1000},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
        )

        browser_page.route(
            "**/*",
            lambda route:
                route.abort()
                if route.request.resource_type in [
                    "media",
                    "font"
                ]
                else route.continue_()
        )

        for i in range(page):
            page_start = time.time()

            start_count = i * 24

            url = (
                f"https://www.oliveyoung.co.kr/store/search/getSearchMain.do"
                f"?query={keyword}"
                f"&startCount={start_count}"
            )

            # 1. goto 시간 측정
            t = time.time()
            browser_page.goto(url)

            print(f"[{i+1}페이지] goto: {time.time()-t:.3f}초")

            # 2. 대기 시간 측정 36s -> 24s ->
            t = time.time()
            # browser_page.wait_for_timeout(1000) // 1. 36s
            browser_page.wait_for_selector(
                ".prd_info",
                state="attached",
                timeout=5000
            )
        
            print(f"[{i+1}페이지] wait: {time.time()-t:.3f}초")
        
            # 3. HTML 가져오기 시간
            t = time.time()
            html = browser_page.content()

            print(f"[{i+1}페이지] content: {time.time()-t:.3f}초")

            # 4. BeautifulSoup 파싱 시간
            t = time.time()
            soup = BeautifulSoup(html, "html.parser")
            lis = soup.select(".prd_info")

            print(f"[{i+1}페이지] soup: {time.time()-t:.3f}초")

            # 5. 상품 추출 시간
            t = time.time()

            count = 0
            for li in lis:

                brand = li.select_one(".tx_brand")
                name = li.select_one(".tx_name")
                product_link = li.select_one(".prd_thumb")
                image = li.select_one(".prd_thumb img")
                price = li.select_one(".tx_cur")
            
                if brand and name and product_link and image:

                    products.append({
                        "site": "올리브영",
                        "brand": brand.text.strip(),
                        "name": name.text.strip(),
                        "price": int(
                            price.text
                            .replace(",", "")
                            .replace("원", "")
                            .replace("~", "")
                            .strip()
                        ),
                        "image": image.get("data-src") or image.get("src"),
                        # "link": "https://www.oliveyoung.co.kr" + product_link["href"]
                        "link": product_link["href"]
                    })
                    count += 1

                if len(products) >= 150:
                    break

            print(f"[{i+1}페이지] extract: {time.time()-t:.3f}초")
            print(f"[{i+1}페이지] 전체: {time.time()-page_start:.3f}초")
        
        browser.close()
    print(
        f"올리브영 소요시간: {time.time()-start_time:.2f}초"
    )

    return products


def main():

    keyword = "기초"

    start_time = time.time()   # 시작 시간 측정

    with ThreadPoolExecutor(max_workers=2) as executor:

        musinsa_future = executor.submit(search_musinsa, keyword)
        olive_future = executor.submit(search_olive, keyword, 7)

        musinsa_products = musinsa_future.result()
        olive_products = olive_future.result()


    products = musinsa_products + olive_products

    end_time = time.time()   # 종료 시간 측정

    print("무신사:", len(musinsa_products))
    print("올리브영:", len(olive_products))
    print("전체:", len(products))

    print(f"총 실행 시간: {end_time - start_time:.2f}초")

# python scrapper.py 할 때만 실행
if __name__ == "__main__":
    main()
