import os
from time import sleep

for i in range(80):
    sleep(3)
    response = requests.get(
        f'https://www.cisa.gov/known-exploited-vulnerabilities-catalog?page={i}',
        headers={"T-Agent": "Vurnelabilities_project"},
        timeout=10
    )
    print(f'Strona ({i+1}/80)')
    filepath = os.path.join(PATH, f'page{i}.html')

    with open(filepath, 'w', encoding='utf-8') as f:
              f.write(response.text)


