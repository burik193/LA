import engine
import mainframe
import mainframe as MF

MF = mainframe.MF()
guild_list = MF.get_guild_list()
engine = engine.Engine()
raid_name = engine.get_zone()
search = engine.get_boss(raid_name=raid_name)
if search:
    list_of_classes = engine.get_setups(guild_list=guild_list)
else:
    list_of_classes = engine.get_setups_offline(guild_list=guild_list)