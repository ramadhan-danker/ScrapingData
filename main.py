
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd



# Fungsi untuk mengambil data dari halaman
def scrape_page(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    service = Service('chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)


    # Mengambil konten halaman
    content = driver.page_source
    driver.quit()

    data = BeautifulSoup(content, 'html.parser')
    flexbox2_contents = data.find_all(class_="flexbox2-content")

    results = []

    for content in flexbox2_contents:

        url = content.find("a")["href"]
        judul = content.find("div", class_="flexbox2-title").text.strip()
        spans = content.find_all("span", class_="studio")
        studios = ', '.join([span.text.strip() for span in spans])  # Mengonversi list ke string
        sinopsis = content.find("div", class_="synops").p.text.strip()
        genres = ', '.join([genre.text for genre in content.find("div", class_="genres").find_all("a")])

        results.append({

            "URL": url,
            "Judul": judul,
            "Studio": studios,
            "Sinopsis": sinopsis,
            "Genre": genres
        })

    return results


# URL dasar
base_url = 'https://sakuranovel.id/genre/romance/page/'

# Jumlah halaman di halaman pertama
page_count = 5  #jumlah halaman di sini

# Inisialisasi list untuk menyimpan semua hasil
all_results = []

# Loop melalui setiap halaman
for page_number in range(1, page_count + 1):
    url = f"{base_url}{page_number}/"
    results = scrape_page(url)
    all_results.extend(results)

# Buat DataFrame dari semua hasil
df = pd.DataFrame(all_results)

# Simpan DataFrame ke file Excel
df.to_excel("data_hasil.xlsx", index=False)

