from replit import db
from ytdl.YTDLSource import YTDLSource
import asyncio
from bot.Queue import Queue
import database.main as my_db


class Song():
    def __init__(self, title):
        self.title = title
    
    def __str__(self):
        return f'{self.title}'


if __name__ == '__main__':

    # url = 'https://www.youtube.com/watch?v=4PssBppUr6w&list=PLYbw1heZNGFFSv6Ioihd08jXGrsYDLE37'
    # url_pl = 'https://www.youtube.com/playlist?list=PLYbw1heZNGFFSv6Ioihd08jXGrsYDLE37'

    # asyncio.run(YTDLSource.extract_info(url))
    # asyncio.run(YTDLSource.extract_info(url_pl))
    my_db.init_guild('server')

    queue = Queue('server')

    songs = []
    for index in range(3):
        songs.append({'title': f'Musica {index + 1}'})

    queue.add(songs)

    queue.next()
    queue.next()
    queue.prev()

    queue.remove('3')

    # guild_db = db['server']

    # db_queue = guild_db['queue']

    # db_queue['song_list'].append(1)

    # db_queue['cur_song_index'] += len(db_queue['song_list'])

    print(db['server'])

    if '' in 'any content':
        print('valido')

    
