#!/usr/bin/env python3
import os
import sys
from pyrogram import Client
import frontmatter
import re
from datetime import datetime, timezone
import keyring
import time

content_path = sys.argv[1]

UTC_HOUR = 7
date_parts = list(map(int, os.path.basename(content_path).split('-')[0:3]))
post_date = datetime(year=date_parts[0], month=date_parts[1], day=date_parts[2], hour=UTC_HOUR-1, minute=59, second=1, tzinfo=timezone.utc)

def process_content(content):
	content = re.sub("!\[.*?\]\(.*?\)\n*", "", content)
	content = re.sub(r"\[([^`]*)`([^\]]*)`([^`]*)\]", r"[\1\2\3]", content)
	content = re.sub(r"<kbd>(.*?)</kbd>", r"`\1`", content)
	content = re.sub(r"\[(.*?)\]\((/.*?)\)", r"[\1](https://ov7a.github.io\2)", content)
	return content

post = frontmatter.load(content_path)
updated_content = "\n\n".join(filter(None, [
	", ".join(map(lambda tag: "#" + tag, post['tags'])) if 'tags' in post else None,
	post.get('title'),
	process_content(post.content)
]))

def get_api_info(name, message, cast=str):
	if name in os.environ:
		return os.environ[name]

	keyring_value = keyring.get_password("tg_api", name)
	if keyring_value:
		return keyring_value

	while True:
		value = input(message)
		try:
			return cast(value)
		except ValueError as e:
			print(e, file=sys.stderr)
			time.sleep(1)

api_id = get_api_info('TG_API_ID', 'Enter your API ID: ', int)
api_hash = get_api_info('TG_API_HASH', 'Enter your API hash: ')

channel_name='minutkaprosvescheniya'

client = Client("publisher", api_id, api_hash, no_updates=True)

async def main():
	async with client:	
		await client.send_message(channel_name, updated_content, schedule_date=post_date)
		
client.run(main())

