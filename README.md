# stealthscraper
<p align="center">
<img width="399" alt="immagine" src="https://raw.githubusercontent.com/TheKevinWang/stealthscraper/main/logo.png">
<br>
Craiyon AI generated logo.
</p>

A social media scraper that attempts to be stealthy by using gui automation. Uses [Realistic-Mouse](https://github.com/AntoinePassemiers/Realistic-Mouse) for mouse movement. 
Currently, it relys on select all + copy for getting the url from the browser. Eventually, I want to use a plugin and also support [undetected_chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver). The idea is that plugins are harder/impossible to detect compared to something like undetected_chromedriver, which is a "cat and mouse game" of detection. 

Supports:
* LinkedIn Employees
* LinkedIn posts
* Twitter posts
* Youtube channel vid urls + descriptions
* Facebook (Post text only. Text based scraping.)

# Usage
Currently, only Chrome and Windows is supported. 
```
pip install -r requirements.txt 
# Scrapes 3 pages of employees (total of 30). First, launches a browser and waits for manual login (-w). 
python3 main.py -u 'https://www.linkedin.com/company/procter-and-gamble' -m linkedin_employees -o out.json -l 3 -w 
```
