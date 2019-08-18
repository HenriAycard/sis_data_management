#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 13:10:07 2019

@author: henriaycard
"""

import urllib3
import json
import datetime
import csv
import time

def unicode_normalize(text):
    return text.translate({ 0x2018:0x27, 0x2019:0x27, 0x201C:0x22, 0x201D:0x22, 0xa0:0x20 }).encode('utf-8')

def request_data_from_url(url):
    #lecture url
    #req = urllib3.request.RequestMethods(url)
    success = False
    while success is False:
        http = urllib3.PoolManager()
        response = http.request('GET', url)
        True



    #return the contents of the response
    return response.data

def get_facebook_page_data(page_id, access_token):

    website = "https://graph.facebook.com/v4.0/"
    
    location = "%s/posts/" % page_id 
    
    fields = "?message%2Ccreated_time%2Ctype%2Cname%2Cid%2Ccomments.limit(0).summary(true)%2Cshares%2Creactions.limit(0).summary(true)"
      
    authentication = "&access_token=%s" % (access_token)
    
    request_url = website + location + fields + authentication
#    request_url2 = "https://graph.facebook.com/v4.0/StartinSaclay/posts/?message%2Ccreated_time%2Ctype%2Cname%2Cid%2Ccomments.limit(0).summary(true)%2Cshares%2Creactions.limit(0).summary(true)&access_token=EAAHdlWmZAsDUBAPfwiXSrdRD2Kj3PlAIZAcVnKHrtB9konTieHj9fGkZB7bn99FqlIk87fjSTpSKLrTOcizjCJknKe4OfdUgrbUkRXBybavhb7DdgtuWUvsZA9VxgDKVotXjGYwUhsh8yGDUpoNZA5TWtoY1PsPeymvxlJPHvxVIPaELYKGImZC6Y8REY41Q8ZBNAKJ1fhfhQZDZD"

    data = json.loads(request_data_from_url(request_url))
    return data

def process_post(post, access_token):

    post_id = post['id']
    
    post_message = '' if 'message' not in post.keys() else \
            unicode_normalize(post['message'])
        
    #post_type = post['type']
    post_published = datetime.datetime.strptime(
            post['created_time'],'%Y-%m-%dT%H:%M:%S+0000')
    post_published = post_published + \
            datetime.timedelta(hours=-2)
    post_published = post_published.strftime(
            '%Y-%m-%d %H:%M:%S')

    num_reactions = 0 if 'reactions' not in post else \
            post['reactions']['summary']['total_count']
    num_comments = 0 if 'comments' not in post else \
            post['comments']['summary']['total_count']
    num_shares = 0 if 'shares' not in post else post['shares']['count']

    reactions = get_reactions_for_post(post_id, access_token) if \
            post_published > '2016-02-24 00:00:00' else {}

    num_likes = 0 if 'like' not in reactions else \
            reactions['like']['summary']['total_count']

    num_likes = num_reactions if post_published < '2016-02-24 00:00:00' \
            else num_likes

    def get_num_total_reactions(reaction_type, reactions):
        if reaction_type not in reactions:
            return 0
        else:
            return reactions[reaction_type]['summary']['total_count']

    num_loves = get_num_total_reactions('love', reactions)
    num_wows = get_num_total_reactions('wow', reactions)
    num_hahas = get_num_total_reactions('haha', reactions)
    num_sads = get_num_total_reactions('sad', reactions)
    num_angrys = get_num_total_reactions('angry', reactions)

    return (post_id, post_message,
            post_published, num_reactions, num_comments, num_shares,
            num_likes, num_loves, num_wows, num_hahas, num_sads, num_angrys)
    
def get_reactions_for_post(post_id, access_token):

    website = "https://graph.facebook.com/v2.6"
    
    location = "/%s" % post_id
    
    reactions = "/?fields=" \
            "reactions.type(LIKE).limit(0).summary(total_count).as(like)" \
            ",reactions.type(LOVE).limit(0).summary(total_count).as(love)" \
            ",reactions.type(WOW).limit(0).summary(total_count).as(wow)" \
            ",reactions.type(HAHA).limit(0).summary(total_count).as(haha)" \
            ",reactions.type(SAD).limit(0).summary(total_count).as(sad)" \
            ",reactions.type(ANGRY).limit(0).summary(total_count).as(angry)"
    
    authentication = "&access_token=%s" % access_token
    
    request_url = website + location + reactions + authentication

    data = json.loads(request_data_from_url(request_url))
     
    return data

def scrape_facebook_page(page_id, access_token):
    with open('%s_facebook_posts.csv' % page_id, 'w') as file:
        w = csv.writer(file)
        
        w.writerow(["post_id", "post_message", "post_published", "num_reactions", "num_comments", "num_shares", "num_likes", "num_loves", "num_wows", "num_hahas", "num_sads", "num_angrys"])

        has_next_page = True
        num_processed = 0  
        scrape_starttime = datetime.datetime.now()

        print("Scraping %s Facebook Page: %s\n" % (page_id, scrape_starttime))

        posts = get_facebook_page_data(page_id, access_token)

        while has_next_page:
            if num_processed == 200:
                break
                
            for post in posts['data']:

                w.writerow(process_post(post, access_token))
                    
                num_processed += 1

            if 'paging' in posts.keys():
                posts = json.loads(request_data_from_url(
                                        posts['paging']['next']))
            else:
                has_next_page = False


        print("Completed!\n%s posts Processed in %s" % \
                (num_processed, datetime.datetime.now() - scrape_starttime))