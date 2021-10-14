from datetime import datetime

from httpx import AsyncClient
import discord
from discord.ext import commands, vbu
from discord.ext.commands.cooldowns import BucketType

from cogs.utils import respond


class Weather(vbu.Cog):
    @staticmethod
    def error_embed(status_code: int, request_url: str):
        timestamp = datetime.utcnow()
        embed = discord.Embed(
            title="Oops...",
            description="An error occurred while fetching weather information.",
            color=discord.Color.red(),
            timestamp=timestamp,
        )
        embed.add_field(name="Status Code", value=str(status_code))
        embed.add_field(name="Request URL", value=request_url.replace(" ", "%20"))
        embed.set_author(
            name="MetaWeather",
            url="https://www.metaweather.com",
            icon_url="https://www.metaweather.com/static/img/weather/png/lc.png",
        )
        return embed

    @commands.command()
    @commands.cooldown(1, 30, BucketType.user)
    async def weather(self, ctx: vbu.Context, location: str):
        await ctx.defer()
        client = AsyncClient()
        search_url = f"https://www.metaweather.com/api/location/search/?query={location}"
        search_response = await client.get(url=search_url)
        if search_response.status_code != 200 or not search_response.json():
            embed = self.error_embed(search_response.status_code, search_url)
            await respond(ctx, embed=embed)
            await client.aclose()
            return
        search_data = search_response.json()[0]
        weather_url = (
            f"https://www.metaweather.com/api/location/{search_data['woeid']}"
        )
        weather_response = await client.get(url=weather_url)
        if weather_response.status_code != 200 or not weather_response.json():
            embed = self.error_embed(weather_response.status_code, weather_url)
            await respond(ctx, embed=embed)
            await client.aclose()
            return
        weather_data = weather_response.json()["consolidated_weather"][0]
        embed = discord.Embed(
            title=f"Weather in {search_data['title']} ({search_data['location_type']})",
            description=weather_data["weather_state_name"],
            color=discord.Color.darker_grey(),
            timestamp=datetime.utcnow(),
        )
        embed.add_field(
            name="Wind Speed (MPH)",
            value=str(round(weather_data["wind_speed"])),
        )
        embed.add_field(
            name="Wind Speed (KPH)",
            value=str(round(weather_data["wind_speed"] * 1.609344)),
        )
        embed.add_field(
            name="Temperature (°C)", value=str(round(weather_data["the_temp"]))
        )
        embed.add_field(
            name="Temperature (°F)",
            value=str(round(weather_data["the_temp"] * 1.8 + 32)),
        )
        embed.add_field(name="Humidity", value=f"{weather_data['humidity']}%")
        embed.set_thumbnail(
            url=f"https://www.metaweather.com/static/img/weather/png/{weather_data['weather_state_abbr']}.png"
        )
        embed.set_author(
            name="MetaWeather",
            url="https://www.metaweather.com",
            icon_url="https://www.metaweather.com/static/img/weather/png/lc.png",
        )
        await respond(ctx, embed=embed)


def setup(bot: vbu.Bot):
    """
    Registers command cog to bot.
    :param bot: Bot object
    """
    cog = Weather(bot)
    bot.add_cog(cog)
