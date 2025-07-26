# DumbWiki🤖📖

This Python application scrapes random articles from Wikipedia, extracts key information, saves the data to a CSV file, and sends an email report with a summary and the CSV attachment. It's designed to provide a quick and automated way to gather information from Wikipedia and stay informed about the scraping process.

## Table of Contents
* [✨ Features](#-features)
* [🛠️ Installation](#️-installation)
* [⚙️ Configuration](#️-configuration)
* [🚀 Usage](#-usage)
* [📁 Project Structure](#-project-structure)
* [⚠️ Important Notes](#️-important-notes)

## ✨ Features

* **Random Article Scraping:** Fetches a configurable number of random articles from Wikipedia.
* **Data Extraction:** Extracts essential information from each article, including:
    * Title
    * URL
    * First significant paragraph
    * Infobox data (if available)
    * Categories
    * Word count of the first paragraph
    * Timestamp of scraping
* **Data Storage:** Saves the scraped article data into a CSV file within a `data/` directory, with a timestamped filename for easy organization.
* **Email Notifications:** Sends an HTML-formatted email report upon completion, summarizing the scraping results. The email includes:
    * Status (success or failure)
    * Number of articles scraped
    * A summary list of scraped articles with links, word counts, and categories
    * The generated CSV file as an attachment
* **Error Handling:** Includes robust error handling for both scraping and email sending, with detailed logging.
* **Logging:** Comprehensive logging to a timestamped log file within a `logs/` directory, as well as console output, for monitoring the application's activity and troubleshooting.
* **Configurable:** Easy-to-modify settings in `config.py` for email credentials, scraping parameters (e.g., number of articles, delay), and file paths. 
* **Flexible Scraping Method:** Supports both `requests` (default) and `Selenium` for web scraping, allowing for handling of dynamic content if `use_selenium` is enabled in `scraper.py` (currently set to `False`).
* **Environment Variable Support:** Utilizes `python-dotenv` to securely load sensitive information like email credentials from a `.env` file. 

## 🛠️ Installation

1.  **Clone the repository:**

     ```bash
    git clone https://github.com/vedantbhole/dumb-wiki.git
    cd dumb-wiki
    ```


2.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Configuration

Before running the application, you need to configure your email settings and scraping preferences.

1.  **Create a `.env` file:**
    In the root directory of the project, create a file named `.env` and add the following:

    ```
    EMAIL_USER=your_email@gmail.com
    EMAIL_PASSWORD=your_app_password
    RECIPIENT_EMAIL=recipient_email@example.com
    ```

    * Replace `your_email@gmail.com` with the email address you want to send notifications *from*. 
    * Replace `your_app_password` with an [App Password](https://support.google.com/accounts/answer/185833?hl=en) if you are using Gmail with 2-Factor Authentication. **Do not use your main email password.**
    * Replace `recipient_email@example.com` with the email address you want to send notifications *to*. 

2.  **Configure `config.py`:**
    Open `config.py` to adjust scraping parameters:

    ```python
    # Email configuration (loaded from .env)
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587

    # Scraping configuration
    WIKIPEDIA_BASE_URL = 'https://en.wikipedia.org'
    MAX_ARTICLES = 5  # Number of random articles to scrape
    DELAY_BETWEEN_REQUESTS = 1 # Seconds to wait between requests

    # File paths
    DATA_DIR = 'data'
    LOGS_DIR = 'logs'
    ```

    You can modify `MAX_ARTICLES` and `DELAY_BETWEEN_REQUESTS` according to your needs. 

## 🚀 Usage

To run the Wikipedia scraper, execute the `main.py` file:

```bash
python3 main.py
```

The script will:

1. Scrape the specified number of random Wikipedia articles.

2. Save the extracted data into a CSV file in the ```data/``` directory.

3. Send an email report to the ```RECIPIENT_EMAIL``` configured in your ```.env``` file.

4. Log its activities to a file in the ```logs/```  directory and to the console.
## ⚠️ Important Notes

* **App Passwords for Gmail:** If you're using Gmail and have 2-Factor Authentication enabled (highly recommended), you **must** generate an "App password" to use instead of your regular Gmail password in the `.env` file. Using your main password directly is insecure and likely to fail.
* **Respectful Scraping:** The `DELAY_BETWEEN_REQUESTS` setting is crucial. Please keep a reasonable delay to avoid overwhelming Wikipedia's servers. Be mindful of their [Terms of Use](https://foundation.wikimedia.org/wiki/Terms_of_Use/en) and API policies.
* **Selenium Usage:** The `WikipediaScraper` class supports `use_selenium=True`, which can be enabled in `scraper.py`'s `main()` function if you encounter issues with standard `requests` for dynamic content. If using Selenium, ensure you have Chrome browser installed as `webdriver-manager` will automatically download the correct ChromeDriver.
* **Error Notifications:** In case of unexpected errors during scraping, the application attempts to send an error notification email.
