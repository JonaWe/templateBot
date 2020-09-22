from discord.ext import commands


class SubCommandRequired(commands.BadArgument):
    pass

class NoPermissionsToViewThisCommand(commands.UserInputError):
    pass