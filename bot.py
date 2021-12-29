import discord
import requests
from bs4 import BeautifulSoup
from datetime import datetime
reaction = 0
date_time = datetime.now()
global embed_search 
embed_search = discord.Embed
global page_nr
page_nr = int


async def create_embed(link, a, message):
    global embed_search
    global page_nr
    embed_search = discord.Embed(
        title = "Searching for: " + a,
        color = discord.Color.blue(),
    )
    embed_search.set_footer(text ="Please let me know if any bugs appear!")
    #get the name of the light novel and modify it for the link
    embed_search.add_field(
        name = "Page Number",
        value = page_nr,
        inline = False
    )
    embed_search.add_field(
        name = "Direct link to search: ",
        value = link,
        inline = False,
    )
    scrape(link, embed_search)
    if Nothing_found == True:
        await message.channel.send("Nothing found")
    else:
        await message.channel.send(embed=embed_search)
    

def scrape(link, embed_search):
    global Nothing_found
    Nothing_found = False
    URL = link #the URL to request
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id = "posts") #the id to find the needed data
    try:
        job_elements = results.find_all("h1", class_ = "post-title entry-title" ) #more accurate data retrieval
        for job_element in job_elements:
            name = job_element.find("a", rel = "bookmark") #data retrieval
            title = name.text #get the light novel name so it can be manipulated
            nume = name.text #get the light novel name so it can be used in the embed
            title = title.replace("–","") #weird character used in the site :/
            title = title.replace(" ","-") #to create the link
            title = title.replace(" ","-") #another weird character used in the site :/ (ALT + 255)
            title = title.replace("[","") #to create the link
            title = title.replace("]","") #to create the link
            link = "https://jnovels.com/" #default light novel link
            link = link + title #get the final light novel link
            embed_search.add_field(
                name = nume,
                value = link,
                inline = False,
            )
    except AttributeError:
        Nothing_found = True


client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


#aaaaaaaa i wish i could see the source code from some good bot it would make this so much easier
@client.event
async def on_message(message):
    if message.author == client.user:
        try:
            if message.embeds[0] != None:
                await message.add_reaction("◀️") #adding reaction the message so the embed can be changed
                await message.add_reaction("▶️") #adding reaction the message so the embed can be changed
        except IndexError:
            return
    if message.content.startswith('&help'):
        await message.channel.send('&find <light novel name>')
    if message.content.startswith('&find'):
        global reaction
        reaction = 0
        global page_nr
        page_nr = 1
        await search(message)


async def search(message):
    try:
        a = message.content #get the message
        link_text = a #for manipulation
        link_text = link_text[6:] #deleting &find 
        a = link_text
        link_text = link_text.replace(' ', '+') #replacing spaces for the link
        link = "https://jnovels.com/page/1/?s=" #the default novel link
        link = link + link_text #make the integral link starting at page 1
        await create_embed(link, a, message) #awaitable coroutine so it works dont ask me why it needs to be like this
    except AttributeError:
            await message.channel.send("Nothing found...")


@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    global reaction
    reaction += 1 #count the number of reactions
    message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
    if reaction >=3: #if the number of reactions is above 2 change the embed
        message_time = int(round(message.created_at.timestamp()))
        request_time = int(datetime.now().timestamp())
        if (message_time + 7500 > request_time):
            if (str(payload.emoji) == '◀️' ):
                await edit_left(message)
            elif (str(payload.emoji) == '▶️' ):
                await edit_right(message)
        else:
            return


async def edit_left(message):
    global embed_search
    global page_nr
    page_nr = int(message.embeds[0].fields[0].value)
    if page_nr == 1:
        await message.channel.send("Can't go below 1st page!")
    else:
        page_nr = page_nr - 1
    text = message.embeds[0].title
    text_link = message.embeds[0].title[15:].replace(" ","-") #to create the link
    link = "https://jnovels.com/page/" + str(page_nr) + "/?s=" + text_link
    new_search = discord.Embed(
        title = text,
        color = discord.Color.blue(),
    )
    new_search.set_footer(text ="Please let me know if any bugs appear!")
    #get the name of the light novel and modify it for the link
    new_search.add_field(
        name = "Page Number: ",
        value = page_nr,
        inline = False,
    )
    new_search.add_field(
        name = "Direct link to search: ",
        value = link,
        inline = False,
    )
    embed_search = new_search
    scrape(link, embed_search)
    if Nothing_found == True:
        await message.channel.send("No more pages")
    else:
        await message.edit(embed = embed_search)


async def edit_right(message):
    global embed_search
    page_nr = int(message.embeds[0].fields[0].value)
    page_nr = page_nr + 1
    text = message.embeds[0].title
    text_link = message.embeds[0].title[15:].replace(" ","-") #to create the link
    link = "https://jnovels.com/page/" + str(page_nr) + "/?s=" + text_link
    new_search = discord.Embed(
        title = text,
        color = discord.Color.blue(),
    )
    new_search.add_field(
        name = "Page Number: ",
        value = page_nr,
        inline = False,
    )
    new_search.set_footer(text ="Please let me know if any bugs appear!")
    new_search.add_field(
        name = "Direct link to search: ",
        value = link,
        inline = False,
    )
    embed_search = new_search
    scrape(link, embed_search)
    if Nothing_found == True:
        await message.channel.send("No more pages")
        print(message.embeds[0].fields[0].value)
        message.embeds[0].fields[0].value = str(int(message.embeds[0].fields[0].value) - 1)
    else:
        await message.edit(embed = embed_search)


#◀️
#▶️


client.run('OTI0Mzg2ODAxNzMxMzcxMDM4.Ycd0Sw.6g-dAdj_ug1Drv4QAUDpe3Rw6ek')