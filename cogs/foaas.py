import discord
from discord.ext import commands, vbu

from cogs.utils import foaas


RESPONSES = {
    "absolutely": "Absolutely fucking not, %s, no fucking way!",
    "anyway": "Who the fuck are you anyway, %s, why are you stirring up so much trouble, and, who pays you?",
    "awesome": "This is Fucking Awesome.",
    "back": "%s, back the fuck off.",
    "bday": "Happy Fucking Birthday, %s.",
    "because": "Why?  Because fuck you, that's why.",
    "bm": "Bravo mike, %s.",
    "bye": "Fuckity bye!",
    "caniuse": "Can you use %s?  Fuck no!",
    "cup": "How about a nice cup of shut the fuck up?",
    "dumbledore": "Happiness can be found, even in the darkest of times, if one only remembers to fuck off.",
    "equity": "Equity only? Long hours? Zero Pay? Well %s, just sign me right the fuck up.",
    "fascinating": "Fascinating story, in what chapter do you shut the fuck up?",
    "flying": "I don't give a flying fuck.",
    "fts": "Fuck that shit, %s.",
    "give": "I give zero fucks.",
    "idea": "That sounds like a fucking great idea!",
    "immensity": "You cannot imagine the immensity of the FUCK I do not give.",
    "keep": "%s: Fuck off. And when you get there, fuck off from there too. Then fuck off some more. Keep fucking off until you get back here. Then fuck off again.",
    "keepcalm": "Keep the fuck calm and %s!",
    "legend": "%s, you're a fucking legend.",
    "logs": "Check your fucking logs!",
    "no": "No fucks given.",
    "problem": "What the fuck is your problem, %s?",
    "programmer": "Fuck you, I'm a programmer!",
    "question": "To fuck off or not to fuck off (that is not a question)",
    "ridiculous": "That's fucking ridiculous",
    "rockstar": "%s, you're a fucking Rock Star!",
    "rtfm": "Read the fucking manual!",
    "shutup": "%s, shut the fuck up.",
    "single": "Not a single fuck was given.",
    "think": "%s, you think I give a fuck?",
    "thinking": "%s, what the fuck were you actually thinking?",
    "what": "What the fuck?",
    "xmas": "Merry Fucking Christmas, %s.",
    "yoda": "Fuck you, you must, %s.",
    "zero": "Zero, that's the number of fucks I give."
}


class FOAAS(vbu.Cog):
    @commands.group(name='foaas', invoke_without_subcommand=False)
    async def foaas(self, ctx: vbu.Context):
        """Fock Off as a Service (FOAAS)"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @foaas.command()
    async def info(self, ctx: vbu.Context):
        """Provides information about the FOAAS module."""
        embed = discord.Embed(
            title="Fuck Off as a Service",
            description="FOAAS (Fuck Off As A Service) provides a modern, RESTful, scalable solution to the common problem of telling people to fuck off.\nWe've implemented the responses to the API without calling the API itself, however credit must be given to the makers of these responses.\n\nYou can find them over at https://www.foaas.com/",
            colour=discord.Colour.dark_theme(),
        )
        await ctx.send(embed=embed)

    async def halt_until_agree(self, ctx: vbu.Context):
        embed = discord.Embed(
            title="Hold up!",
            description="""You need to agree to the following rules before you can use the FOAAS module.

**1)** This module is designed for fun use only, and is not to be used for harassment of other users.
**2)** Do not harass other users using this system.  Abuse of this system will not be tolerated.
**3)** If you are found to be abusing this system, you will be blocked permanently from using it.

Pressing the button below constitutes acceptance of these rules.""",
            colour=discord.Colour.dark_red(),
        )
        components = discord.ui.MessageComponents(
            discord.ui.ActionRow(
                discord.ui.Button(label="I agree to the rules.", custom_id=f"FOAAS AGREE {ctx.author.id}")
            )
        )
        await ctx.send(embed=embed, components=components)

    @commands.Cog.listener("on_component_interaction")
    async def handle_component(self, interaction: discord.Interaction):
        if not isinstance(interaction.component, discord.ui.button.Button):
            return
        if not interaction.component.custom_id.startswith("FOAAS"):
            return
        mode, user_id = interaction.component.custom_id.split(" ")[1:]
        if int(user_id) != interaction.user.id:
            await interaction.response.send_message("This prompt can only be responded to by the user who triggered it!", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        embeds = interaction.message.embeds
        components = discord.ui.MessageComponents(
            discord.ui.ActionRow(
                discord.ui.Button(label="I agree to the rules.", custom_id=f"FOAAS AGREE {interaction.user.id}", disabled=True)
            )
        )
        await interaction.message.edit(embeds=embeds, components=components)
        await foaas.accept(user_id)
        await interaction.edit_original_message(content="Thank you for accepting the rules of the FOAAS module.")

    @foaas.command()
    async def exec(self, ctx: vbu.Context, response: str, param: str = None):
        if not await foaas.check(ctx.author.id):
            await self.halt_until_agree(ctx)
            return
        if response not in RESPONSES.keys():
            await ctx.send("Oops... That response doesn't seem to exist in my database.  Please try again.\n\nYou can use `/foaas responses` to see a list of possible responses.", ephemeral=True)
            return
        text = RESPONSES[response] + f" - {ctx.author.display_name}"
        if "%s" in text:
            if param:
                text = text.replace("%s", param)
            else:
                await ctx.send("Oops... That response requires a parameter (`param`)!", ephemeral=True)
                return
        await ctx.send(content=text)

    @foaas.command()
    async def responses(self, ctx: vbu.Context):
        response = "The following responses are available:"
        for i in RESPONSES.keys():
            response += f"\n**{i}** - {RESPONSES[i].replace('%s', '{param}')}"
        response += "\n\nNote: The value `{param}` will be replaced with the value you provide with the `param` optional argument of the `/foaas exec` command."
        embed = discord.Embed(
            title="FOAAS Responses",
            description=response,
            colour=discord.Colour.dark_theme(),
        )
        await ctx.send(embed=embed, ephemeral=True)


def setup(bot: vbu.Bot):
    cog = FOAAS(bot)
    bot.add_cog(cog)