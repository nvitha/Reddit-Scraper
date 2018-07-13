'''Fetches the usernames of people who have commented in a specific subreddit for the past user-defined 
number of comments. Assumes a sqlite database named "usernames.db" in the same directory 
with a table named "usernames" with a single column with type text'''

import requests
import pprint
import sqlite3
import math
from time import sleep

conn = sqlite3.connect('usernames.db') 
cur = conn.cursor()

# define the subreddit here
subreddit = 'news'
comments_to_get = 1000 #at minimum, will grab 500 unless you set at 0

comment_gets = int(math.ceil(float(comments_to_get)/500.00))

for i in range(comment_gets): #since the pushshift api only supports returning 500 comments at a time
	if i == 0: #build the request URL
		request_string = 'https://api.pushshift.io/reddit/search/comment/?subreddit=' + subreddit + '&size=500'
	else:
		request_string = 'https://api.pushshift.io/reddit/search/comment/?subreddit=mademesmile&size=500&before=' + str(last_time)
		print(last_time) # prints the epoch time of the when the last comment fetched was submitted to reddit

	response = requests.get(request_string) #request the URL
	response_json = response.json()['data'] #parse the json
	last_time = response_json[-1]['created_utc'] #nab the time of the last item for use to grab 500 more comments

	# to execute many commands, create a list of tuples to add to the table
	name_list = []
	for item in response_json:
		tuple = (item['author']),
		name_list.append(tuple)

	cur.executemany('INSERT OR IGNORE INTO usernames VALUES (?)', name_list) # insert the list into the database
	conn.commit() #commit the database to storage just in case the computer crashes.
	# slower than committing after the loop, but allows stopping the script without loss of data
	# sleep(5)

conn.close() # close the connection to the database so that we don't hog resources
