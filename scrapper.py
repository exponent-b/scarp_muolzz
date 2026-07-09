import requests
from bs4 import BeautifulSoup

def search_incruit(keyword):
    
    url = f"https://search.incruit.com/list/search.asp?col=job&kw={keyword}"
    r = requests.get(url) # GET 요청을 보내서 해당 URL의 응답(Response)을 받아오는 함수
    # print(r.text) # html코드를 들고옴

    soup = BeautifulSoup(r.text, "html.parser")
    lis = soup.find_all("li", class_ = "c_col")

    jobs = []

    for li in lis:
        company = li.find("a", class_="cpname").text # .text를 하면 문자만 나옴
        title = li.find ("div", class_ = "cell_mid").find("div", class_ = "cl_top").find("a").text
        location = li.find("div", class_ = "cl_md").find_all("span")[0].text
        link = li.find("div", class_ = "cell_mid").find("div", class_ = "cl_top").find("a").get("href") # <a 안에 href =의 값을 가져온다
        
        jobs_data = {
            "company" : company,
            "title" : title,
            "location" : location,
            "link" : link

        }

        jobs.append(jobs_data)
        print(jobs)
    return jobs



