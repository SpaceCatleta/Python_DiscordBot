import discord
from botParsers.vk.data.VKPost import VKPost


def vk_post_to_embed(data: VKPost) -> discord.Embed:
    embed: discord.Embed = discord.Embed(color=0x206694, description=data.text)
    embed.set_author(name=data.authorName, url=data.authorHref, icon_url=data.authorImageUrl)
    if len(data.media) > 0:
        embed.set_image(url=data.media[0])
    embed.set_footer(text='vk.com')
    return embed
