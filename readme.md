
```markdown
# Dice Job Listings Scraper

This is a web scraper that extracts job listings from Dice.com. It navigates through the job listings, clicks on each job to view more details, and extracts relevant information such as the job title, company, location, and recruiter information.

## Installation

This project requires Python 3.6 or later. You'll also need to install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

To run the scraper, use the following command:

```bash
python app.py
```

The scraper will start navigating through Dice.com and extracting job listings. The data is saved in a CSV file named `dice_listings.csv`.

## How It Works

The scraper uses Selenium WebDriver to navigate the website and BeautifulSoup to parse the HTML and extract the data. It uses CSS selectors to find the elements on the page.

The scraper first finds all the job cards on the page, then it iterates over each card, clicking on it to view more details. It then extracts the job title, company, location, and recruiter information, and adds it to a pandas DataFrame. The DataFrame is then saved to a CSV file.

## Troubleshooting

If the scraper is unable to find an element on the page, it may be because the page has not finished loading. You can adjust the sleep times in the code to wait longer for the page to load.

If you encounter any other issues, please open an issue on GitHub.

## Contributing

Contributions are welcome! Please open a pull request with your changes.

## License

This project is licensed under the MIT License.