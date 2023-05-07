from time import sleep
import pyautogui
from rmm.mouse import Mouse
import numpy as np
import shlex
import subprocess

mouse = Mouse(speed=1.7, mode=Mouse.Mode.TRACKPAD)

#clicks on an image.
# @param img_path filepath to img
# @param clickcnt how may times to click the image (ie double click = 2)
# @param x y area within the image click. percentage.
def clickImg(img_path,conf=0.9,x=.5,y=.5,clickcnt=1,reload_all=False,all=False,retries=0,rando=False):
    if(rando):
        x = abs(np.random.normal(.5, .2, 1)[0])
        y = abs(np.random.normal(.5, .2, 1)[0])
        #TODO: fix this ugly shit lol
        if x > 1:
            x = 1
        if y > 1:
            y = 1
    for i in range(retries+1):
        sleep(1)
        if all:
            imgs = list(pyautogui.locateAllOnScreen(img_path, confidence=conf))
        else:
            imgs = [pyautogui.locateOnScreen(img_path, confidence=conf)]
        if len(imgs) > 0 and imgs[0] != None: #fix this shit lol
            imgFound = True
            break
    if not imgFound:
        return False
        #raise Exception("Image not found.")
    for img in imgs:
        if img:
            mouse.move_to(img.left + img.width * x, img.top + img.height * y)
            mouse.click(clickcnt)
            normal_sleep(.1)

#click on middle by default
#TODO: fix this messy shit lol
def click_img_until_gone(img_path, conf=0.9, x=.5, y=.5, clickcnt=1, reload_all=False, all=False, retries=0):
    imgExists = True
    while imgExists:
        imgFound = False
        for i in range(retries+1):
            sleep(.1)
            if all:
                imgs = list(pyautogui.locateAllOnScreen(img_path, confidence=conf))
            else:
                imgs = [pyautogui.locateOnScreen(img_path, confidence=conf)]
            if len(imgs) > 0 and imgs[0] != None: #fix this shit lol
                imgFound = True
                break
        if not imgFound:
            imgExists = False
            return False
            #raise Exception("Image not found.")
        for img in imgs:
            if img:
                mouse.move_to(img.left + img.width * x, img.top + img.height * y)
                mouse.click(clickcnt)
                normal_sleep(.1)
#scrolls for 3 "rounds"
def scroll_down(scroll_num = 700):
    scroll_num = -1 * scroll_num
    pyautogui.scroll(scroll_num + np.random.randint(-100, 100))
    normal_sleep(.01)
    pyautogui.scroll(scroll_num + np.random.randint(-100, 100))
    normal_sleep(.01)
    pyautogui.scroll(scroll_num + np.random.randint(-100, 100))
    normal_sleep(.01)

#credit to https://stackoverflow.com/a/20577580
def dequote(s):
    """
    If a string has single or double quotes around it, remove them.
    Make sure the pair of quotes match.
    If a matching pair of quotes is not found,
    or there are less than 2 characters, return the string unchanged.
    """
    if (len(s) >= 2 and s[0] == s[-1]) and s.startswith(("'", '"')):
        return s[1:-1]
    return s

#Sleep with normal distribution delay added to it for realism.
def normal_sleep(dur=1, mean=0.0, sd=0.2):
    sleep(dur + abs(np.random.normal(mean, sd, 1)[0]))

#moves mouse randomly to the left. still needs a bit of y movement to be realistic.
def move_mouse_rand_L(pixelsToMove, xLim=5, yLim=5):
    pos = pyautogui.position()
    mouse.move_to(pos.x+pixelsToMove+np.random.randint(-1*xLim,xLim), pos.y+np.random.randint(-1*yLim,yLim))

#go to url into a browser window using shortcut
def browser_sc_nav_to(url):
    pyautogui.hotkey('ctrl', 'l')  # focus url hotkey
    pyautogui.write(url)
    pyautogui.press('enter')

def sc_exit_active_wnd():
    pyautogui.hotkey('alt', 'f4')

#uses active window title to verify browser has started
def start_browser(browser,path):
    if browser == 'ff':
        browser_cmd = '"' + path + '"' + ' --private-window'
        window_text = 'Mozilla Firefox'
    elif browser == 'chrome':
        browser_cmd = '"' + path + '"' + ' -incognito'
        window_text = "Chrome"
    elif browser == "tor":
        browser_cmd = '"' + path + '"'
        window_text = 'Tor'
    #os.system(browser_cmd)
    subprocess.Popen(shlex.split(browser_cmd), start_new_session=True)
    didBrowserStart = False

    for i in range(15):
        sleep(.3)
        try:
            active_window = pyautogui.getActiveWindowTitle()
        except: #probably linux or macos where getActiveWindowTitle() not supported. just assume it started
            sleep(1)
            didBrowserStart = True
            break #TODO: refactor
        if window_text in active_window:
            didBrowserStart = True
            break
    if not didBrowserStart:
        raise Exception("Browser failed to start.")
        #return False
    sleep(.7)

from random import randint
#credit to Pithikos https://stackoverflow.com/a/61730849
def get_dominant_color(pil_img):
    img = pil_img.copy()
    img = img.convert("RGBA")
    img = img.resize((1, 1), resample=0)
    dominant_color = img.getpixel((0, 0))
    return dominant_color

def get_dominant_color(pil_img, palette_size=16):
    # Resize image to speed up processing
    img = pil_img.copy()
    img.thumbnail((100, 100))

    # Reduce colors (uses k-means internally)
    paletted = img.convert('P', palette=Image.ADAPTIVE, colors=palette_size)

    # Find the color that occurs most often
    palette = paletted.getpalette()
    color_counts = sorted(paletted.getcolors(), reverse=True)
    palette_index = color_counts[0][1]
    dominant_color = palette[palette_index*3:palette_index*3+3]

    return dominant_color

#scrolls down and copies everything
#TODO:complete this. havent added func pointer for scrape yet
'''
def scrollLoop():
    no_new_posts_count = 0
    i = 0
    while i < 3:
        num_posts_begin = len(text_scraper.posts)
        normalSleep(.5)
        pyautogui.hotkey('ctrl', 'a')
        normalSleep(.1)
        pyautogui.hotkey('ctrl', 'c')
        normalSleep(.1)
        try:
            all_cpy = Tk().clipboard_get()
        except:
            print('exception lol')

        #text_scraper.scrape_linkedin_posts(all_cpy)
        #TODO add func pointer here for scrape

        normalSleep(1)
        moveMouseRandoL(1)
        scroll_down(1200)
        # pyautogui.press('space')
        # normalSleep(.1)
        # pyautogui.press('space')
        # normalSleep(.1)
        # pyautogui.press('space')
        print('total scraped: ' + str(len(html_scraper.posts)))

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
'''