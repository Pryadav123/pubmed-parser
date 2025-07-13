import xml.etree.ElementTree as ET
from typing import List, Dict, Any

COMPANY_KEYWORDS = ["inc", "ltd", "llc", "corp", "pharmaceuticals", "biotech", "therapeutics"]
ACADEMIC_KEYWORDS = ["university", "college", "institute", "hospital", "school of medicine", "research center"]

def is_non_academic(affiliation: str) -> bool:
    lower_affiliation = affiliation.lower()
    has_company_keyword = any(keyword in lower_affiliation for keyword in COMPANY_KEYWORDS)
    is_not_academic = not any(keyword in lower_affiliation for keyword in ACADEMIC_KEYWORDS)
    return has_company_keyword or (affiliation and is_not_academic)

def parse_pubmed_xml(xml_data: str) -> List[Dict[str, Any]]:
    if not xml_data:
        return []
    results = []
    root = ET.fromstring(xml_data)
    for article in root.findall(".//PubmedArticle"):
        paper_data = {
            "PubmedID": "", "Title": "", "Publication Date": "",
            "Non-academic Author(s)": [], "Company Affiliation(s)": [],
            "Corresponding Author Email": "Not Available"
        }
        pmid_node = article.find(".//PMID")
        if pmid_node is not None: paper_data["PubmedID"] = pmid_node.text
        title_node = article.find(".//ArticleTitle")
        if title_node is not None: paper_data["Title"] = "".join(title_node.itertext()).strip()
        pubdate_node = article.find(".//PubDate")
        if pubdate_node is not None:
            year = pubdate_node.findtext("Year", "")
            month = pubdate_node.findtext("Month", "")
            day = pubdate_node.findtext("Day", "")
            paper_data["Publication Date"] = f"{year}-{month}-{day}"
        
        non_academic_authors, company_affiliations = set(), set()
        author_list_node = article.find(".//AuthorList")
        if author_list_node:
            for author in author_list_node.findall(".//Author"):
                full_name = f'{author.findtext("ForeName", "")} {author.findtext("LastName", "")}'.strip()
                affiliation_info = author.find(".//AffiliationInfo/Affiliation")
                if affiliation_info is not None:
                    affiliation_text = "".join(affiliation_info.itertext()).strip()
                    if is_non_academic(affiliation_text):
                        non_academic_authors.add(full_name)
                        company_affiliations.add(affiliation_text)
        
        if non_academic_authors:
            paper_data["Non-academic Author(s)"] = sorted(list(non_academic_authors))
            paper_data["Company Affiliation(s)"] = sorted(list(company_affiliations))
            results.append(paper_data)
    return results