from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.tools import tool


@tool
def search_wikipedia(query: str) -> str:
    """Tìm kiếm thông tin trên Wikipedia."""
    search = DuckDuckGoSearchResults(output_format="list")
    results = search.run(query)
    return results