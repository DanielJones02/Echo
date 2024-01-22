

from installation import *
from utilities import *


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Ping Command
    @commands.slash_command()
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)  # Latency in milliseconds
        embed = discord.Embed(title="Ping", description=f"Pong! Latency is {latency}ms", color=embed_colour)
        await ctx.respond(embed=embed) 


    # Say Command
    @commands.slash_command()
    async def say(self, ctx, message: Option(str, "Message to repeat")):
        embed = discord.Embed(title="Say", description=message, color=embed_colour)
        await ctx.respond(embed=embed)


    # Invite Command
    @commands.slash_command()
    async def invite(self, ctx):
        embed = discord.Embed(title="Invite", description=bot_invite, color=embed_colour)
        await ctx.respond(embed=embed) 


    @commands.slash_command()
    async def server_info(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(title="Server Information", color=embed_colour)
        embed.set_thumbnail(url=guild.icon_url)
        embed.add_field(name="Server Name", value=guild.name, inline=True)
        embed.add_field(name="Server ID", value=guild.id, inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Owner", value=guild.owner.display_name, inline=True)
        # Removed the line for region since it's no longer available
        embed.add_field(name="Creation Time", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
        await ctx.respond(embed=embed)


    @commands.slash_command()
    async def user_info(self, ctx, user: Option(discord.Member, "User to get information about", default=None)):
        user = user or ctx.author # if user is blank (no data parsed) it will show the info of the user running the command
        embed = discord.Embed(title="User Information", color=embed_colour)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Username", value=user.display_name, inline=True)
        embed.add_field(name="User ID", value=user.id, inline=True)
        embed.add_field(name="Joined Server", value=user.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
        embed.add_field(name="Account Created", value=user.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
        await ctx.respond(embed=embed) 


    @commands.slash_command()
    async def avatar(self, ctx, user: Option(discord.Member, "User to get avatar for", default=None)):
        user = user or ctx.author

        if isinstance(user, discord.Member):
            embed = discord.Embed(title=f"{user.display_name}'s Avatar", color=embed_colour)

            if user.avatar:
                # User has an avatar, include the URL in the embed
                embed.set_image(url=user.avatar.url)
            else:
                # User doesn't have an avatar, provide a default image or message
                embed.description = "This user does not have an avatar."
        else:
            # Handle the case where user is not a Member
            embed = discord.Embed(title="User Avatar", color=embed_error)
            embed.description = "Invalid user provided."

        await ctx.respond(embed=embed)


    @commands.slash_command()
    async def eight_ball(self, ctx, *, question: str):
        responses = ["It is certain.", "Without a doubt.", "Yes, definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."]
        answer = random.choice(responses)
        embed = discord.Embed(title="🎱 Magic 8-Ball", description=f"Question: {question}\nAnswer: {answer}", color=embed_error)
        await ctx.respond(embed=embed)
    

    @commands.slash_command()
    async def generate_qr(self, ctx, link: str):
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(link)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Save the image to a BytesIO object
        with BytesIO() as image_binary:
            img.save(image_binary, 'PNG')
            image_binary.seek(0)
            # Send the image in discord
            file = discord.File(fp=image_binary, filename='qr_code.png')
            await ctx.respond("Here's your QR code:", file=file)
    

    @commands.slash_command()
    async def membercount(self, ctx):
        guild = ctx.guild
        member_count = guild.member_count

        # Create and respond an embed
        embed = discord.Embed(title="Member Count", color=0x2ecc71)  # You can replace 0x2ecc71 with your desired color
        embed.add_field(name="Server Members", value=f"The server has {member_count} members.", inline=False)

        await ctx.respond(embed=embed)


    @commands.slash_command()
    async def diceroll(self, ctx):
        result = random.randint(1, 6)

        # Create and respond an embed
        embed = discord.Embed(title="Dice Roll", color=0xe74c3c)  # You can replace 0xe74c3c with your desired color
        embed.add_field(name="Result", value=f"You rolled a {result}!", inline=False)

        await ctx.respond(embed=embed)


    @commands.slash_command()
    async def dailyquote(self, ctx):
        # Fetch a random quote from the Quotable API
        response = requests.get("https://api.quotable.io/random")
        if response.status_code == 200:
            quote_data = response.json()
            content = quote_data.get("content", "Quote not available.")
            author = quote_data.get("author", "Unknown")

            # Create and respond an embed
            embed = discord.Embed(title="Quote of the Day", color=0x3498db)  # You can replace 0x3498db with your desired color
            embed.add_field(name="Content", value=content, inline=False)
            embed.add_field(name="Author", value=author, inline=False)

            await ctx.respond(embed=embed)
        else:
            await ctx.respond("Failed to fetch the daily quote. Try again later.")


    @commands.slash_command()
    async def calculator(self, ctx, expression: Option(str, "Mathematical expression")):
        try:
            result = eval(expression)

            # Create a success embed
            embed = discord.Embed(title="Calculation Result", color=embed_colour)
            embed.add_field(name="Expression", value=expression, inline=False)
            embed.add_field(name="Result", value=result, inline=False)

            await ctx.respond(embed=embed)
        except Exception as e:
            # Create an error embed
            embed = discord.Embed(title="Error", description=str(e), color=embed_error)

            await ctx.respond(embed=embed)


    @commands.slash_command()
    async def joke(self, ctx):
        try:
            response = requests.get("https://official-joke-api.appspot.com/random_joke")
            joke_data = response.json()
            setup = joke_data["setup"]
            punchline = joke_data["punchline"]

            # Create an embed
            embed = discord.Embed(title="Joke Time!", color=embed_colour)
            embed.add_field(name="Setup", value=setup, inline=False)
            embed.add_field(name="Punchline", value=punchline, inline=False)

            # Send the embed
            await ctx.respond(embed=embed)
        except Exception as e:
            await ctx.respond(f"Error fetching joke: {e}")



    @commands.slash_command()
    async def coinflip(self, ctx):
        result = random.choice(["Heads", "Tails"])
        embed = discord.Embed(title="Coinflip", description=f"The coin landed on: {result}", color=embed_colour)
        await ctx.respond(embed=embed)


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Fun Cog Loaded! {Fore.RESET}')

def setup(bot):
    bot.add_cog(Fun(bot))