from playwright.sync_api import sync_playwright
import time

def search_zigzag(keyword):

    start = time.time()

    products = []
    product_set = set()

    url = f"https://zigzag.kr/search?keyword={keyword}"

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page(
            viewport={"width":1280, "height":1000}
        )

        api_data = []


        def get_api(response):

            if "GetSearchResult" in response.url:
                # print("지그재그 API 발견")
                try:
                    data = response.json()
                    api_data.append(data)
                    # print("응답 저장:", len(api_data))

                except Exception as e:
                    print("json 오류", e)


        page.on("response", get_api)


        page.goto(url)

        page.wait_for_timeout(2000)


        # 무한스크롤
        for _ in range(7):
            page.mouse.wheel(0, 1000)
            page.wait_for_timeout(800)



        for data in api_data:

            try:
                items = (data["data"]["search_result"])

                # 내부에서 UX_GOODS_CARD_ITEM 찾기
                def find_products(obj):
                    result = []

                    if isinstance(obj, dict):
                        # 상품 발견
                        if obj.get("type") == "UX_GOODS_CARD_ITEM":
                            result.append(obj)
                            return result

                        for v in obj.values():
                            result.extend(find_products(v))

                    elif isinstance(obj, list):
                    
                        for x in obj:
                            result.extend(find_products(x))

                    return result

                items = find_products(items)

                print("찾은 상품:", len(items))
                
                for item in items:
                
                    product_id = item.get("catalog_product_id")

                    if not product_id:
                        continue
                    
                    if product_id in product_set:
                        continue

                    product_set.add(product_id)
                    # print(item.get("jpeg_image_url"))

                    products.append({

                        "site": "지그재그",
                        "brand": item.get("shop_name",""),
                        "name": item.get("title",""),
                        "price": int(item.get("final_price", 0)),
                        "image": (
                            item.get("jpeg_image_url")
                            or item.get("image_url")
                            or item.get("webp_image_url")
                            or ""
                        ),
                        
                        "link": item.get("product_url","")
                    })

                    
                    if len(products) >= 150:
                        break


            except Exception as e:
                print("파싱 오류:", e)


            if len(products) >= 150:
                break

        browser.close()


    print(
        f"지그재그 소요시간: {time.time()-start:.2f}초"
    )

    print("지그재그:",len(products))


    return products

if __name__ == "__main__":

    result = search_zigzag("반팔")

    print("\n상품 개수:", len(result))

    for p in result[:5]:
        print("----------------")
        print("브랜드:", p["brand"])
        print("상품명:", p["name"])
        print("가격:", p["price"])
        print("링크:", p["link"])