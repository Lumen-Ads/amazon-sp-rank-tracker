# Amazon Rank Tracker - eCommerce Marketing Tool

Amazon Rank Tracker is a powerful Python-based application designed to help businesses and eCommerce marketing agencies track sponsored product rankings on Amazon. This tool enables **Amazon marketing** professionals to monitor product performance and optimize ad strategies effectively.

## Key Features

- **Track Sponsored Rankings** – Monitor keyword rankings for Amazon-sponsored products.
- **Excel File Support** – Upload an Excel file with ASINs and keywords for automated tracking.
- **Data Export** – Save results back to an Excel file for further analysis.
- **User-Friendly Interface** – Interactive and responsive UI built with PyQt.
- **Automated Web Scraping** – Uses Selenium to fetch real-time ranking data.

## Why Use Amazon Rank Tracker?

For **eCommerce marketing agencies**, staying ahead in **Amazon marketing** requires precise tracking of ad performance. This tool streamlines that process, making campaign optimization more data-driven and efficient.

## Requirements

To run this application, install Python along with the following dependencies:

- PyQt5
- Selenium
- pandas
- openpyxl
- webdriver-manager
- beautifulsoup4
- xlsxwriter
- fake-useragent

Install them using:

```
pip install -r requirements.txt
```

## How to Use

1. **Clone the repository:**
   ```
   git clone https://github.com/Lumen-Ads/amazon-sp-rank-tracker.git
   ```
2. **Navigate to the project directory:**
   ```
   cd amazon-sp-rank-tracker
   ```
3. **Run the application:**
   ```
   python src/main.py
   ```
4. **Upload your Excel file**, start tracking, and download results.

## Project Structure

```
amazon-rank-tracker
├── src
│   ├── main.py
│   ├── ui
│   │   ├── __init__.py
│   │   └── main_window.py
│   ├── scraper
│   │   ├── __init__.py
│   │   └── amazon_scraper.py
│   └── utils
│       ├── __init__.py
│       ├── selenium_setup.py
│       └── excel_handler.py
├── requirements.txt
├── README.md
└── .gitignore
```

## License

This project is licensed under the MIT License:

```
MIT License

Copyright (c) 2025 Cliqby Commerce LLP

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Learn More

For expert insights on **Amazon marketing** and **eCommerce marketing strategies**, visit **[Cliqby](https://cliqby.com)**.
