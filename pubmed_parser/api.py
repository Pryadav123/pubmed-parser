import httpx
from typing import List

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

def search_pubmed(query: str, max_results: int = 20) -> List[str]:
    search_url = f"{BASE_URL}esearch.fcgi"
    params = { "db": "pubmed", "term": query, "retmax": max_results, "retmode": "json" }
    try:
        with httpx.Client() as client:
            response = client.get(search_url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("esearchresult", {}).get("idlist", [])
    except httpx.RequestError as e:
        print(f"An error occurred while searching PubMed: {e}")
        return []

def fetch_paper_details(pmids: List[str]) -> str:
    if not pmids:
        return ""
    fetch_url = f"{BASE_URL}efetch.fcgi"
    params = { "db": "pubmed", "id": ",".join(pmids), "rettype": "abstract", "retmode": "xml" }
    try:
        with httpx.Client() as client:
            response = client.get(fetch_url, params=params)
            response.raise_for_status()
            return response.text
    except httpx.RequestError as e:
        print(f"An error occurred while fetching paper details: {e}")
        return ""