import argparse
import csv
import sys
from .api import search_pubmed, fetch_paper_details
from .parser import parse_pubmed_xml

def run():
    parser = argparse.ArgumentParser(
        description="Fetches research papers from PubMed and identifies authors from pharmaceutical or biotech companies."
    )
    parser.add_argument("query", type=str, help="The search query for PubMed.")
    parser.add_argument("-f", "--file", type=str, default="", help="Filename to save the results. Prints to console if not provided.")
    parser.add_argument("-d", "--debug", action="store_true", help="Print debug information.")

    args = parser.parse_args()

    if args.debug:
        print(f"Executing with query: '{args.query}'")

    pmids = search_pubmed(args.query)
    if not pmids:
        print("No papers found for the given query.")
        return

    if args.debug:
        print(f"Found {len(pmids)} paper IDs: {pmids}")

    xml_data = fetch_paper_details(pmids)
    if not xml_data:
        print("Could not fetch paper details.")
        return

    results = parse_pubmed_xml(xml_data)
    if not results:
        print("No papers with non-academic authors found for this query.")
        return

    output_to_csv(results, args.file)

def output_to_csv(data: list, filename: str):
    if not data:
        return
    headers = data[0].keys()
    output_stream = open(filename, 'w', newline='', encoding='utf-8') if filename else sys.stdout
    
    writer = csv.DictWriter(output_stream, fieldnames=headers)
    writer.writeheader()

    for row in data:
        row["Non-academic Author(s)"] = "; ".join(row["Non-academic Author(s)"])
        row["Company Affiliation(s)"] = "; ".join(row["Company Affiliation(s)"])
        writer.writerow(row)

    if filename:
        output_stream.close()
        print(f"Successfully saved results to {filename}")

if __name__ == "__main__":
    run()