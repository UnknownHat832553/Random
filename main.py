import nextcord
import aiohttp
import os
from nextcord.ext import commands
from flask import Flask
from threading import Thread

from server import server_on

bot = commands.Bot(
    command_prefix='!',
    intents=nextcord.Intents.all(),
    help_command=None
)

class GenView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @nextcord.ui.button(label='รูป 18+', style=nextcord.ButtonStyle.red)
    async def send_nsfw(self, button: nextcord.Button, interaction: nextcord.Interaction):
        await self.send_image(interaction, 'https://api.waifu.pics/nsfw/waifu', 'รูป 18+')

    @nextcord.ui.button(label='รูปอนิเมะ', style=nextcord.ButtonStyle.green)
    async def send_anime(self, button: nextcord.Button, interaction: nextcord.Interaction):
        await self.send_image(interaction, 'https://api.waifu.pics/sfw/waifu', 'รูปอนิเมะ')

    @nextcord.ui.button(label='รูปวิวสวยๆ', style=nextcord.ButtonStyle.blurple)
    async def send_nature(self, button: nextcord.Button, interaction: nextcord.Interaction):
        await self.send_image(interaction, 'https://api.unsplash.com/photos/random?query=nature&client_id=o5oYYw0hk_WZCDPVO9A_3qAwt08aESiQRvcX2LqOXu0', 'รูปวิวธรรมชาติ')

    @nextcord.ui.button(label='รูปอาหาร', style=nextcord.ButtonStyle.gray)
    async def send_food_button(self, button: nextcord.Button, interaction: nextcord.Interaction):
        await self.send_food(interaction)

    @nextcord.ui.button(label='รูปผี/ลึกลับ', style=nextcord.ButtonStyle.secondary)
    async def send_ghost(self, button: nextcord.Button, interaction: nextcord.Interaction):
        await self.send_image(interaction, 'https://api.unsplash.com/photos/random?query=ghost,horror&client_id=o5oYYw0hk_WZCDPVO9A_3qAwt08aESiQRvcX2LqOXu0', 'รูปผี/ลึกลับ')

    async def send_image(self, interaction, url, tag):
        msg = await interaction.response.send_message(f'## > [+] กำลังโหลด {tag}...', ephemeral=True)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        image_url = data['url'] if 'url' in data else data.get('urls', {}).get('regular', '❌ ไม่พบรูปภาพ')
                        await msg.edit(content=f'{tag}: {image_url}')
                    else:
                        await msg.edit(content='❌ โหลดรูปภาพไม่สำเร็จ')
        except Exception as e:
            await msg.edit(content=f'เกิดข้อผิดพลาด: {str(e)}')

    async def send_food(self, interaction):
        msg = await interaction.response.send_message(f'## > [+] กำลังหาของกินให้...', ephemeral=True)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://foodish-api.com/api/') as response:
                    data = await response.json()
                    food_url = data['image']
                    await msg.edit(content=f'รูปอาหาร:\n{food_url}')
        except Exception as e:
            await msg.edit(content=f'เกิดข้อผิดพลาด: {str(e)}')

@bot.event
async def on_ready():
    bot.add_view(GenView())
    await bot.change_presence(activity=nextcord.Game(name="สุ่มรูปต่างๆ"))

@bot.command(name="random")
async def random(ctx):
    embed = nextcord.Embed(
        title='เลือกปุ่มเพื่อสุ่มรูปภาพที่คุณชอบ 💖',
        description='มีทั้งรูป 18+, รูปอนิเมะ, วิวสวยๆ และของกิน',
        color=0xf06292
    )
    embed.set_image(url='https://c.tenor.com/JbnLKar05tAAAAAC/tenor.gif')
    await ctx.send(embed=embed, view=GenView())

    try:
        await ctx.message.delete()
    except:
        pass

server_on()
bot.run(os.getenv('TOKEN'))
