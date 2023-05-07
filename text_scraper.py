'''
scraper based on text (ie from select all and copy on a website). Not as good as html, but more adapatble and less impacted by change
'''
import re
fb_posts={}
fi = 0
ti = 0
tweets = {}
tweet_filter_set = {'·'}
def clear():
    global fb_posts,tweets,fi,ti
    fb_posts = {}
    fi = 0
    ti = 0
    tweets = {}
def scrape_tweets(txt,acc_name=''):
    global ti
    # startPostReg = r"\d\w{,7}•"
    # â€¢ instead of • in html
    startPostReg = r" .{,20}Retweeted$"
    endPostReg = r"^Feed post$|^Affiliated pages$|^You might like$"
    post = ''
    post_i = 0
    inPost = False
    for line,nxt_line in txt.splitlines():
        # TODO: tighten this
        if re.match(startPostReg, line):
            inPost = True
        elif inPost and (re.match(endPostReg, line) or (line[0] == '@' and line[1:]==acc_name)):
            inPost = False
            if not (post in posts):
                posts[i] = post.rstrip('\n')
                i += 1
            post = ''
        if inPost and not (line in tweet_filter_set):
            post += line + '\n'
    return posts

def scrape_fb_company_posts(txt):
    global fi
    #startPostReg = r"\d\w{,7}•"
    # â€¢ instead of • in html
    #startPostReg = r"^  ·$"
    startPostReg = r"^[\w ].{,40}· ?$"
    endPostReg = startPostReg #r"[\d:]* \/ [\d:]*"
    seeMorePost = r"See more$"
    spaces = 0
    post = ''
    post_i = 0
    inPost = False
    for line in txt.splitlines():
        #skip See More
        #if re.match(seeMorePost,line):
        #    post = ''
        #   inPost = False
        #    break
        # TODO: tighten this
        if re.match(startPostReg,line) and not inPost:
            inPost = True
        elif inPost and re.match(endPostReg,line): #spaces == 2:

            inPost = False
            if not (post in posts):
                fb_posts[fi] = post.rstrip('\n')
                fi += 1
            post = ''
        if inPost and not (line in filter_set):
            post += line + '\n'
    return fb_posts


filter_set = {'Your document has finished loading'
              'Your document is loading'}
posts={}

'''
 <span class="break-words">
      <span dir="ltr">
      
'''
i = 0
def scrape_linkedin_posts(txt):
    global i
    #startPostReg = r"\d\w{,7}•"
    # â€¢ instead of • in html
    startPostReg = r" \d.{,15}ago"
    endPostReg = r"^Feed post$|^Affiliated pages$|^Loading more results$"
    post = ''
    post_i = 0
    inPost = False
    for line in txt.splitlines():
        # TODO: tighten this
        if re.match(startPostReg,line):
            inPost = True
        elif inPost and re.match(endPostReg,line):
            inPost = False
            if not (post in posts):
                posts[i] = post.rstrip('\n')
                i += 1
            post = ''
        if inPost and not (line in filter_set):
            post += line + '\n'
    return posts

