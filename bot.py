import os
import random
import discord
import requests
from bs4 import BeautifulSoup

client = discord.Client()

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}



@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))



async def download_video(msg, link = None):
	#the link to the tiktok to download
	#link is empty if the link wasn't parsed from multiple words
	if link == None:
		link = msg.content

	#raw data from requests
	r = requests.get(link, headers=headers, allow_redirects=True)
	
	#parsed data thats searchable
	data = BeautifulSoup(r.text, 'html.parser')

	#tiktok only has one video tag on the page on the web version when going to the link of a video
	##used findAll to check if there is more so signify it's some different page or the front page which has none
	vid = data.findAll('video')
	#basically just making sure it's not on a non-video page
	if len(vid) == 1:
		#a random name for the file
		name = str(random.random()*20000) + '.mp4'
		#the video from the source video tag
		file_link = vid[0]['src']

		
		file = requests.get(file_link, allow_redirects=True)
		
		print('file is: ', type(file))

		#writes to random name file
		open(name, 'wb').write(file.content)
		#async sends file to server
		try:
			#tried to use file itself but it gave issues, saving and sending the file just works
			await msg.channel.send(file=discord.File(name, name))
		except Exception as err:
			print('lol couldn\'t send: ' + str(err))
			msg.channel.send()
		#>delet this
		os.remove(name)
	else:
		print('issues finding a video: ' + link)

#the jemu clause
async def download_discord_video(msg, link):
	channel = msg.channel

	#i feel like this is botched but it's 5am and i just want to focus on this for a second
	extension = '.mp4' if '.mp4' in link else '.webm'

	tmp_name = str(random.random()*200) + '.mp4'



	file = requests.get(link)

	open(name, 'wb').write(file.content)


	try:
			#tried to use file itself but it gave issues, saving and sending the file just works
		await msg.channel.send(file=discord.File(name, name))
	except Exception as err:
		print('lol couldn\'t send: ' + str(err))
		msg.channel.send('files to big probably')
	#>delet this
	os.remove(name)


@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith('$hello'):
		await message.channel.send('Hello!')

	if 'cdn.discordapp.com' in message.content:
		if '.mp4' in message.content or '.webm' in message.content:
			
			for m in message.content.split(' '):
				if '.mp4' in m or '.webm' in m:
					await download_discord_video(message, m)

	elif 'tiktok.com' in message.content:
		#checking if there's other text besides tiktok
		if len(message.content.split(' ')) > 1:
			#m for section that might contain the link, should've named it better
			for m in message.content.split(' '):
				if 'tiktok.com' in m:
					await download_video(message, m)
		else:
			await download_video(message)

key = os.environ.get('discord_token')
client.run(key)




#var name on heroku discord_token