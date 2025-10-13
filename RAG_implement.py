import requests
from bs4 import BeautifulSoup
import re

def fetch_morgan_cs_data():
    base_url = "https://www.morgan.edu/computer-science"
    response = requests.get(base_url, timeout=10)

    if response.status_code != 200:
        print(" Unable to fetch data from Morgan CS website.")
        return {}

    soup = BeautifulSoup(response.text, "html.parser")

    data = {}

    # Fetch course links or events
    course_links = [a.text.strip() for a in soup.find_all("a") if "COSC" in a.text]
    event_titles = [e.text.strip() for e in soup.find_all("h3") if "Event" in e.text]
    form_links = [a["href"] for a in soup.find_all("a", href=True) if "form" in a["href"].lower()]

    if course_links:
        data["COURSES"] = list(set(course_links))
    if event_titles:
        data["EVENTS"] = event_titles
    if form_links:
        data["FORMS"] = form_links

    return data


def update_section(file_path, section_name, new_items):
    """
    Replaces or appends the specified section in the knowledge base file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    pattern = rf"\[{section_name}\](.*?)(?=\n\[|$)"
    new_section = f"[{section_name}]\n" + "\n".join(new_items) + "\n"

    if re.search(pattern, content, re.S):
        content = re.sub(pattern, new_section, content, flags=re.S)
    else:
        content += "\n" + new_section

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    print(f" Updated section: [{section_name}] with {len(new_items)} new items.")


def run_rag_update():
    
    # Pulls live data from Morgan’s site and updates the local knowledge base.
    
    print(" Searching latest Morgan CS info...")
    new_data = fetch_morgan_cs_data()

    if not new_data:
        print("No new data found.")
        return

    file_path = "data/knowledge_base.txt"

    for section, items in new_data.items():
        update_section(file_path, section, items)

    print("Knowledge base successfully refreshed!")


if __name__ == "__main__":
    run_rag_update()
