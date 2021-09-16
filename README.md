## Discord Music Bot

In this project I use:
 - [discord.py](https://discordpy.readthedocs.io): Awesome library that implements all Discord API;
 - [replit](https://replit.com): Easy to use platform with free host and nice built-in database;
 - [youtube API](https://developers.google.com/youtube/v3/docs): Help to find videos url on youtube by query;
 - [yt-dlp](https://github.com/yt-dlp/yt-dlp): Get stream url from video url on youtube.
 - [Uptime Robot](https://uptimerobot.com/): To keep bot alive.

### How to use
Fork this project, create a free account on *replit* and pull your github repo to your repl.

If you open `env.py` file you will see two ENV_VARIABLES. You need to feel then with your data to the bot run properly. 
 - BOT_TOKEN: Create you bot in [Discord Developer Portal](https://discord.com/developers/applications) and copy your token.
 - GOOGLE_API_TOKEN: Create account on Google Dev platform and get your token.

Don't forget to add your tokens to replit secrets (Enviroment variables). Finally click RUN (or Ctrl + Enter).

The replit server keep running for an hour without requests, after that they enter in sleeping stage. So, to prevent you bot to go to sleep you can you the free service of *Uptime Robot*.

Create an account on *Uptime Robot* and add an new monitor for the url of your repl with a interval. You don't need a short interval, I use 20 min.


### Features
**Note: The main code is written in English, but the bot commands and answers (with funny stuff :D) are in Portuguese, thats is my native language.**

 - Prefix: `.ava`. Choose what you want.

 - Commands:
    - add: Receives an video url or query and add it to the list/queue. If receives a query look for the first match on YouTube. You can use " e toca" at the end of query to start playing it instantly.

    Examples:
    ```
    .ava add https://www.youtube.com/watch?v=-6J3HfX4sbg //will just append to list/queue
    .ava add zé vaqueiro tenho medo //same as previous
    .ava add coração radiante e toca //will play right after fetch needed info
    ```
    - toca: Receives an video url or query and play it. If arg is a query, first try to find a matching song on database list/queue, otherwise look on youtube as `add` command.

    Examples:
    ```
    .ava toca https://www.youtube.com/watch?v=-6J3HfX4sbg
    .ava toca ta vendo aquela lua
    ```
    - apaga: Receives a query and delete all matching songs on list/queue.

    Examples:
    ```
    .ava apaga tenho medo //will delete 'Tenho Medo - Zé Vaqueiro (Vídeo Oficial)'
    .ava apaga //will delete all.
    ```

    - lista: Print to chat all the current songs on list/queue.

    - proxima(alias=prox): Skip to next song on list/queue.
    
    - anterior(alias=ant): Back to previous song on list/queue.

    - perai: Pause song, if playing.

    - continua: Resume song, if paused.

    - vaza: Disconnect voice from channel, if connected.


