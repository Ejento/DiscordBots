#! /usr/bin/python3
# moviebot.py - Searching and pulling movies from IMDB (made by TichuMaster)

import discord, requests, bs4, logging, asyncio, os, datetime
logging.basicConfig(level = logging.INFO, format = "%(asctime)s - %(levelname)s - %(message)s")


os.chdir("/home/akumu/Documents/myProj")
client = discord.Client() # create the clien
# The helpText for the command !exp
helpText = """Usage: **!command <title/name>**.\n`!movie <title>`: It returns a IMDB link with the movie you searched.
`!more <title>`: It returns three (3) IMDB movies for more variant.
`!actor <name>`: It returns the profile of the actor / actress that you searched.
`!scene`: It returns this text."""

# We need to extract the name after the command and create the IMDB url
def getUrl(message):
    mes = message.content.split(" ")
    movieTitle = " ".join(mes[1:])
    tempUrl = "http://www.imdb.com/find?ref_=nv_sr_fn&q=%s&s=tt" % (movieTitle)
    logging.info(tempUrl)
    return tempUrl

# We are getting all the ellements from the HTML and we are searching for what we need
def getElements(site):
    res = requests.get(site)
    res.raise_for_status() # Checking for errors
    soup = bs4.BeautifulSoup(res.text, "lxml")
    elements = soup.select('.findResult a') # css class = findResult attribute = a
    logging.info(len(elements))
    return elements

# Logging the commands that have been used
def writeToFile(text):
    if not os.path.isfile("commands.txt"):
        comFile = open("commands.txt", "w") # if the file doesn't exist, we have to create it
        comFile.write(text + "\n")
        comFile.close()
    else:
        comFile = open("commands.txt", "a") # if the file exists, we append the new content
        comFile.write(text + "\n")
        comFile.close()

# Standar procedure for login
@client.event
async def on_ready():
    print('Logged in as:')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith("!movie"): # We are checking the start of the message
        url = getUrl(message) # we are getting the url
        elem = getElements(url) # we are getting the elements that we need
        suggestedMovie = "http://www.imdb.com" + elem[1].get('href') # we need the first result so we are using elem[1] (the seccond element)
        await client.send_message(message.channel, suggestedMovie) # sending the message
    elif message.content.startswith("!more"):
        suggestedFilms = [] # a temporary list so we can store the suggestions
        url = getUrl(message)
        elem = getElements(url)
        for i in range(1, 6, 2):
            suggestedFilms.append("http://www.imdb.com" + elem[i].get('href'))
        logging.info(suggestedFilms)
        # Create the message with the 3 suggestions
        await client.send_message(message.channel, "*" + str(message.author) + "*" + ", I have 3 suggestions for you :\n")
        for url in suggestedFilms:
            await client.send_message(message.channel, url)
        del(suggestedFilms)
    elif message.content.startswith("!actor"):
        mes = message.content.split(" ")
        actorName = " ".join(mes[1:])
        url = "http://www.imdb.com/find?ref_=nv_sr_fn&q=%s&s=nm" % (actorName)
        elem = getElements(url)
        if elem == []:
            await client.send_message(message.channel, "Sorry didn't found that! :lirikS:")
        else:
            suggestedActor = "http://www.imdb.com" + elem[1].get('href')
            await client.send_message(message.channel, suggestedActor)
    elif message.content.startswith("!scene"):
        await client.send_message(message.channel, helpText)

    if message.content.startswith("!"):
        command = str(message.author) + " - " + str(message.content) + " - " + str(message.channel) + " - " + str(message.timestamp)
        writeToFile(command)
    
# Starting the client / bot
client.run("MzU4MzQyNDE0Njg5MTA3OTY4.DJ3D6Q.rcFIyA8zP06RxuHANqkgVY-Iou0")
