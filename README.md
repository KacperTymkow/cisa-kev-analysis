# 🔐 CISA KEV Analysis

Scraper i analiza danych z oficjalnego katalogu **CISA Known Exploited Vulnerabilities (KEV)** — bazy rządu USA zawierającej potwierdzone, aktywnie exploitowane podatności.

---

## 📌 O projekcie

CISA (Cybersecurity and Infrastructure Security Agency) publikuje katalog luk bezpieczeństwa, które są aktywnie wykorzystywane przez atakujących. Projekt pobiera te dane, parsuje je do DataFrame i przeprowadza analizę obejmującą:

- Którzy vendorzy mają najwięcej exploitowanych produktów
- Jakie typy podatności (CWE) dominują
- Trendy czasowe — które lata i miesiące są "gorące"
- Jakie typy ataków najczęściej pojawiają się w opisach luk
- Tłumaczenie opisów luk na język polski

**Źródło danych:** https://www.cisa.gov/known-exploited-vulnerabilities-catalog

---

## 📁 Struktura projektu

```
cisa-kev-analysis/
│
├── scraper.py          # Pobiera strony HTML z katalogu CISA i zapisuje lokalnie
├── parser.py           # Parsuje HTML → buduje DataFrame i zapisuje CSV
├── analysis.ipynb      # Analiza i wizualizacje
│
├── html_pages/         # Pobrane strony HTML (ignorowane przez git)
├── vulnerabilities.csv # Wynikowy dataset (ignorowany przez git)
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Instalacja

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
requests
beautifulsoup4
pandas
matplotlib
seaborn
googletrans==4.0.0rc1
```

---

## 🚀 Jak uruchomić

### Krok 1 — Pobierz strony HTML

```bash
python scraper.py
```

Pobiera strony 0–79 z katalogu CISA i zapisuje do folderu `html_pages/`.
Między requestami jest 3-sekundowa przerwa — nie spamuj serwera rządowego 🙏

> ⚠️ Zmień zmienną `PATH` w `scraper.py` na swoją ścieżkę lokalną.

### Krok 2 — Parsuj HTML do DataFrame

```bash
python parser.py
```

Otwiera każdy plik HTML, wyciąga dane i zapisuje `vulnerabilities.csv`.

### Krok 3 — Analiza

Otwórz `analysis.ipynb` w Jupyter i uruchom komórki po kolei.

---

## 📊 Analizy

| Analiza | Opis |
|---|---|
| Top vendorzy | Którzy producenci mają najwięcej exploitowanych produktów |
| Najczęstsze CWE | Dominujące typy słabości (SQL Injection, Path Traversal, RCE...) |
| Trendy roczne | Liczba luk dodanych do katalogu per rok |
| Sezonowość | Agregat miesięczny — czy istnieją wzorce sezonowe |
| Typy ataków (NLP) | Klasyfikacja opisów luk po słowach kluczowych |
| Tłumaczenia | Opisy luk przetłumaczone na język polski via googletrans |

---

## 🗃️ Kolumny datasetu

| Kolumna | Opis |
|---|---|
| `cve_id` | Unikalny identyfikator podatności (np. CVE-2024-1234) |
| `vendor_product` | Producent i produkt (np. Microsoft \| Windows) |
| `vulnerability_name` | Nazwa luki |
| `description` | Opis podatności (EN) |
| `description_PL` | Opis podatności (PL) |
| `cwe_id` | Typ słabości (np. CWE-89) |
| `cwe_link` | Link do definicji CWE |
| `ransomware` | Czy luka była używana w kampaniach ransomware |
| `action` | Wymagana akcja zaradcza |
| `date_added` | Data dodania do katalogu CISA |
| `due_date` | Deadline na wdrożenie poprawki |

---

## 🔍 Ciekawe obserwacje

- **2022** był rekordowym rokiem pod względem liczby exploitów w katalogu
- Wyraźna sezonowość — piki w **marcu** i **listopadzie**
- **Microsoft** dominuje wśród vendorów z największą liczbą podatności
- **Path Traversal** i **improper authentication** to najczęstsze typy ataków

---

## 📝 Uwagi techniczne

- `googletrans` jest niestabilne przy dużej liczbie requestów — tłumaczenie puszczane jest w paczkach po 50 rekordów z przerwami
- Strona CISA może zwracać 403 bez odpowiedniego `User-Agent` — scraper używa nagłówka przeglądarki
- Dataset zawiera ~1580 rekordów (stan na maj 2025)