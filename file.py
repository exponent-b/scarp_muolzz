import csv

def save_to_csv(products):
    with open("./downloads.csv", "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)

        writer.writerow([
            "No",
            "쇼핑몰",
            "브랜드",
            "상품명",
            "가격",
            "링크"
        ])

        for i, product in enumerate(products, start=1):
            writer.writerow([
                i,
                product["site"],
                product["brand"],
                product["name"],
                product["price"],
                product["link"]
            ])