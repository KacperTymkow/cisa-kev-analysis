"""
CISA Known Exploited Vulnerabilities - Parser
Otwiera zapisane pliki HTML i parsuje dane do DataFrame.
"""

import os
import pandas as pd
from bs4 import BeautifulSoup


PATH = '/home/kacper/Dokumenty/vurn/'


def scrape_file(filepath: str) -> list[dict]:
    """
    Parsuje jeden plik HTML z katalogu CISA KEV.
    Zwraca listę słowników — każdy słownik to jedna podatność.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # --- Vendor | Product ---
    meta_list = [n.text.strip() for n in soup.find_all(class_='c-teaser__meta')]

    # --- CVE ID ---
    title_list = [n.find('span').text.strip() for n in soup.find_all(class_='c-teaser__title')]

    # --- Nazwa luki i opis ---
    vuln_names = []
    descriptions = []
    for n in soup.find_all(class_='c-teaser__vuln-name'):
        vuln_names.append(n.find(string=True, recursive=False).strip())
        descriptions.append(n.find('span').text.strip())

    # --- CWE link i ID ---
    cwe_links = []
    cwe_ids = []
    for n in soup.find_all(class_='c-teaser__cwes-line'):
        a = n.find('a')
        cwe_links.append(a['href'] if a else None)
        cwe_ids.append(a.text if a else None)

    # --- Ransomware ---
    ransomware = []
    for n in soup.find_all(class_='c-teaser__content'):
        p = n.find_all('p')
        strong = p[1].find('strong') if len(p) > 1 else None
        ransomware.append(strong.text if strong else None)

    # --- Wymagana akcja ---
    action_list = []
    for n in soup.find_all(class_='c-teaser__teaser-action'):
        action_list.append(n.find('span').next_sibling.strip())

    # --- Daty ---
    added_dates = []
    due_dates = []
    for n in soup.find_all(class_='c-teaser__teaser-dates'):
        li = n.find_all('li')
        added_dates.append(li[0].find('span').next_sibling.strip() if len(li) > 0 else None)
        due_dates.append(li[1].find('span').next_sibling.strip() if len(li) > 1 else None)

    # Łączymy wszystko w listę słowników (jeden dict = jedna luka)
    rows = []
    for i in range(len(vuln_names)):
        rows.append({
            'vendor_product':    meta_list[i]    if i < len(meta_list)    else None,
            'cve_id':            title_list[i]   if i < len(title_list)   else None,
            'vulnerability_name': vuln_names[i],
            'description':       descriptions[i],
            'cwe_link':          cwe_links[i]    if i < len(cwe_links)    else None,
            'cwe_id':            cwe_ids[i]      if i < len(cwe_ids)      else None,
            'ransomware':        ransomware[i]   if i < len(ransomware)   else None,
            'action':            action_list[i]  if i < len(action_list)  else None,
            'date_added':        added_dates[i]  if i < len(added_dates)  else None,
            'due_date':          due_dates[i]    if i < len(due_dates)    else None,
        })

    return rows


def build_dataframe(path: str) -> pd.DataFrame:
    """
    Leci po wszystkich plikach HTML w folderze,
    parsuje każdy i składa jeden duży DataFrame.
    """
    all_rows = []

    # Sortujemy pliki żeby leciały po kolei: page0, page1, ..., page79
    files = sorted([f for f in os.listdir(path) if f.endswith('.html')])
    total = len(files)

    for idx, filename in enumerate(files, start=1):
        filepath = os.path.join(path, filename)
        print(f'Parsowanie: {filename} ({idx}/{total})')

        rows = scrape_file(filepath)
        all_rows.extend(rows)

    # Budujemy DataFrame z całości
    df = pd.DataFrame(all_rows)

    # Konwertujemy daty
    df['date_added'] = pd.to_datetime(df['date_added'])
    df['due_date'] = pd.to_datetime(df['due_date'])

    print(f'\n✅ Gotowe! Łącznie {len(df)} podatności z {total} stron.')
    return df


if __name__ == '__main__':
    df_vurn = build_dataframe(PATH)
    print(df_vurn.head())
    print(df_vurn.dtypes)

    # Opcjonalnie zapisz do CSV
    df_vurn.to_csv(os.path.join(PATH, 'vulnerabilities.csv'), index=False)
    print('Zapisano do vulnerabilities.csv')