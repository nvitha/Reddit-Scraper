'''Fetches the usernames of people who have commented in a specific subreddit for the past user-defined 
number of comments. '''

import requests
import pprint
import sqlite3

import math
from time import sleep


failed = False
try:
	conn = sqlite3.connect('comments.db')
except error as e:
	failed = True
	print(e)
finally:
	conn.close() 
	if failed:
		quit()
conn = sqlite3.connect('comments.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS comments (subreddit text, author text, permalink text, body text, timestamp text);')


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
		tuple = (subreddit,item['author'],item['permalink'],item['body'],item['created_utc'])
		#print(tuple)
		name_list.append(tuple)

	cur.executemany('INSERT OR IGNORE INTO comments VALUES (?,?,?,?,?)', name_list) # insert the list into the database
	conn.commit() #commit the database to storage just in case the computer crashes.
	# slower than committing after the loop, but allows stopping the script without loss of data
	# sleep(5)

conn.close() # close the connection to the database so that we don't hog resources
