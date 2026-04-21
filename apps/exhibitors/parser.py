from bs4 import BeautifulSoup
from .models import Exhibitor


def clean_text(text):
    return " ".join(text.split())  # removes extra spaces/newlines


def parse_exhibitors(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'lxml')

    rows = soup.find_all('tr')

    count = 0

    for row in rows:
        cols = row.find_all('td')

        if len(cols) < 6:
            continue

        try:
            logo = cols[0].find('img')['src'] if cols[0].find('img') else ''

            name = clean_text(cols[1].text)
            country = clean_text(cols[2].text)
            hall = clean_text(cols[3].text)
            booth = clean_text(cols[4].text)
            sector = clean_text(cols[5].text)

            # 🚨 Avoid duplicates
            if Exhibitor.objects.filter(name=name, booth=booth).exists():
                continue

            Exhibitor.objects.create(
                name=name,
                country=country,
                hall=hall,
                booth=booth,
                sector=sector,
                logo_url=logo
            )

            count += 1

        except Exception as e:
            print("Error:", e)

    print(f"{count} records inserted.")