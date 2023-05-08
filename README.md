# stealthscraper
<p align="center">
<img width="399" alt="immagine" src="https://raw.githubusercontent.com/TheKevinWang/stealthscraper/main/logo.png">
<br>
Craiyon AI generated logo of a ninja holding a paint scraper. 
</p>

A social media scraper that attempts to be stealthy by using gui automation. This will start a Chrome browser and actually move the mouse and keyboard. A VM can be used to run this in the background. Uses [Realistic-Mouse](https://github.com/AntoinePassemiers/Realistic-Mouse) for mouse movement. 
Currently, it relys on select all + copy for getting the html content from the browser. Eventually, I want to use a plugin and also support [undetected_chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver). The idea is that plugins are harder/impossible to detect compared to something like undetected_chromedriver, which is a "cat and mouse game" of detection. 

Supports:
* LinkedIn Employees
* LinkedIn posts
* Twitter posts
* Youtube channel vid urls + descriptions
* Facebook (Post text only. Text based scraping.)

# Usage
Currently, only Chrome and Windows is supported. 
Install:
```
pip install -r requirements.txt 
```
Help:
```
python main.py -h                                                                                              
usage: main.py [-h] [-u URL] [-U URL_FILE] [-o OUTFILE] [-b BROWSER_PATH]
               [-m {linkedin_posts,linkedin_employees,youtube_vids,facebook_posts_txt,twitter_tweets}] [-t {txt,json}] [-usr USR] [-pwd PWD] [-w] [-l LIMIT]    

Social media scraper.

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     Url to scrape.
  -U URL_FILE, --url-file URL_FILE
                        File of urls to scrape. Use comment out using # to ignore lines
  -o OUTFILE, --out OUTFILE
                        File to dump output. If blank, output is printed
  -b BROWSER_PATH, --browser_path BROWSER_PATH
                        Path to browser. Currently, only chrome is supported.
  -m {linkedin_posts,linkedin_employees,youtube_vids,facebook_posts_txt,twitter_tweets}, --module {linkedin_posts,linkedin_employees,youtube_vids,facebook_posts
_txt,twitter_tweets}
                        Which module to use for scraping.
  -t {txt,json}, --out-type {txt,json}
                        Output raw json or text.
  -usr USR, --username USR
                        Username to use for login.
  -pwd PWD, --password PWD
                        Password to use for login.
  -w, --wait-auth       Launches a browser and waits for you to login. Press any key to continue.
  -l LIMIT, --limit LIMIT
                        Max number of scroll iterations to go through.
```
Launches a browser and waits for manual login (-w). Scrape 3 pages of LinkedIn employees (total of 30).
```
python3 main.py -u 'https://www.linkedin.com/company/procter-and-gamble' -m linkedin_employees -o out.json -l 3 -w 
```
