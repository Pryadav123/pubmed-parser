# PubMed Paper Parser

This is a command-line tool that fetches research papers from PubMed based on a query, filters for papers with authors affiliated with pharmaceutical or biotech companies, and saves the results to a CSV file.

## Code Organization

The project is structured into three main Python modules:
* `api.py`: Handles all communication with the external PubMed API.
* `parser.py`: Contains the logic for parsing the raw API data and filtering it based on author affiliations.
* `cli.py`: Provides the command-line interface for the user to interact with the program, using Python's `argparse`.

## Installation

1.  Clone the repository:
    ```bash
    git clone [https://github.com/Pryadav123/pubmed-parser.git](https://github.com/Pryadav123/pubmed-parser.git)
    cd pubmed-parser
    ```
2.  Install the dependencies using Poetry:
    ```bash
    poetry install
    ```

## Usage

To run the program, use the following command structure. You will need to find the path to your project's Python interpreter first.

1.  Find the Python path:
    ```bash
    poetry env info -p
    ```
2.  Run the script, replacing `<path_to_your_python>` with the output from the command above:
    ```bash
    <path_to_your_python>/bin/python -m pubmed_parser_prem_warriors.cli "your search query" --file results.csv
    ```

### Examples

* **Search for papers and save to a file:**
    ```bash
    <path_to_your_python>/bin/python -m pubmed_parser_prem_warriors.cli "cancer therapy Pfizer" --file output.csv
    ```
* **Search and print results to the console:**
    ```bash
    <path_to_your_python>/bin/python -m pubmed_parser_prem_warriors.cli "clinical trial phase 3"
    ```

## Tools Used
* **Python 3.9+**
* **Poetry** for dependency management.
* **httpx** for making API requests.
