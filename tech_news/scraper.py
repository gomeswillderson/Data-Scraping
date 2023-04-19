import time
import requests
from bs4 import BeautifulSoup
from typing import Optional, List
from datetime import datetime
from tech_news.database import create_news


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


def scrape_next_page_link(html_content: str) -> Optional[str]:
    """
    Faz o scrape do conteúdo HTML de uma página de novidades para
    obter a URL da próxima página.

    Parâmetros:
        html_content (str): Conteúdo HTML da página de novidades.

    Retorna:
        str ou None: URL da próxima página, caso exista,
        ou None, caso contrário.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    next_page = soup.find("a", class_="next page-numbers")
    if next_page:
        return next_page["href"]
    else:
        return None


def scrape_news(html_content):
    """
    Extrai informações relevantes de uma página de notícia
    a partir do seu conteúdo HTML.

    Args:
        html_content (str): O conteúdo HTML da página de notícia.

    Returns:
        dict: Um dicionário contendo as informações extraídas da página,
        incluindo o título,resumo, categoria, data de publicação, autor,
        tempo de leitura e URL da notícia.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    news = {}
    url = soup.find("link", {"rel": "canonical"})["href"]

    # Verifique a data das notícias e o horário de leitura
    meta_date = soup.find("li", {"class": ["meta-date", "post-modified-info"]})
    if meta_date:
        news_date = meta_date.text.split(" ")[0]
        news["timestamp"] = datetime.strptime(news_date, "%d/%m/%Y").strftime(
            "%d/%m/%Y"
        )

        reading_time = soup.find("li", {"class": "meta-reading-time"})
        if reading_time:
            reading_time = reading_time.text.split(" ")[0]
            news["reading_time"] = int(reading_time)

        news["category"] = soup.find("span", {"class": "label"}).text
    else:
        # Verifique o tempo de leitura em uma tag específica
        reading_time = soup.find(
            "meta",
            {
                "name": lambda value: value
                and str(value).startswith("twitter:data"),
                "content": lambda value: value if "minutos" in value else "",
            },
        )
        if reading_time:
            reading_time = reading_time["content"].split(" ")[0]
            news["reading_time"] = int(reading_time)

        # Verifique a data de notícias em uma classe específica
        news_date = soup.find("div", {"class": "topic-page-title-meta"})
        if news_date:
            news_date = news_date.text.replace("Última atualização", "")
            news["timestamp"] = datetime.strptime
            (news_date, "%d/%B/%Y").strftime(
                "%d/%m/%Y"
            )

        # Extrair categoria do URL
        news["category"] = url.split("/")[3].title()

    # Extrair informações de notícias restantes
    news["url"] = url
    news["title"] = soup.find("h1", {"class": "entry-title"}).text.strip()
    news["writer"] = soup.find("a", {"class": "url fn n"}).text
    news["summary"] = (
        soup.find("div", {"class": "entry-content"}).find("p").text.strip()
    )

    return news


def get_tech_news(amount: int) -> List[str]:
    """
    Obtém notícias de tecnologia do blog da Trybe.

    Args:
        amount (int): Quantidade de notícias a serem obtidas.

    Returns:
        List[str]: Lista contendo as notícias obtidas.
    """
    url = "https://blog.betrybe.com"
    scraper = []

    # Obter links das atualizações do blog
    html_content = fetch(url)
    get_all_links = scrape_updates(html_content)

    # Obter mais links até atingir a quantidade desejada
    while len(get_all_links) < amount:
        next_page = scrape_next_page_link(html_content)
        html_content = fetch(next_page)
        get_page_links = scrape_updates(html_content)
        get_all_links.extend(get_page_links)

    # Extrair notícias a partir dos links obtidos
    for link in get_all_links[:amount]:
        html_content = fetch(link)
        scraper.append(scrape_news(html_content))

    # Criar notícias
    create_news(scraper)

    # Retornar as notícias extraídas
    return scraper
