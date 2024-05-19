import requests
import streamlit as st

def fetch_data_from_api(url):
    '''Return the json data fetched from the given url'''

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None


def extract_citations(source):
    '''Return the all the citations present in the source list passed'''

    citations = []
    # source is list of objects
    for obj in source:
        temp_obj = {}
        link = obj.get("link")
        id = obj.get("id")

        if link != "":
            temp_obj["id"] = id
            temp_obj["link"] = link

        if temp_obj:
            citations.append(temp_obj)
    return citations


def fetch_all_citations_from_api(api_url):
    '''Return all the citations from all pages of the API'''

    all_citations = []
    page = 1

    while True:
        page_url = f"{api_url}?page={page}"
        response = fetch_data_from_api(page_url)
        data = response.get("data")
        # get url for next page
        next_url = data.get("next_page_url")
        data = data.get("data")
        if not data:
            break

        for data_obj in data:
            # import pdb; pdb.set_trace()
            source = data_obj.get("source")
            citations = extract_citations(source)
            all_citations.extend(citations)

        page += 1
        # as the pages will end there will be no next url and we exit the loop
        if next_url is None:
            break
    return all_citations

if __name__ == "__main__":
    api_url = "https://devapi.beyondchats.com/api/get_message_with_sources"
    citations = fetch_all_citations_from_api(api_url)

    # print(citations)
    st.json({
        "citations": citations
    })
