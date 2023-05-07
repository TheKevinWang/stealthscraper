'''Scrape contents from raw html of website'''
from bs4 import BeautifulSoup
import re
import validators

class twitterScraper:
    def __init__(self):
        self.tweet_set = set()
        self.tweets = []
    #TODO: add html body
    def scrape_tweets(self,htm):

        soup = BeautifulSoup(htm)
        #select tweet element
        tweet_selector = {'data-testid':'cellInnerDiv'}
        tweet_body_selector = {'data-testid':'tweetText'}
        shared_link_selector = {'data-testid':'card.wrapper'}
        tweet_divs = soup.findAll('div',tweet_selector)
        for tweet_ele in tweet_divs:
            tweet = {}
            try:
                is_retweet = not tweet_ele.find(lambda tag:tag.name=="span" and re.match(r".* Retweeted$",tag.text)) == None
                body = BeautifulSoup(str(tweet_ele.findAll('div',tweet_body_selector)[0])).get_text()
                shared_links = tweet_ele.find('div',{'data-testid':'card.wrapper'})
                if shared_links:
                    #ie when sharing a yt video link that expands inline
                    #TODO: handle this case
                    if shared_links.find('a'):
                        shared_link_href = shared_links.find('a')['href']
                    else:
                        shared_link_href = ''
                    shared_link_text = shared_links.find('span').get_text()
                time = tweet_ele.find('time')['datetime']
                #TODO: parse this
                num_rep_retw_likes = tweet_ele.find('div',{'aria-label':re.compile(r'\d* replies, .*')})
                if (num_rep_retw_likes):
                    tweet['num_rep_retw_likes'] = num_rep_retw_likes['aria-label']
                # if just "View Tweet analytics" and no "1337 Views. View Tweet analytics" then it means 0
                num_impressions = tweet_ele.find('a',{'aria-label':re.compile(r'.?View Tweet analytics$')})['aria-label']
                if num_impressions == "View Tweet analytics":
                    num_impressions = '0'
                tweet['num_impressions'] = num_impressions
                if shared_links:
                    tweet['shared_link'] = {"href": shared_link_href, "text": shared_link_text}
                tweet['isRetweet'] = is_retweet
                tweet['body'] = body
                tweet['time'] = time
                tweet['link'] = tweet_ele.find('a', {'aria-label': re.compile(r'^.*\d$|.*ago')})['href']
                if body not in self.tweet_set:
                    self.tweets.append(tweet)
                    self.tweet_set.add(body)
            except Exception as e:
                print('excpetion while scraping tweet' + str(e))

#TODO: look into hashsets instead of sets
#TODO: refactor bs4 find to use [] instead of hacks


#TODO strings to ints. sometimes string is '1,158' or who knows what else
#TODO no new lines for post body text.. they are sep eles or something
#TODO wrong image scraped(prof url)
def remove_styles(soup):
    for tag in soup():
        for attribute in ["style"]:
            del tag[attribute]
    #delete at root
    del soup[attribute]

class linkedinScraper:
    def __init__(self):
        self.lnkn_posts = []
        self.lnkn_posts_set = set()
        self.lnkn_emps = []
    def scrape_linkedin_posts(self, htm):
        soup = BeautifulSoup(htm)
        #when selecting all and copying, it includes style="" tags in everything from converting css to inline.
        # removed to avoid clutter, esp for post html body
        #TODO:refactor
        for post in soup.findAll('div',{'class': re.compile(r'.*occludable-update.*')}):
            try:
                lnkn_post = {}
                #removes these weird '\xa0' chars blocking links
                body = post.find('span',{'class':'break-words'})
                #TODO: convert this to abs date
                # '5d • ' => '5d'
                #TODO: select all copy doesn't copy <video> video src is nowhere to be found.
                video = post.find('video')
                if video:
                    lnkn_post['video_url'] = video['src']
                days_ago = post.findAll('div',{'class':['update-components-text-view', 'white-space-pre-wrap', 'break-words']})
                #TODO: better way to do this lol
                for ele in days_ago:
                    text = ele.get_text()
                    if re.match('.* • .*',text) and len(text) < 50:
                        days_ago = ele

                img_container = post.find('div',{'class':'ivm-image-view-model'})
                if (img_container):
                    lnkn_post['img_url'] = img_container.find('img',{'loading':'lazy'})['src']
                    lnkn_post['img_alt'] = img_container.find('img',{'loading':'lazy'})['alt']
                shared_link = post.find('a',{'class':re.compile(r'.?tap-target.?')})
                shared_post = post.find('article')
                reaction_cnt = post.find('span',{'class':'social-details-social-counts__reactions-count'})
                comment_cnt = post.find('button',{'aria-label':re.compile(r'^\d* comment[s]? on .*')})
                repost_cnt = post.find('button',{'aria-label':re.compile(r'^\d* repost[s]? of .*')})
                if body:
                    remove_styles(body)
                    lnkn_post['body'] = body.get_text().replace(u'\xa0', u' ')
                    #html body is pretty clean, so include as well.
                    #TODO: select all copy inclues bunch of
                    lnkn_post['body_html'] = str(body)
                else:
                    lnkn_post['body'] = ''
                if shared_post:
                    lnkn_post['shared_post_text'] = shared_post.get_text()
                if shared_link:
                    lnkn_post['shared_link_text'] = shared_link.get_text()
                    lnkn_post['shared_link_href'] = shared_link['href']
                if days_ago:
                    lnkn_post['days_ago'] = days_ago.get_text().split(' ')[0]
                    lnkn_post['isEdited'] = 'Edited' in days_ago.get_text()
                    lnkn_post['shared_to_audience'] = days_ago.find('li-icon')['type']
                if reaction_cnt:
                    lnkn_post['reactions'] = reaction_cnt.get_text()
                else:
                    lnkn_post['reactions'] = 0
                if comment_cnt:
                    lnkn_post['comments'] = comment_cnt.get_text().split(' ')[0]
                else:
                    lnkn_post['comments'] = 0
                if repost_cnt:
                    lnkn_post['reposts'] = repost_cnt.get_text().split(' ')[0]
                else:
                    lnkn_post['reposts'] = 0
                if body not in self.lnkn_posts_set:
                    self.lnkn_posts.append(lnkn_post)
                    self.lnkn_posts_set.add(body)
            except Exception as e:
                print('excpetion while scraping linkedin posts' + str(e))
    #should be no dupes.. hopefully..
    def scrape_linkedin_emps(self, htm):
        soup = BeautifulSoup(htm)
        for emp_li in soup.findAll('li',{'class':'reusable-search__result-container'}):
            try:
                emp = {}
                name = emp_li.find('span', {'aria-hidden': 'true'})
                if name:
                    emp['name'] = name.get_text()
                else: #TODO refactor
                    emp['name'] = "LinkedIn Member"
                    emp['title'] = emp_li.find('div',{'class':'entity-result__primary-subtitle t-14 t-black t-normal'}).get_text()
                    emp['location'] = emp_li.find('div',{'class': 'entity-result__secondary-subtitle t-14 t-normal'}).get_text()
                    pic_url = emp_li.find('img', {'loading': 'lazy'})
                    if pic_url:
                        emp['pic_url'] = pic_url['src']
                    else:
                        emp['pic_url'] = ''
                    self.lnkn_emps.append(emp)
                    continue
                conn_degree = emp_li.find('span',{'class':'image-text-lockup__text entity-result__badge-text'}).find('span',{'aria-hidden':'true'}).get_text()
                if conn_degree:
                    emp['conn_degree'] = conn_degree.split(" ")[1]
                emp['title'] = emp_li.find('div',{'class':'entity-result__primary-subtitle t-14 t-black t-normal'}).get_text()
                pic_url = emp_li.find('img',{'loading':'lazy'})
                if pic_url:
                    emp['pic_url'] = pic_url['src']
                else:
                    emp['pic_url'] = ''
                emp['prof_url'] = emp_li.find('a',{'class':'app-aware-link'})['href']
                emp['isPremium'] = not emp_li.find('path',{'class':'background-mercado'}) == None
                emp['location'] = emp_li.find('div',{'class':'entity-result__secondary-subtitle t-14 t-normal'}).get_text()
                mutual_conns = emp_li.find('div',{'class':'entity-result__simple-insight-text-container'})
                if mutual_conns:
                    emp['mutual_conns'] = mutual_conns.get_text()
                else:
                    emp['mutual_conns'] = ''
                self.lnkn_emps.append(emp)
            except Exception as e:
                print('excpetion while scraping linkedin employees' + str(e))

class ytScraper:
    def __init__(self):
        self.yt_videos = []
        self.yt_title_set = set()
    def scrape_yt(self,htm):
        soup = BeautifulSoup(htm)
        for vid in soup.findAll('div',{'id':'content','class':'style-scope ytd-rich-item-renderer'}):
            try:
                yt = {}
                link = vid.find('a',{'id':'video-title-link'})
                title = vid.find('yt-formatted-string',{'id':'video-title'}).get_text() #link.get_text()
                views = vid.findAll('span',{'class':'inline-metadata-item style-scope ytd-video-meta-block'})[0].get_text()
                #if not yet premiered, views returns "Premieres 3/15/23, 6:00AM"
                if re.match(r'^Premieres .*',views):
                    days_ago = views
                    views = '0'
                else:
                    # TODO: convert this to abs date
                    days_ago = vid.findAll('span',{'class':'inline-metadata-item style-scope ytd-video-meta-block'})[1].get_text()
                yt['url'] = link['href']
                yt['title'] = title
                yt['views'] = views
                yt['days_ago'] = days_ago
                if title not in self.yt_title_set:
                    self.yt_videos.append(yt)
                    self.yt_title_set.add(title)
            except Exception as e:
                print('excpetion while scraping youtube' + str(e))
ctnt_lnks = set()
href_lnks = set()
def scrape_facebook_urls(htm):
    soup = BeautifulSoup(htm)
    #ctnt_lnks = set()
    #href_lnks = set()
    for link in soup.find_all('a', href=True):
        try:
            c = link.contents
            if c:
                content = str(c[0])
            href_link = link['href']
            if content and validators.url(content):
                ctnt_lnks.add(content)
            if not 'facebook.com' in href_link:
                href_lnks.add(href_link)
        except Exception as e:
            print('exception scraping fb urls'+str(e))
    #return ctnt_lnks,href_lnks
#used to determine redudnancy


