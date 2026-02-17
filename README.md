<img width="1815" height="857" alt="third" src="https://github.com/user-attachments/assets/424bd8d3-41b6-4f44-b64b-d708fc06585b" /><img width="1815" height="857" alt="third" src="https://github.com/user-attachments/assets/95218af2-cec9-4114-8475-8e2a1e0ee8a4" />El Pais Opinion Scraper & Analyzer(browserstack assignment)

Watch the full automation suite running in real-time:

> CLICK HERE TO WATCH THE SCREEN RECORDING <
> https://drive.google.com/file/d/1VJ14uB36yK-I6lIT6JTSVMldV8iXxm2k/view?usp=drive_link

Below are the execution outputs from the parallel run involving Chrome (Windows), Firefox (macOS), Edge (Windows), Samsung Galaxy S22 (Android), and iPhone 14 Pro (iOS).
<img width="1855" height="760" alt="first" src="https://github.com/user-attachments/assets/242fc6e1-8dd3-4e28-b804-4b80392d40ea" />
<img width="1830" height="810" alt="second" src="https://github.com/user-attachments/assets/4619cb01-43e1-4181-bc29-3ab9c2864c83" />
<img width="1815" height="857" alt="third" src="https://github.com/user-attachments/assets/ecaa85a7-6636-40bf-a6f5-08ec6419c1c0" />
<img width="1811" height="857" alt="fourth" src="https://github.com/user-attachments/assets/07943a39-c823-4af2-9fe5-6a87b378c4f6" />
<img width="1464" height="823" alt="fifth" src="https://github.com/user-attachments/assets/4345b395-cb70-48a4-9092-0cda59727a1e" />

Technical Implementation
Core Features

    Cross-Browser Parallel Execution: Leverages Python's ThreadPoolExecutor to run 5 concurrent sessions.

    Smart Content Extraction: Scrapes titles, content summaries, and cover images. Handles mobile lazy-loading gracefully.

    Automated Translation: Translates Spanish headers to English using the Rapid Translate API.

    Data Analysis: Identifies repeated words in translated headers (>2 occurrences).

    Robust Error Handling: Manages cookie banners, network timeouts, and element visibility checks.

Setup & Installation

1. Clone the Repository
Bash

git clone https://github.com/YOUR_USERNAME/elpais-scraper.git
cd elpais-scraper

2. Install Dependencies
Bash

pip install -r requirements.txt

3. Configure Environment Variables
Create a .env file in the root directory:
Ini, TOML

BROWSERSTACK_USERNAME=your_username
BROWSERSTACK_ACCESS_KEY=your_access_key
RAPIDAPI_KEY=your_rapidapi_key

How to Run

Execute the main script to launch the parallel test suite:
Bash

python browserstack.py

Project Structure

    browserstack.py: Main script containing the scraping class and threading logic.

    requirements.txt: List of Python dependencies.

    .env: Configuration file for API keys (excluded from version control).

    .gitignore: Specifies intentionally untracked files to ignore.

    README.md: Project documentation.

Author: [Your Name]
