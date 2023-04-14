import time
import requests
from bs4 import BeautifulSoup


def fetch(url: str) -> str:
    """
    Faz uma requisição HTTP GET para a URL fornecida,
    respeitando um Rate Limit de 1 requisição por segundo.

    Args:
        url: str - A URL para fazer a requisição.

    Returns:
        str - O conteúdo HTML da resposta, caso a requisição
        seja bem sucedida com Status Code 200: OK. None, caso contrário.
    """
    headers = {"user-agent": "Fake user-agent"}
    try:
        time.sleep(1)
        response = requests.get(url, headers=headers, timeout=3)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.exceptions.Timeout:
        return None


def scrape_updates(html_content: str) -> list:
    """
    Extrai uma lista de URLs de atualizações da página de novidades da Trybe.

    Args:
        html_content (str): O conteúdo HTML da página de novidades da Trybe.

    Returns:
        list: Uma lista de URLs de atualizações encontrados na página.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    news_links = soup.find_all("a", class_="cs-overlay-link")
    return [link["href"] for link in news_links]


# Requisito 3
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""


# Requisito 4
def scrape_news(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
