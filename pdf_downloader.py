import requests
from pydantic import HttpUrl

def download_pdf(pdf_url: HttpUrl):
    response = requests.get(str(pdf_url), timeout = 10)
    response.raise_for_status()
    print('response', response)
    return response.content