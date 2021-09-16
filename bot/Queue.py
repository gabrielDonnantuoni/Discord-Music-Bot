from replit import db
from ytdl.YTDLSource import get_audio_source

class Queue():
    def __init__(self, guild_id):
        self.db_queue = db[guild_id]['queue']

    def next(self):
        self.__update_list()
        song = self.__try_get_index()
        return get_audio_source(song) if song else None
    
    def prev(self):
        self.__update_list(foward=False)
        song = self.__try_get_index()
        return get_audio_source(song) if song else None

    def add(self, songs, should_update_index=False):
        self.db_queue['song_list'].extend(songs)
        if should_update_index:
            cur_index = len(self.db_queue['song_list']) - 1
            self.db_queue['cur_song_index'] = cur_index

    def with_local_song(self, query):
        '''
        If query matches a song[title] in song_list return it.
        Otherwise return the default param.
        '''
        try:
            song = next(
                song for song in self.db_queue['song_list']
                if query.lower() in song['title'].lower()
            )
        except StopIteration:
            song = None

        if song:
            cur_index = self.db_queue['song_list'].index(song)
            self.db_queue['cur_song_index'] = cur_index
            return get_audio_source(song)
        
        return None

    def remove(self, query):
        self.db_queue['song_list'] = [
            song for song in self.db_queue['song_list']
            if query.lower() not in song['title'].lower()
        ]
        
    def __try_get_index(self):
        try:
            return self.db_queue['song_list'][self.db_queue['cur_song_index']]
        except IndexError:
            if len(self.db_queue['song_list']) > 0:
                self.db_queue['cur_song_index'] = 0
                return self.db_queue['song_list'][self.db_queue['cur_song_index']]
            else:
                return None

    def __update_list(self, foward=True):
        if not self.db_queue['keep_played']:
            self.db_queue['song_list'].pop(self.db_queue['cur_song_index'])
            
        if foward and self.db_queue['keep_played']:
            self.db_queue['cur_song_index'] += 1
        else:
            self.db_queue['cur_song_index'] -= 1

