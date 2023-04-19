from typing import List, Tuple
from tech_news.database import db


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


# Requisito 8
def search_by_date(date):
    """Seu código deve vir aqui"""


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
