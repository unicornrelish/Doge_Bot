#Utility commands for the bot to execute.
from discord.ext import commands
import discord
import random
from datetime import datetime as d
from var import mcserver_ip

class Utilities(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='help',
        description='Displays this text!',
        aliases=['commands', 'command'],
        usage='cog'
        )
    async def help_command(self, ctx, cog='all'):
   
        # The third parameter comes into play when
        # only one word argument has to be passed by the user

        # Prepare the embed

        help_embed = discord.Embed(
            title='Help',
            color=0xC27C0E
        )
        help_embed.set_thumbnail(url=self.bot.user.avatar_url)
        help_embed.set_footer(
            text=f'Requested by {ctx.message.author.name}',
            icon_url=self.bot.user.avatar_url
        )

        # Get a list of all cogs
        cogs = [c for c in self.bot.cogs.keys()]

        # If cog is not specified by the user, we list all cogs and commands

        if cog == 'all':
            for cog in cogs:
                # Get a list of all commands under each cog

                cog_commands = self.bot.get_cog(cog).get_commands()
                commands_list = ''
                for comm in cog_commands:
                    commands_list += f'**{comm.name}** - *{comm.description}*\n'

                # Add the cog's details to the embed.

                help_embed.add_field(
                    name=cog,
                    value=commands_list,
                    inline=False
                ).add_field(
                    name='\u200b', value='\u200b', inline=False
                )

                # Also added a blank field '\u200b' is a whitespace character.
            pass
        else:

            # If the cog was specified

            lower_cogs = [c.lower() for c in cogs]

            # If the cog actually exists.
            if cog.lower() in lower_cogs:

                # Get a list of all commands in the specified cog
                commands_list = self.bot.get_cog(cogs[ lower_cogs.index(cog.lower()) ]).get_commands()
                help_text=''

                # Add details of each command to the help text
                # Command Name
                # Description
                # [Aliases]
                #
                # Format
                for command in commands_list:
                    help_text += f'```{command.name}```\n' \
                        f'**{command.description}**\n\n'

                    # Also add aliases, if there are any
                    if len(command.aliases) > 0:
                        help_text += f'**Aliases :** `{"`, `".join(command.aliases)}`\n\n\n'
                    else:
                        # Add a newline character to keep it pretty
                        # That IS the whole purpose of custom help
                        help_text += '\n'

                    # Finally the format
                    help_text += f'Format: `@{self.bot.user.name}#{self.bot.user.discriminator}' \
                        f' {command.name} {command.usage if command.usage is not None else ""}`\n\n\n\n'

                help_embed.description = help_text
            else:
                # Notify the user of invalid cog and finish the command
                await ctx.send('Invalid cog specified.\nUse `help` command to list all cogs.')
                return

        await ctx.send(embed=help_embed)
   
        return

    @commands.command(name='ping', description='The ping command!')
    async def ping_command(self, ctx):
        start = d.timestamp(d.now())
    	# Gets the timestamp when the command was used
        
        msg = await ctx.author.send(content='Pinging')
        # Sends a message to the user in the channel the message with the command was received.
    	# Notifies the user that pinging has started

        await msg.edit(content=f'Pong!\nOne message round-trip took {( d.timestamp( d.now() ) - start ) * 1000 }ms.')
    	# Ping completed and round-trip duration show in ms
    	# Since it takes a while to send the messages
    	# it will calculate how much time it takes to edit an message.
    	# It depends usually on your internet connection speed
        return

    @commands.command(name='stats', description='Displays server stats!')
    async def stats_command(self, ctx):
        total = 0
        online = 0
        offline = 0
        idle = 0
        gaming = 0
        streaming = 0

        msg = await ctx.send('Processing...')
        
        if ctx.guild is not None:
            for user in ctx.guild.members:
                total += 1
            
                if user.status == discord.Status.offline:
                    offline += 1
                elif user.status == discord.Status.online:
                    online += 1
                elif user.status == discord.Status.idle:
                    idle += 1
                if user.activity is not None:    
                    if user.activity.type == discord.ActivityType.playing:
                        gaming += 1
                    elif user.activity.type == discord.ActivityType.streaming:
                        streaming += 1

        
            embed = discord.Embed(
                title='Server Stats', 
                color=0xC27C0E
            )
            embed.set_thumbnail(
                url=ctx.guild.icon_url
            )
            embed.set_footer(
                text=f'Requested by {ctx.message.author.name}',
                icon_url=self.bot.user.avatar_url
            )
            embed.add_field(name='Online', value=online)
            embed.add_field(name='Offline', value=offline)
            embed.add_field(name='Total', value=total)
            embed.add_field(name='Idle', value=idle)
            embed.add_field(name='Gaming', value=gaming)
            embed.add_field(name='Streaming', value=streaming)

            await msg.edit(content=None, embed=embed)
        
        else:
            await msg.edit(content='Try using this in a server!')


    @commands.command(name='mcserver', description='Shows the Minecraft Server IP!')
    async def mcserver_command(self, ctx):
        await ctx.send(f'IP: `{mcserver_ip}`')

def setup(bot):
    bot.add_cog(Utilities(bot))
    # Adds the Basic commands to the bot
    # Note: The "setup" function has to be there in every cog file

    
