import discord
import requests
from bs4 import BeautifulSoup


embed_search = discord.Embed
async def create_embed(link, a, message):
    embed_search = discord.Embed(
        title = "Searching for: " + a,
        color = discord.Color.blue(),
    )
    embed_search.set_footer(text ="Please let me know if any bugs appear!")
    #get the name of the light novel and modify it for the link
    embed_search.add_field(
        name = "Direct link to search: ",
        value = link,
        inline = False,
    )
    scrape(link, embed_search)
    await message.channel.send(embed=embed_search)
    


def scrape(link, embed_search):
    URL = link #the URL to request
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id = "posts") #the id to find the needed data
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


client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


#aaaaaaaa i wish i could see the source code from some good bot it would make this so much easier
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('&help'):
        await message.channel.send('&find <light novel name>')
    if message.content.startswith('&find'):
        a = message.content #get the message
        link_text = a #for manipulation
        link_text = link_text[6:] #deleting &find 
        a = link_text
        link_text = link_text.replace(' ', '+') #replacing spaces for the link
        link = "https://jnovels.com/page/" #the default novel link
        page = "1/?s="
        link = link + page + link_text #make the integral link starting at page 1
        await create_embed(link, a, message) #awaitable coroutine so it works dont ask me why it needs to be like this
        await message.add_reaction("◀️") #adding reaction the message so the embed can be changed
        await message.add_reaction("▶️") #adding reaction the message so the embed can be changed



client.run('OTI0Mzg2ODAxNzMxMzcxMDM4.Ycd0Sw.6g-dAdj_ug1Drv4QAUDpe3Rw6ek')