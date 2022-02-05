#!/usr/bin/env python3
import os
import sys
from telethon.sync import TelegramClient
import socks
import frontmatter
import re
from datetime import datetime
import keyring

content_path = sys.argv[1]
file_path = sys.argv[2] if len(sys.argv) > 2 else None

UTC_HOUR = 7
date_parts = list(map(int, os.path.basename(content_path).split('-')[0:3]))
post_date = datetime(year=date_parts[0], month=date_parts[1], day=date_parts[2], hour=UTC_HOUR, second=1)

def process_content(content):
	content = re.sub("!\[.*?\]\(.*?\)\n*", "", content)
	content = re.sub("```[a-z]+", "```", content)
	content = re.sub(r"<kbd>(.*?)</kbd>", r"`\1`", content)
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

session = os.environ.get('TG_SESSION', 'publisher')
api_id = get_api_info('TG_API_ID', 'Enter your API ID: ', int)
api_hash = get_api_info('TG_API_HASH', 'Enter your API hash: ')

channel_name='minutkaprosvescheniya'

with TelegramClient(session, api_id, api_hash) as client:
	client.send_message(channel_name, updated_content, parse_mode='md', schedule=post_date, file=file_path)

