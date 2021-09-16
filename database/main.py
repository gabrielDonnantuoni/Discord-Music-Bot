from replit import db


def verify_guild_db(ctx):
    guild_id = f'{ctx.guild.id}'
    if not db.get(guild_id):
        init_guild(guild_id)
    return guild_id


def init_guild(guild_id):
    db[guild_id] = {
        'queue': {
            'cur_song_index': -1,
            'song_list': [],
            'keep_played': True,
        },
        'config': {
        },
    }
