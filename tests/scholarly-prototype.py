from scholarly import scholarly

def fetch_author_info(author_name):
    # Search for the author
    search_query = scholarly.search_author(author_name)
    try:
        author_result = next(search_query)
    except StopIteration:
        return None

    # Retrieve all the details for the author
    return scholarly.fill(author_result)

def fetch_publication_titles(author_info):
    # Extract publication titles
    return [pub['bib']['title'] for pub in author_info.get('publications', [])]

def fetch_citations_for_first_publication(author_info):
    # Check if there are publications
    if not author_info.get('publications'):
        return []

    # Take a closer look at the first publication
    first_publication = author_info['publications'][0]
    filled_publication = scholarly.fill(first_publication)

    # Which papers cited that publication?
    return [citation['bib']['title'] for citation in scholarly.citedby(filled_publication)]

def write_to_file(filename, data):
    with open(filename, "w") as file:
        for item in data:
            file.write(item + "\n")

# Main execution
author_name = "NASA PLANET"
author_info = fetch_author_info(author_name)

if author_info:
    scholarly.pprint(author_info)

    # Print and write publication titles to a file
    publication_titles = fetch_publication_titles(author_info)
    print(publication_titles)
    write_to_file("publications.txt", publication_titles)

    # Print and write citation titles to a file
    citations = fetch_citations_for_first_publication(author_info)
    print(citations)
    write_to_file("citations.txt", citations)
else:
    print(f"No author found for {author_name}")
