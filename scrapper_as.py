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
        # print(jobs)
    return jobs


def saramin_incruit(keyword):

    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
    }

    re = requests.get(f"https://www.saramin.co.kr/zf_user/search?search_area=main&search_done=y&search_optional_item=n&searchType=recently&searchword={keyword}", headers=headers) # GET 요청을 보내서 해당 URL의 응답(Response)을 받아오는 함수

    # print(re)
    htm = BeautifulSoup(re.text, "html.parser")
    line = htm.find_all("div", class_ = "item_recruit")


    jobs = []

    for l in line:
        # print(l.text)
        company = l.find("a", class_="track_event data_layer").text # .text를 하면 문자만 나옴
        title = l.find ("h2", class_ = "job_tit").find("a").get("title")
        location = l.find("div", class_ = "job_condition").find_all("span")[0].text
        link = l.find("a", class_ = "data_layer").get("href") # href =의 값을 가져온다

        #print(link)


        jobs_data = {
            "company" : company,
            "title" : title,
            "location" : location,
            "link" : link
        }
        jobs.append(jobs_data)
        # print(jobs)

    return jobs
