'''
Stealth Scraper

A social media scraper that attempts to be stealthy by using gui automation.

TODO: browser plugin instead of select all + copy.
TODO: simulate realistic typing delays (not just random)
TODO: transparent mode: scrapes in background with user or other program controlling mouse/kb
TODO: scrape impressions (like, applause, etc), comments, reposts for linkedin posts.
TODO: download images (or even better retrieve from cache) instead of just including urls
'''

from tkinter import Tk
import text_scraper
import klembord
import argparse
from pathlib import Path
from html_scraper import *
from utils import *

def copy_all(delay=.1):
    pyautogui.hotkey('ctrl', 'a')
    normal_sleep(delay)
    pyautogui.hotkey('ctrl', 'c')

#Uses pytube for scraping video url. Uses custom impl for scraping urls from channel, because pytube doesn't work for it.
def scrape_youtube_channel(url, usr='', pwd='', login=False, ff_path='C:\Program Files\Google\Chrome\Application\chrome.exe', scroll_lim=9000):
    from pytube import YouTube
    ytScrape = ytScraper()
    start_browser('chrome', ff_path)
    if login:
        None #TODO
    #for now just go straight to video.
    #more stealthy to go to main page and click videos, but not necessary on yt
    if not re.search(r"\/videos$",url):
        url += '/videos'
    browser_sc_nav_to(url)
    normal_sleep(2)
    no_new_posts_count = 0
    i = 0
    hit_bottom = False
    while i < scroll_lim and not hit_bottom:
        num_posts_begin = len(ytScrape.yt_videos)
        normal_sleep(.5)
        copy_all()
        normal_sleep(.1)
        try:
            page_html = klembord.get_with_rich_text()[1]
        except Exception as e:
            print(str(e))
        ytScrape.scrape_yt(page_html)
        normal_sleep(1)
        move_mouse_rand_L(1)
        scroll_down(1100)
        print('total scraped: ' + str(len(ytScrape.yt_videos)))

        i += 1
        num_posts_end = len(ytScrape.yt_videos)
        if num_posts_end - num_posts_begin == 0:
            no_new_posts_count += 1
            if no_new_posts_count >= 5:
                hit_bottom = True
                print('hit bottom')
        else:
            no_new_posts_count = 0
    for yt_vid in ytScrape.yt_videos:
        yt_vid['desc'] = YouTube(yt_vid['url']).description
    return ytScrape.yt_videos


def scrape_twitter_tweets(url, usr='', pwd='', login=False, ff_path='C:\Program Files\Google\Chrome\Application\chrome.exe', scroll_lim=9000):
    twtr_scrape = twitterScraper()
    start_browser('chrome',ff_path)
    if login:
        None #TODO
    browser_sc_nav_to(url)
    normal_sleep(2)
    #get rid of notification nag if it's there TODO: detect and don't do if not there
    pyautogui.press('esc')
    sleep(.1)
    scroll_down(200)
    sleep(.3)
    no_new_posts_count = 0
    i = 0
    hit_bottom = False
    while i < scroll_lim and not hit_bottom:
        num_posts_begin = len(twtr_scrape.tweets)
        normal_sleep(.5)
        copy_all()
        normal_sleep(.1)
        try:
            page_html = klembord.get_with_rich_text()[1]
        except Exception as e:
            print(str(e))
        twtr_scrape.scrape_tweets(page_html)
        normal_sleep(1)
        move_mouse_rand_L(1)
        scroll_down(1100)
        print('total scraped: '+str(len(twtr_scrape.tweets)))
        i += 1
        num_posts_end = len(twtr_scrape.tweets)
        if num_posts_end - num_posts_begin == 0:
            no_new_posts_count += 1
            if no_new_posts_count >= 5:
                hit_bottom = True
                print('hit bottom')
        else:
            no_new_posts_count = 0
    return twtr_scrape.tweets


def scrape_facebook_posts_txt(url, usr='', pwd='', login=False, ff_path='C:\Program Files\Google\Chrome\Application\chrome.exe', scroll_lim=9000):
    start_browser('chrome',ff_path)
    if login:
        None #TODO
    browser_sc_nav_to(url)
    normal_sleep(1.5)
    click_img_until_gone('images/Facebook/see_more_light.png', .8)#0.8)
    click_img_until_gone('images/Facebook/fb_see_more_light_hl.png', .8)
    copy_all()
    normal_sleep(.1)
    scroll_num = -500
    pyautogui.scroll(scroll_num+np.random.randint(-100,100))
    normal_sleep(.01)
    pyautogui.scroll(scroll_num+np.random.randint(-100,100))
    normal_sleep(.01)
    no_new_posts_count = 0
    hit_bottom = False
    i = 0
    while i < scroll_lim and not hit_bottom:
        num_posts_begin = len(text_scraper.fb_posts)
        i += 1
        #todo clickImgs()
        #clickImg('fb_see_more_light_hl.png', .8)
        click_img_until_gone('images/Facebook/fb_see_more_light_hl.png', .8)
        click_img_until_gone('images/Facebook/see_more_light.png', .8)
        normal_sleep(.1)
        copy_all()
        normal_sleep(.1)
        try:
            all_cpy = Tk().clipboard_get()
            page_html = klembord.get_with_rich_text()[1]
        except Exception as e:
            print(str(e))
        text_scraper.scrape_fb_company_posts(all_cpy)
        html_scraper.scrape_facebook_urls(page_html)
        move_mouse_rand_L(10)
        normal_sleep(.1)
        #TODO:randomize
        pyautogui.scroll(scroll_num+np.random.randint(-100,100))
        normal_sleep(.01)
        pyautogui.scroll(scroll_num+np.random.randint(-100,100))
        normal_sleep(.01)
        pyautogui.scroll(scroll_num+np.random.randint(-100,100))
        normal_sleep(.01)
        #pyautogui.press('space')
        sleep(.3)
        print('total scraped: '+str(len(text_scraper.fb_posts)))
        move_mouse_rand_L(1)
        i += 1
        num_posts_end = len(text_scraper.fb_posts)
        if num_posts_end - num_posts_begin == 0:
            no_new_posts_count += 1
            if no_new_posts_count >= 5:
                hit_bottom = True
                print('hit bottom')
        else:
                no_new_posts_count = 0

    return {'posts':text_scraper.fb_posts,'content':html_scraper.ctnt_lnks,'hrefs':html_scraper.href_lnks}

def linkedin_login(usr,pwd):
    browser_sc_nav_to()
    normal_sleep()
    # if (pyautogui.locateOnScreen('signinbtn_light.png', confidence=0.4)):
    #    clickImg('signinbtn_light.png', 0.4)
    clickImg('images/LinkedIn/usrButton.png', 0.7, retries=20)
    normal_sleep()
    pyautogui.write(usr, interval=0.1)
    pyautogui.press('tab')
    normal_sleep(.2)
    pyautogui.write(pwd, interval=0.1)
    normal_sleep()
    pyautogui.press('enter')
    # pyautogui.write(pwd, interval=0.25)
    normal_sleep(2)
    if (pyautogui.locateOnScreen('images/skip_phone.png', confidence=0.7)):
        clickImg('images/LinkedIn/skip_phone.png', 0.7, retries=20)
    # wait for everything to load up
    # TODO:react to load
    normal_sleep(3)

def scrape_linkedin_employees(url, usr='', pwd='', login=False, ff_path='C:\Program Files\Google\Chrome\Application\chrome.exe', scroll_lim=9000):
    lnknScrape = linkedinScraper()
    start_browser('chrome',ff_path)
    if login:
        linkedin_login(usr,pwd)
    browser_sc_nav_to(url)
    normal_sleep()
    clickImg('images/LinkedIn/company_emps.png', rando=True, conf=0.7, retries=20)
    normal_sleep()
    scroll_down(200)
    sleep(.3)
    no_new_posts_count = 0
    i = 0
    hit_bottom = False
    while i < scroll_lim and not hit_bottom:
        num_posts_begin = len(lnknScrape.lnkn_emps)
        copy_all()
        normal_sleep(.1)
        try:
            page_html = klembord.get_with_rich_text()[1]
        except Exception as e:
            print(str(e))

        lnknScrape.scrape_linkedin_emps(page_html)
        normal_sleep(1)
        move_mouse_rand_L(1)
        scroll_down(1100)
        clickImg('images/LinkedIn/company_emps_next_selected.png', conf=0.9, retries=20, rando=True)
        print('total scraped: ' + str(len(lnknScrape.lnkn_emps)))
        i += 1
        num_posts_end = len(lnknScrape.lnkn_emps)
        if num_posts_end - num_posts_begin == 0:
            no_new_posts_count += 1
            if no_new_posts_count >= 5:
                hit_bottom = True
                print('hit bottom')
        else:
            no_new_posts_count = 0
    return lnknScrape.lnkn_emps

def scrape_linkedin_posts(url, usr='', pwd='', login=False, ff_path='C:\Program Files\Google\Chrome\Application\chrome.exe', scroll_lim=9000):
    lnknScrape = linkedinScraper()
    start_browser('chrome', ff_path)
    if login:
        linkedin_login(usr, pwd)
    browser_sc_nav_to(url)
    normal_sleep()
    clickImg('images/LinkedIn/company_posts.png', conf=0.7, retries=20, rando=True)
    normal_sleep()
    # select all and copy. should be no partial posts
    i = 0
    no_new_posts_count = 0
    hit_bottom = False
    while i < scroll_lim and not hit_bottom:
        num_posts_begin = len(lnknScrape.lnkn_posts)
        normal_sleep(.5)
        copy_all()
        normal_sleep(.1)
        try:
            page_html = klembord.get_with_rich_text()[1]
        except Exception as e:
            print(str(e))
        lnknScrape.scrape_linkedin_posts(page_html)
        normal_sleep(1)
        move_mouse_rand_L(1)
        scroll_down(1500)
        print('total scraped: ' + str(len(lnknScrape.lnkn_posts)))
        i += 1
        num_posts_end = len(lnknScrape.lnkn_posts)
        if num_posts_end - num_posts_begin == 0:
            no_new_posts_count += 1
            if no_new_posts_count >= 4:
                hit_bottom = True
                print('hit bottom')
        else:
                no_new_posts_count = 0
    return lnknScrape.lnkn_posts
def scrape_linkedin_posts_txt(url, usr='', pwd='', login=False, ff_path='C:\Program Files\Google\Chrome\Application\chrome.exe', scroll_lim=9000):
    start_browser('chrome',ff_path)
    if login:
        linkedin_login(usr, pwd)
    browser_sc_nav_to(url)
    normal_sleep()
    clickImg('images/LinkedIn/company_posts.png', conf=0.7, retries=20)
    normal_sleep()
    #select all and copy. should be no partial posts
    i = 0
    no_new_posts_count = 0
    hit_bottom = False
    while i < scroll_lim and not hit_bottom:
        num_posts_begin = len(text_scraper.posts)
        normal_sleep(.5)
        copy_all()
        normal_sleep(.1)
        try:
            all_cpy = Tk().clipboard_get()
        except Exception as e:
            print(str(e))
        text_scraper.scrape_linkedin_posts(all_cpy)
        normal_sleep(1)
        move_mouse_rand_L(1)
        scroll_down(1200)
        print('total scraped: ' + str(len(text_scraper.posts)))
        i += 1
        num_posts_end = len(text_scraper.posts)
        if num_posts_end - num_posts_begin == 0:
            no_new_posts_count += 1
            if no_new_posts_count >= 5:
                hit_bottom = True
                print('hit bottom')
        else:
                no_new_posts_count = 0
    return text_scraper.posts

if __name__ == '__main__':
    modules = ['linkedin_posts','linkedin_employees','youtube_vids','facebook_posts_txt','twitter_tweets']
    parser = argparse.ArgumentParser(description='Social media scraper.')
    parser.add_argument('-u','--url', dest='url', type=str, help='Url to scrape.')
    parser.add_argument('-U','--url-file', dest='url_file', type=str, help='File of urls to scrape. Use comment out using # to ignore lines')
    parser.add_argument('-o','--out', dest='outFile', type=str, help='File to dump output. If blank, output is printed')
    parser.add_argument('-b','--browser_path', dest='browser_path', type=str, help='Path to browser. Currently, only chrome is supported.')
    #TODO: print desc for each module if help'd
    #TODO: auto select module based on url if not provided
    parser.add_argument('-m','--module', dest='module', choices=modules, help='Which module to use for scraping.')
    parser.add_argument('-t','--out-type', dest='outType', choices=['txt','json'], help='Output raw json or text.')
    parser.add_argument('-usr', '--username', dest='usr',type=str, help='Username to use for login.')
    #TODO more secure way of doing this...'
    parser.add_argument('-pwd', '--password', dest='pwd',type=str, help='Password to use for login.')
    parser.add_argument('-w', '--wait-auth', dest='wait_auth', action='store_true',
                        help='Launches a browser and waits for you to login. Press any key to continue.')
    parser.add_argument('-l', '--limit', dest='limit', type=int, help='Max number of scroll iterations to go through.')
    args = vars(parser.parse_args())
    if not args['url'] and not args['url_file']:
        parser.print_help()
        exit(-1)

    urls=[]
    if args['url_file']:
        with open(args['url_file']) as file:
            urls = [line.rstrip() for line in file if line[0] != '#']

    if(args['url']):
        args['url'] = dequote(args['url'])
        urls.append(args['url'])


    browser_path = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
    if args['browser_path']:
        browser_path = args['browser_path']
    if args['wait_auth']:
        start_browser('chrome', browser_path)
        browser_sc_nav_to(args['url'])
        input('Press Enter to continue...')
        print('Continuing...')
    if args['limit']:
        limit = args['limit']
    else:
        #TODO: instead of big number just dont stop
        limit = 100000
    dir_out = False
    if len(urls) > 1:
        Path(args['outFile']).mkdir(parents=True, exist_ok=True)
        dir_out = True
    for url in urls:
        if args['module'] == 'linkedin_posts':
            results = scrape_linkedin_posts(url,ff_path=browser_path, scroll_lim=limit)
        elif args['module'] == 'linkedin_employees':
            results = scrape_linkedin_employees(url,ff_path=browser_path,scroll_lim=limit)
        elif args['module'] == 'youtube_vids':
            results = scrape_youtube_channel(url,ff_path=browser_path,scroll_lim=limit)
        elif args['module'] == 'facebook_posts_txt':
            results = scrape_facebook_posts_txt(url,ff_path=browser_path,scroll_lim=limit)
        elif args['module'] == 'twitter_tweets':
            results = scrape_twitter_tweets(url,ff_path=browser_path,scroll_lim=limit)
        sleep(.1)
        #TODO: maybe reuse browser rather than close it
        #TODO: cross os compat?
        sc_exit_active_wnd()
        if args['outFile']:
            if dir_out:
                #https://www.linkedin.com/company/procter-and-gamble => procter-and-gable
                outFileName = "".join(x for x in url.split('/')[-1] if x.isalnum() or x in "._- ")+'.json'
                outFile = args['outFile']+'/'+outFileName
            else:
                outFile = args['outFile']
        if outFile:
            with open(outFile, 'w', encoding='utf-8') as handle:
                handle.write(str(results))
        else:
            print(str(results))