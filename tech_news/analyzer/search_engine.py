from typing import List, Tuple
from tech_news.database import db, search_news
from datetime import datetime


def search_by_title(title: str) -> List[Tuple[str, str]]:
    """
    Busca notícias por título no banco de dados.

    Args:
        title: string com o título da notícia a ser buscada.

    Returns:
        Uma lista de tuplas com as notícias encontradas na busca, contendo
        o título e a URL da notícia. Exemplo:
        [
          ("Título1_aqui", "url1_aqui"),
          ("Título2_aqui", "url2_aqui"),
          ("Título3_aqui", "url3_aqui"),
        ]

        Caso nenhuma notícia seja encontrada, uma lista vazia é retornada.
    """
    news = db.news.find({"title": {"$regex": f".*{title}.*", "$options": "i"}})
    result = [(n["title"], n["url"]) for n in news]
    return result


def search_by_date(date: str) -> list[tuple[str, str]]:
    """
    Busca notícias no banco de dados a partir de uma data.

    Args:
        date (str): Uma string representando uma data no formato ISO.

    Returns:
        Uma lista de tuplas contendo o título e a URL das notícias encontradas.

    Raises:
        ValueError: se a data fornecida estiver em formato inválido.

    """
    try:
        date_formater = datetime.fromisoformat(date).strftime("%d/%m/%Y")
    except ValueError:
        raise ValueError("Data inválida")

    find = search_news({"timestamp": date_formater})
    news_by_date = [(news["title"], news["url"]) for news in find]

    return news_by_date


def search_by_category(category: str) -> List[Tuple[str, str]]:
    """Busca as notícias de uma determinada categoria.

    Args:
        category: Categoria a ser buscada.

    Returns:
        Uma lista de tuplas contendo o título e a URL
        de cada notícia encontrada.
    """
    regex_query = {"category": {"$regex": category, '$options': 'i'}}
    news_found = search_news(regex_query)
    news_info = [(news["title"], news["url"]) for news in news_found]
    return news_info
