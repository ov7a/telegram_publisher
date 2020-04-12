#!/usr/bin/env python3
import os
import sys
from telethon.sync import TelegramClient
import socks
import frontmatter
from datetime import datetime

content_path = sys.argv[1]

UTC_HOUR = 7
date_parts = list(map(int, os.path.basename(content_path).split('-')[0:3]))
post_date = datetime(year=date_parts[0], month=date_parts[1], day=date_parts[2], hour=UTC_HOUR, second=1)

post = frontmatter.load(content_path)
updated_content = "\n\n".join(filter(None, [
	", ".join(map(lambda tag: "#" + tag, post['tags'])) if 'tags' in post else None,
	post.get('title'),
	post.content
]))

def get_env(name, message, cast=str):
	if name in os.environ:
		return os.environ[name]
	while True:
		value = input(message)
		try:
			return cast(value)
		except ValueError as e:
			print(e, file=sys.stderr)
			time.sleep(1)

session = os.environ.get('TG_SESSION', 'publisher')
api_id = get_env('TG_API_ID', 'Enter your API ID: ', int)
api_hash = get_env('TG_API_HASH', 'Enter your API hash: ')

channel_name='minutkaprosvescheniya' 

proxy = (socks.SOCKS5, 'localhost', 9050) 
	
with TelegramClient(session, api_id, api_hash, proxy=proxy) as client:
	client.send_message(channel_name, updated_content, parse_mode='md', schedule=post_date)


	
