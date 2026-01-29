import streamlit as st


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def create_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )


def get_pharmacy_urls(driver, search_url):
    base_url = "https://www.pagesjaunes.fr"
    urls = []

    driver.get(search_url)

    wait = WebDriverWait(driver, 15)
    wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'a.bi-denomination.pj-link')
        )
    )

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    elements = driver.find_elements(By.CSS_SELECTOR, 'a.bi-denomination.pj-link')

    for e in elements:
        href = e.get_attribute("href")
        if href:
            if href.startswith("/"):
                href = base_url + href
            if "annuaire" not in href:
                urls.append(href)

    return list(set(urls))  # supprime les doublons


def scrape_pharmacy(driver, url):
    driver.get(url)

    # Nom
    try:
        nom = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "div.col-sm-7.col-md-8.col-lg-9.denom h1")
            )
        ).text.replace("\nOuvrir la tooltip", "").strip()
    except:
        nom = None

    # Adresse(s)
    try:
        elements = driver.find_elements(
            By.CSS_SELECTOR,
            "a.teaser-item.black-icon.address.streetAddress.map-click-zon.pj-lb.pj-link span"
        )
        adresses = [e.text.strip() for e in elements if "Loca" not in e.text]
        adresse_complete = " | ".join(adresses)
    except:
        adresse_complete = None

    return {
        "URL": url,
        "Nom_Entreprise": nom,
        "Adresse": adresse_complete
    }


def scrape_all_pharmacies(urls):
    driver = create_driver(headless=True)
    data = []

    try:
        for url in urls:
            data.append(scrape_pharmacy(driver, url))
    finally:
        driver.quit()

    return pd.DataFrame(data)



def main(search_url):
    

    driver = create_driver(headless=False)

    try:
        urls = get_pharmacy_urls(driver, search_url)
    finally:
        driver.quit()

    df = scrape_all_pharmacies(urls)
    return df







with st.form("my_form"):
    reason = st.text_input("Write here ...")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Send")
    if submitted:
        st.write("ATTENDRE 30 SECONDES ")
        st.write(reason)
        df = main(reason)
        st.dataframe(df)

st.write("-----------")