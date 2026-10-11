import os
import time
import re

import pandas as pd
import serpapi
import requests
import trafilatura


# ==========================================================
# CONFIGURATION
# ==========================================================

API_KEY = os.getenv("SERPAPI_KEY")

if not API_KEY:
    raise ValueError(
        "SERPAPI_KEY belum ditemukan.\n"
        "Set API key terlebih dahulu."
    )


client = serpapi.Client(
    api_key=API_KEY
)


# ==========================================================
# KEYWORDS
# ==========================================================

keywords = [
    "Bumi Resources",
    "Saham BUMI",
    "Kinerja BUMI",
    "Utang BUMI","Produksi BUMI"
]


# ==========================================================
# YEAR RANGE
# ==========================================================

years = range(2020, 2026)


# ==========================================================
# MAX PAGE PER QUERY
# ==========================================================

MAX_PAGES = 100


# ==========================================================
# REQUEST SETTINGS
# ==========================================================

REQUEST_TIMEOUT = 20


# ==========================================================
# SCRAPE GOOGLE NEWS
# ==========================================================

def scrape_google_news(keyword, year):

    results_data = []

    start_date = f"{year}-01-01"
    end_date = f"{year + 1}-01-01"

    query = (
        f'"{keyword}" '
        f"after:{start_date} "
        f"before:{end_date}"
    )

    print()
    print("-" * 70)
    print(f"KEYWORD : {keyword}")
    print(f"TAHUN   : {year}")
    print("-" * 70)

    seen_links = set()

    for page in range(MAX_PAGES):

        start = page * 10

        print(
            f"  Page {page + 1}/{MAX_PAGES} "
            f"(start={start})"
        )

        try:

            results = client.search({
                "engine": "google_news",
                "q": query,
                "gl": "id",
                "hl": "id",
                "start": start
            })

        except Exception as e:

            print(
                f"  ERROR SerpApi: {e}"
            )

            break

        news_results = results.get(
            "news_results",
            []
        )

        if not news_results:

            print(
                "  Tidak ada hasil lagi."
            )

            break

        new_results = 0

        for news in news_results:

            link = news.get("link")

            if not link:
                continue

            # ----------------------------------------------
            # DEDUPLICATION PER QUERY
            # ----------------------------------------------

            if link in seen_links:
                continue

            seen_links.add(link)

            # ----------------------------------------------
            # SOURCE
            # ----------------------------------------------

            source = news.get("source")

            if isinstance(source, dict):

                source_name = (
                    source.get("name")
                    or source.get("title")
                )

            else:

                source_name = source

            # ----------------------------------------------
            # DATE
            # ----------------------------------------------

            article_date = (
                news.get("iso_date")
                or news.get("date")
            )

            results_data.append({

                "keyword": keyword,

                "title": news.get(
                    "title"
                ),

                "link": link,

                "tanggal": article_date,

                "sumber": source_name
            })

            new_results += 1

        print(
            f"    Hasil baru: {new_results}"
        )

        # Kalau page berikutnya tidak memberikan
        # artikel baru, hentikan pagination.

        if new_results == 0:

            print(
                "    Tidak ada URL baru."
            )

            break

        time.sleep(0.5)

    print(
        f"  Total URL unik: {len(results_data)}"
    )

    return results_data


# ==========================================================
# DOWNLOAD ARTICLE
# ==========================================================

def extract_article(url):

    try:

        downloaded = trafilatura.fetch_url(
            url
        )

        if not downloaded:

            return None

        text = trafilatura.extract(
            downloaded,
            include_comments=False,
            include_tables=False,
            favor_precision=True
        )

        if not text:

            return None

        return text.strip()

    except Exception as e:

        print(
            f"    Gagal extract: {url}"
        )

        return None


# ==========================================================
# CLEAN TEXT
# ==========================================================

def clean_text(text):

    if not text:
        return None

    # Menghapus whitespace berlebihan

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ==========================================================
# MAIN
# ==========================================================

all_news = []


for keyword in keywords:

    for year in years:

        news = scrape_google_news(
            keyword,
            year
        )

        all_news.extend(
            news
        )


# ==========================================================
# DATAFRAME
# ==========================================================

df = pd.DataFrame(
    all_news
)


print()
print("=" * 70)
print("HASIL SERPAPI")
print("=" * 70)

print(
    f"Total URL mentah: {len(df)}"
)


# ==========================================================
# GLOBAL DEDUPLICATION
# ==========================================================

if not df.empty:

    df = df.drop_duplicates(
        subset=["link"]
    )

    df = df.reset_index(
        drop=True
    )


print(
    f"Total URL unik: {len(df)}"
)


# ==========================================================
# EXTRACT ARTICLE CONTENT
# ==========================================================

print()
print("=" * 70)
print("MENGAMBIL ISI ARTIKEL")
print("=" * 70)


contents = []


for index, row in df.iterrows():

    print(
        f"[{index + 1}/{len(df)}] "
        f"{row['sumber']} - "
        f"{row['title']}"
    )

    content = extract_article(
        row["link"]
    )

    content = clean_text(
        content
    )

    contents.append(
        content
    )

    # Jeda supaya tidak terlalu agresif

    time.sleep(0.5)


df["isi"] = contents


# ==========================================================
# REMOVE ARTICLES WITHOUT CONTENT
# ==========================================================

before = len(df)

df = df[
    df["isi"].notna()
]

df = df[
    df["isi"].str.len() >= 200
]

df = df.reset_index(
    drop=True
)

after = len(df)


print()
print(
    f"Artikel sebelum filtering: {before}"
)

print(
    f"Artikel dengan isi valid: {after}"
)


# ==========================================================
# OUTPUT DIRECTORY
# ==========================================================

os.makedirs(
    "dataset",
    exist_ok=True
)


# ==========================================================
# FINAL DATASET
# ==========================================================

final_df = df[
    [
        "title",
        "isi",
        "tanggal",
        "sumber"
    ]
]


# ==========================================================
# SAVE CSV
# ==========================================================

output_file = (
    "dataset/"
    "dataset_berita_hilirisasi.csv"
)


final_df.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)


# ==========================================================
# SAVE BACKUP WITH URL
# ==========================================================

backup_file = (
    "dataset/"
    "dataset_berita_hilirisasi_backup.csv"
)


df.to_csv(
    backup_file,
    index=False,
    encoding="utf-8-sig"
)


# ==========================================================
# SUMMARY
# ==========================================================

print()
print("=" * 70)
print("SCRAPING SELESAI")
print("=" * 70)

print(
    f"Total dataset final: {len(final_df)}"
)

print(
    f"Dataset utama : {output_file}"
)

print(
    f"Dataset backup: {backup_file}"
)


if not final_df.empty:

    print()
    print(
        "Jumlah berita berdasarkan sumber:"
    )

    print(
        final_df["sumber"]
        .value_counts()
        .head(20)
    )