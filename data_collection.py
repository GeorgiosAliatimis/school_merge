import requests
import random
import zipfile
import os 

def random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
    ]
    return random.choice(user_agents)

def download_csv_from_url(url,output_filename):
    user_agent = random_user_agent()
    headers = {'User-Agent': user_agent}
    r=requests.get(url,headers=headers)
    with open(output_filename, "wb") as f:
        f.write(r.content)
    

if "school_performances" not in os.listdir(): os.mkdir("school_performances")
# for year in range(2010,2019):
#     url = f"https://www.compare-school-performance.service.gov.uk/download-data?download=true&amp;regions=0&amp;filters=KS2&amp;fileformat=csv&amp;year={year}-{year+1}&amp;meta=false"
#     output_filename = f"school_performances/performances_{year}.csv"
#     download_csv_from_url(url, output_filename)

for year in range(2000,2010):
    url = f"https://www.compare-school-performance.service.gov.uk/download-data?download=true&amp;regions=0&amp;filters=KS2&amp;fileformat=xls&amp;year={year}-{year+1}&amp;meta=false"
    output_filename = f"school_performances/performances_{year}.xls"
    download_csv_from_url(url, output_filename)

# if "explanations" not in os.listdir():  os.mkdir("explanations")
# for year in range(2010,2019):
#     url = f"https://www.compare-school-performance.service.gov.uk/download-data?download=true&amp;regions=KS2&amp;filters=meta&amp;fileformat=csv&amp;year={year}-{year+1}&amp;meta=true"
#     output_filename = f"explanations/{year}.zip"
#     download_csv_from_url(url, output_filename)
#     with zipfile.ZipFile(output_filename,"r") as zip_ref:
#         zip_ref.extractall("explanations")
#     os.remove(output_filename)
#     os.rename(f"explanations/{year}-{year+1}/ks2_meta.csv",f"explanations/{year}-{year+1}.csv")