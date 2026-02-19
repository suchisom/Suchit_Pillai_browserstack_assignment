<img width="1913" height="1009" alt="dashboard" src="https://github.com/user-attachments/assets/e6de34c0-6a1b-4b49-82e4-573398aa5657" /># El Pais Opinion Scraper & Analyzer (BrowserStack Assignment)


## Live Execution Demo

**Watch the full automation suite running in real-time:**

[**> CLICK HERE TO WATCH THE SCREEN RECORDING <**](https://drive.google.com/file/d/1VJ14uB36yK-I6lIT6JTSVMldV8iXxm2k/view?usp=drive_link)

**Build Link**

[**View Full Test Results & Videos on BrowserStack**](https://tinyurl.com/3dbxj6jz)
---

## Dashboard Verification

The script integrates directly with BrowserStack Automate. Below is the proof of the 5 parallel sessions passing successfully.

<img width="1913" height="1009" alt="dashboard" src="https://github.com/user-attachments/assets/e26c5e4c-6370-48ba-9ef3-660bc1579779" />


---

## Execution Outputs

Below are the actual execution logs from the parallel run involving Chrome (Windows), Firefox (macOS), Edge (Windows), Samsung Galaxy S22 (Android), and iPhone 14 Pro (iOS).

<img width="1855" height="760" alt="first" src="https://github.com/user-attachments/assets/e69f2371-0291-4cfa-a827-7c47ba5f80c4" />


<img width="1830" height="810" alt="second" src="https://github.com/user-attachments/assets/804f2698-3768-4320-b34f-c2101d590a35" />


<img width="1815" height="857" alt="third" src="https://github.com/user-attachments/assets/09c04c55-9b44-4a7a-9a4b-8ff4ca7cc01c" />


<img width="1811" height="857" alt="fourth" src="https://github.com/user-attachments/assets/1e605b42-17bb-49d5-b407-1f95e32c9785" />


<img width="1464" height="823" alt="fifth" src="https://github.com/user-attachments/assets/b658bcf7-1698-4aaf-9912-95b7726d3527" />


---

## Technical Implementation

### Core Features
* **Cross-Browser Parallel Execution:** Leverages Python's `ThreadPoolExecutor` to run 5 concurrent sessions.
* **Smart Content Extraction:** Scrapes titles, content summaries, and cover images. Handles mobile lazy-loading gracefully.
* **Automated Translation:** Translates Spanish headers to English using the Rapid Translate API.
* **Data Analysis:** Identifies repeated words in translated headers (>2 occurrences).
* **Robust Error Handling:** Manages cookie banners, network timeouts, and element visibility checks.

---

## Setup & Installation

### 1. Clone the Repository

git clone [[https://github.com/suchisom/Suchit_Pillai_browserstack_assignment](https://github.com/suchisom/Suchit_Pillai_browserstack_assignment)]
### 2. Install Dependencies

pip install -r requirements.txt

### 3. Configure Environment Variables

Create a .env file in the root directory: Ini, **TOML**

BROWSERSTACK_USERNAME=your_username 
BROWSERSTACK_ACCESS_KEY=your_access_key 
RAPIDAPI_KEY=your_rapidapi_key

### How to Run

Execute the main script to launch the parallel test suite:

python browserstack.py
