# 🌍 CountryFact — World Information Portal

A feature-rich Django web application that lets you explore detailed information about every country in the world — from geography and demographics to economics, military power, live currency exchange rates, and global records.

---

## 🚀 Features

### 📋 Country Info

Look up any country and get a comprehensive detail page covering:

- **General** — official name, capital, region, subregion, population, area, coordinates
- **Identity** — flag (via flagcdn.com), coat of arms, timezone(s), calling codes, TLD, alt spellings
- **Languages & Currencies** — all official languages and currencies with symbols and codes
- **Borders** — list of neighbouring countries with clickable links
- **Economy** — GDP (nominal), GDP per capita, HDI with colour-coded progress bar, Gini coefficient, unemployment rate, inflation rate
- **Military** — Global Firepower rank badge, active & reserve personnel, defence budget
- Wikipedia link for further reading
- _Fields with no data show a clean "No data available" pill instead of a dash_

---

### ⚖️ Compare Two Countries

Side-by-side comparison of any two countries:

- **Geography** — area, region, subregion, landlocked status, borders count
- **Demographics** — population, languages, currencies, calling codes, timezones
- **Economy** — GDP, GDP per capita, HDI, Gini, unemployment, inflation
- **Military** — GFP rank, active troops, reserve troops, defence budget
- **5 interactive charts** (Chart.js) — Population, Area, GDP, Military Budget, HDI
- Searchable dropdowns powered by Tom Select

---

### 🗺️ Countries & Capitals

A sortable, searchable table of all ~196 countries listing:

- Country name, capital city, currency, region
- Data sourced from `COUNTRIESANDCAPITAL1.csv`

---

### 🏆 World Records

Global rankings and records split into themed sections:

| Section                              | What's Inside                                                                    |
| ------------------------------------ | -------------------------------------------------------------------------------- |
| **Largest & Smallest by Area**       | Top 10 largest + 5 smallest countries                                            |
| **Most Populous**                    | Top 10 most populous countries with visual bar                                   |
| **Mountains & Rivers**               | Top 10 highest peaks + longest rivers (side-by-side)                             |
| **Coastlines, Languages, Timezones** | Longest coastlines, most official languages, most timezones                      |
| **Notable Natural Records**          | Card grid — hottest place, wettest country, oldest country, longest border, etc. |
| **Population Density**               | Most densely populated countries                                                 |
| **Largest Economies (GDP)**          | Top 10 by nominal GDP with HDI indicator                                         |
| **Highest GDP per Capita**           | Top 10 wealthiest by per-capita income                                           |
| **Highest HDI**                      | Top 10 human development index with colour-coded progress bar                    |
| **Military Power Index**             | Top 10 by Global Firepower 2024 ranking                                          |

---

### 💱 Currency Exchange

- Live exchange rates fetched from the **open.er-api.com** API
- Convert any amount between any two currencies
- Searchable currency dropdowns (Tom Select) with currency names and codes

---

### 🗾 World Map

Interactive world map for visual country exploration.

---

## 🛠️ Tech Stack

| Layer          | Technology                                                                      |
| -------------- | ------------------------------------------------------------------------------- |
| Backend        | Django 5.0.6, Python 3.x                                                        |
| Data           | `countryinfo` Python package + custom `COUNTRY_EXTRA_DATA` dict (~60 countries) |
| Frontend       | Bootstrap 5, Font Awesome 6, Google Fonts (Poppins)                             |
| Charts         | Chart.js                                                                        |
| Dropdowns      | Tom Select                                                                      |
| Flags          | flagcdn.com                                                                     |
| Exchange Rates | open.er-api.com (live API)                                                      |
| Database       | SQLite (default Django)                                                         |

---

## ⚙️ Setup & Run

```bash
# 1. Clone the repo
git clone <repo-url>
cd COUNTRY-WEBSITE

# 2. Create and activate virtual environment
python -m venv myvenv
myvenv\Scripts\activate        # Windows
# source myvenv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install django countryinfo

# 4. Run migrations
python manage.py migrate

# 5. Start the development server
python manage.py runserver
```

Open `http://127.0.0.1:8000` in your browser.

---

## 📁 Project Structure

```
COUNTRY-WEBSITE/
├── Countryinfo_app/
│   ├── templates/countryinfo_app/   # All HTML templates
│   ├── static/                      # CSS & JS assets
│   ├── views.py                     # All view logic + ranking computations
│   ├── urls.py                      # App URL routes
│   ├── country_data.py              # COUNTRY_EXTRA_DATA & WORLD_RECORDS dicts
│   └── models.py
├── countryinfo_project/             # Django project settings
├── static/
│   ├── COUNTRIESANDCAPITAL1.csv     # Countries + capitals data
│   └── images/
├── myvenv/
│   └── data/                        # Per-country JSON files (countryinfo package)
└── manage.py
```

---

## 📌 Notes

- Economic and military data (`COUNTRY_EXTRA_DATA`) is manually curated for ~60 major countries. Countries without this data still show the page — missing fields display a _"No data available"_ badge.
- Currency exchange requires an active internet connection to fetch live rates.
