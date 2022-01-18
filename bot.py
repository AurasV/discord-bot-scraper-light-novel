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


async def create_embed(link, a, message): #create the first embed
    global embed_search
    global page_nr
    embed_search = discord.Embed( #create the embed
        title = "Searching for: " + a,
        color = discord.Color.blue(),
    )
    embed_search.set_footer(text ="Please let me know if any bugs appear!") #add footer
    embed_search.add_field( #add field
        name = "Page Number",
        value = page_nr,
        inline = False
    )
    embed_search.add_field( #add field
        name = "Direct link to search: ",
        value = link,
        inline = False,
    )
    scrape(link, embed_search) #scrape the site for the links and text needed
    if Nothing_found == True: #if the page doesnt have what i need
        await message.channel.send("Nothing found")
    else:
        await message.channel.send(embed=embed_search) #if it does have what i need
    

def scrape(link, embed_search): #scrape the site
    global Nothing_found
    Nothing_found = False #reset the nothing found flag
    URL = link #the URL to request
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser") #parse the html
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
            embed_search.add_field( #add the field with the search link
                name = nume,
                value = link,
                inline = False,
            )
    except AttributeError: #AttributeError takes place when there's no page
        Nothing_found = True

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client)) #more for debugging than anything


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
    if message.content.startswith('&help'): #help message
        await message.channel.send('&find <light novel name>') #message to send
    if message.content.startswith('&find'): #if message starts with find
        global reaction 
        reaction = 0 #reset number of reaction
        global page_nr
        page_nr = 1 #reset page number for the embed
        await search(message) #search the link


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
            await message.channel.send("Nothing found...") #AttributeError takes place when there's no page


@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent): #when a reaction is added
    global reaction
    reaction += 1 #count the number of reactions if its more than 2 it means its not the bot that reacted and i realized i can do it better but meh
    message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id) #get the message sent
    if reaction >= 3: #if the number of reactions is above 2 change the embed
        message_time = int(round(message.created_at.timestamp())) #get the time of the message
        request_time = int(datetime.now().timestamp()) #get the time of the reaction
        if (message_time + 7500 > request_time): #after some time you cant use the same embed
            if (str(payload.emoji) == '◀️' ): #if the reaction is left
                await edit_left(message)
            elif (str(payload.emoji) == '▶️' ): #if the reaction is right
                await edit_right(message)
        else:
            return


async def edit_left(message): #if the reaction is left
    global embed_search
    global page_nr
    page_nr = int(message.embeds[0].fields[0].value) #get the page number from the embed
    if page_nr == 1:
        await message.channel.send("Can't go below 1st page!") #cant go below 1 duh
    else:
        page_nr = page_nr - 1 #change the number if above 1
    text = message.embeds[0].title #get the search term
    text_link = message.embeds[0].title[15:].replace(" ","-") #to create the link space becomes -
    link = "https://jnovels.com/page/" + str(page_nr) + "/?s=" + text_link #make the link at the needed page
    new_search = discord.Embed( #create the new embed
        title = text,
        color = discord.Color.blue(),
    )
    new_search.set_footer(text ="Please let me know if any bugs appear!") #set the footer of the new embed
    new_search.add_field( #add field
        name = "Page Number: ",
        value = page_nr,
        inline = False,
    )
    new_search.add_field( #add field
        name = "Direct link to search: ",
        value = link,
        inline = False,
    )
    embed_search = new_search #replace the embed with the new one
    scrape(link, embed_search) #do the scraping using the data from the new embed
    if Nothing_found == True:
        await message.channel.send("No more pages") #if there's no more pages now that i think about it this might cause a bug overall ¯\_(ツ)_/¯
    else:
        await message.edit(embed = embed_search) #edit the discord message so it shows the new embed


async def edit_right(message): #if the reaction is right
    global embed_search
    page_nr = int(message.embeds[0].fields[0].value) #get the page number from the embed
    page_nr = page_nr + 1
    text = message.embeds[0].title #get the title from the embed
    text_link = message.embeds[0].title[15:].replace(" ","-") #to create the link
    link = "https://jnovels.com/page/" + str(page_nr) + "/?s=" + text_link #make the new link
    new_search = discord.Embed( #create the new embed
        title = text,
        color = discord.Color.blue(),
    )
    new_search.add_field( #add field
        name = "Page Number: ",
        value = page_nr,
        inline = False,
    )
    new_search.set_footer(text ="Please let me know if any bugs appear!") #remove footer
    new_search.add_field( #add field
        name = "Direct link to search: ",
        value = link,
        inline = False,
    )
    embed_search = new_search #replace the old embed
    scrape(link, embed_search)
    if Nothing_found == True:
        await message.channel.send("No more pages") #send a message in the channel
        print(message.embeds[0].fields[0].value) #this is for debugging
        message.embeds[0].fields[0].value = str(int(message.embeds[0].fields[0].value) - 1) #get the page back to the original number so if you're on page 2 but there's no page 3 it goes back to page 2
    else:
        await message.edit(embed = embed_search) #if there is a link and there's actual LNs in there change the embed


#◀️
#▶️
