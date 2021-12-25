import discord

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


#aaaaaaaa i wish i could see the source code from some good bot
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('&help'):
        await message.channel.send('&find <light novel name>')
    if message.content.startswith('&find'):
        a = message.content
        a = a[6:]
        a = a.replace(' ', '+')
        print(a)
        link = "https://jnovels.com/page/2/?s="
        link = link + a
        print(link)


client.run('OTI0Mzg2ODAxNzMxMzcxMDM4.Ycd0Sw.6g-dAdj_ug1Drv4QAUDpe3Rw6ek')
