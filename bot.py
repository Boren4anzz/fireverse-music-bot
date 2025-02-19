import aiohttp
import asyncio
import time
from datetime import timedelta
from colorama import Fore, Style, init

# Initialize colorama
init()

class FireverseMusicBot:
    def __init__(self, token, account_index):
        self.base_url = 'https://api.fireverseai.com'
        self.token = token
        self.account_index = account_index
        self.played_songs = set()
        self.daily_play_count = 0
        self.DAILY_LIMIT = 50
        self.last_heartbeat = time.time()
        self.total_listening_time = 0
        self.headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.8',
            'content-type': 'application/json',
            'origin': 'https://app.fireverseai.com',
            'referer': 'https://app.fireverseai.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'x-version': '1.0.100',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Brave";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'sec-gpc': '1',
            'token': token
        }

    def log(self, message, overwrite=False):
        prefix = f'[Account {self.account_index}] '
        if overwrite:
            print(f'\r{prefix}{message}', end='')
        else:
            print(f'{prefix}{message}')

    def format_time(self, seconds):
        return str(timedelta(seconds=seconds))

    async def initialize(self):
        try:
            await self.get_user_info()
            await self.get_daily_tasks()
            return True
        except Exception as e:
            self.log(f'❌ Error initializing bot: {str(e)}')
            return False

    async def get_user_info(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'{self.base_url}/userInfo/getMyInfo', headers=self.headers) as response:
                    data = await response.json()
                    level = data['data']['level']
                    exp_value = data['data']['expValue']
                    score = data['data']['score']
                    next_level_exp_value = data['data']['nextLevelExpValue']
                    print(Fore.YELLOW + "==================================================")
                    print("                     BOT STATUS")
                    print("==================================================" + Style.RESET_ALL)
                    print(f">> Detected Account: {self.account_index}")
                    print(Fore.YELLOW + "--------------------------------------------------")
                    print(f"[ ACCOUNT {self.account_index} ] - USER STATS")
                    print("--------------------------------------------------" + Style.RESET_ALL)
                    print(f"   Level            : {level}")
                    print(f"   EXP              : {exp_value} / {next_level_exp_value}")
                    print(f"   Score           : {score:,}")
                    print(f"   Total Time      : {int(self.total_listening_time / 60)} minutes")
                    print(Fore.YELLOW + "--------------------------------------------------" + Style.RESET_ALL)
        except Exception as e:
            self.log(f'❌ Error getting user info: {str(e)}')

    async def get_daily_tasks(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'{self.base_url}/musicTask/getListByCategory?taskCategory=1', headers=self.headers) as response:
                    data = await response.json()
                    if data.get('data') and isinstance(data['data'], list):
                        print(Fore.GREEN + f"[ ACCOUNT {self.account_index} ] - DAILY TASKS PROGRESS")
                        print("--------------------------------------------------" + Style.RESET_ALL)
                        for task in data['data']:
                            if task and task.get('name'):
                                if task.get('taskKey') == 'play_music' and task.get('unit') == 'minutes':
                                    progress = f'{int(self.total_listening_time / 60)}/{task.get("completeNum")}'
                                else:
                                    progress = task.get('itemCount') or f'{task.get("completedRounds", 0)}/{task.get("maxCompleteLimit", task.get("completeNum", 0))}'
                                status = Fore.GREEN + "[✔]" + Style.RESET_ALL if progress.split('/')[0] == progress.split('/')[1] else "[ ]"
                                print(f"   {status} {task.get('name')} ({progress})       (+{task.get('rewardScore')} pts)")
                        print(Fore.GREEN + "--------------------------------------------------" + Style.RESET_ALL)
        except Exception as e:
            self.log(f'❌ Error getting daily tasks: {str(e)}')

    async def get_recommended_songs(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f'{self.base_url}/home/getRecommend', json={'type': 1}, headers=self.headers) as response:
                    data = await response.json()
                    return data.get('data', [])
        except Exception as e:
            self.log(f'❌ Error getting recommended songs: {str(e)}')
            return []

    async def add_to_history(self, music_id):
        try:
            async with aiohttp.ClientSession() as session:
                await session.post(f'{self.base_url}/musicHistory/addToHistory/{music_id}', headers=self.headers)
        except Exception as e:
            self.log(f'❌ Error adding to history: {str(e)}')

    async def get_music_details(self, music_id):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'{self.base_url}/music/getDetailById?musicId={music_id}', headers=self.headers) as response:
                    data = await response.json()
                    return data.get('data')
        except Exception as e:
            self.log(f'❌ Error getting music details: {str(e)}')
            return None

    async def send_heartbeat(self):
        try:
            now = time.time()
            if now - self.last_heartbeat >= 30:
                async with aiohttp.ClientSession() as session:
                    await session.post(f'{self.base_url}/music/userOnlineTime/receiveHeartbeat', headers=self.headers)
                self.last_heartbeat = now
                print('💓', end='')
        except Exception:
            pass

    async def play_music(self, music_id):
        try:
            async with aiohttp.ClientSession() as session:
                await session.post(f'{self.base_url}/musicUserBehavior/playEvent', json={'musicId': music_id, 'event': 'playing'}, headers=self.headers)
            return True
        except Exception:
            return False

    async def end_music(self, music_id):
        try:
            async with aiohttp.ClientSession() as session:
                await session.post(f'{self.base_url}/musicUserBehavior/playEvent', json={'musicId': music_id, 'event': 'playEnd'}, headers=self.headers)
            return True
        except Exception as e:
            self.log(f'❌ Error ending music: {str(e)}')
            return False

    async def like_music(self, music_id):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f'{self.base_url}/musicMyFavorite/addToMyFavorite?musicId={music_id}', headers=self.headers) as response:
                    data = await response.json()
                    return data.get('success', False)
        except Exception as e:
            self.log(f'❌ Error liking music: {str(e)}')
            return False

    async def comment_music(self, music_id, content="good one"):
        try:
            comment_data = {
                'content': content,
                'musicId': music_id,
                'parentId': 0,
                'rootId': 0
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(f'{self.base_url}/musicComment/addComment', json=comment_data, headers=self.headers) as response:
                    data = await response.json()
                    return data.get('success', False)
        except Exception as e:
            self.log(f'❌ Error commenting on music: {str(e)}')
            return False

    async def play_session(self):
        try:
            if self.daily_play_count >= self.DAILY_LIMIT:
                self.log(f'\n🎵 Daily limit reached ({self.DAILY_LIMIT}/{self.DAILY_LIMIT}). Waiting for reset...')
                return False

            songs = await self.get_recommended_songs()
            if not songs:
                self.log('\n❌ No songs available, retrying in 5 seconds...')
                await asyncio.sleep(5)
                return True

            for song in songs:
                if song['id'] in self.played_songs:
                    continue

                self.played_songs.add(song['id'])
                self.daily_play_count += 1

                music_details = await self.get_music_details(song['id']) or {}
                duration = music_details.get('duration', song.get('duration', 180))

                await self.add_to_history(song['id'])

                song_name = song.get('musicName', music_details.get('musicName', 'Unknown Song'))
                author = song.get('author', music_details.get('author', 'Unknown Artist'))

                print(Fore.CYAN + f"[ ACCOUNT {self.account_index} ] - NOW PLAYING")
                print("--------------------------------------------------" + Style.RESET_ALL)
                print(f"   Title          : {song_name}")
                print(f"   Artist        : {author}")
                print(f"   Music ID      : {song['id']}")
                print(f"   Progress      : {self.daily_play_count} / {self.DAILY_LIMIT} songs today")
                print(f"   Duration      : {self.format_time(duration)}")
                like_success = await self.like_music(song['id'])
                print(f"   Like Status   : {Fore.GREEN + 'SUCCESS' + Style.RESET_ALL if like_success else Fore.RED + 'FAILED' + Style.RESET_ALL}")
                comment_success = await self.comment_music(song['id'])
                print(f"   Comment Status: {Fore.GREEN + 'SUCCESS' + Style.RESET_ALL if comment_success else Fore.RED + 'FAILED' + Style.RESET_ALL}")
                print(f"   Time Left     : {self.format_time(duration)}")
                print(f"   Listening Time: {int(self.total_listening_time / 60)} minutes")
                print(Fore.CYAN + "--------------------------------------------------" + Style.RESET_ALL)

                if await self.play_music(song['id']):
                    seconds_played = 0
                    for time_left in range(duration, 0, -1):
                        await self.send_heartbeat()
                        seconds_played += 1
                        self.total_listening_time += 1

                        self.log(f'⏳ Time remaining: {self.format_time(time_left)} | Listening time: {int(self.total_listening_time / 60)} minutes', True)
                        await asyncio.sleep(1)

                    end_success = await self.end_music(song['id'])
                    if end_success:
                        self.log('\n✅ Finished playing')
                    else:
                        self.log('\n⚠️ Song ended but playEnd event failed')

                    await self.get_user_info()
                    await self.get_daily_tasks()
                    break
                else:
                    self.log('\n❌ Failed to play song')
            return True
        except Exception as e:
            self.log(f'❌ Error in play session: {str(e)}')
            await asyncio.sleep(5)
            return True

    async def start_daily_loop(self):
        while True:
            should_continue = await self.play_session()
            if not should_continue:
                self.log('\n⏰ Waiting 24 hours before next session...')
                for time_left in range(24 * 60 * 60, 0, -1):
                    self.log(f'⏳ Next session in: {self.format_time(time_left)}', True)
                    await asyncio.sleep(1)
                self.daily_play_count = 0
                self.played_songs.clear()
                self.total_listening_time = 0
                self.log('\n🔄 Starting new daily session')
                await self.get_user_info()
                await self.get_daily_tasks()
            else:
                await asyncio.sleep(5)

async def read_tokens():
    try:
        with open('tokens.txt', 'r') as file:
            return [line.strip() for line in file if line.strip() and not line.startswith('#')]
    except Exception as e:
        print(f'❌ Error reading tokens.txt: {str(e)}')
        exit(1)

async def main():
    tokens = await read_tokens()
    if not tokens:
        print('❌ No tokens found in tokens.txt')
        exit(1)

    bots = [FireverseMusicBot(token, index + 1) for index, token in enumerate(tokens)]
    init_results = await asyncio.gather(*[bot.initialize() for bot in bots])
    active_bots = [bot for bot, success in zip(bots, init_results) if success]

    if not active_bots:
        print('❌ No accounts could be initialized successfully')
        exit(1)

    await asyncio.gather(*[bot.start_daily_loop() for bot in active_bots])

if __name__ == '__main__':
    asyncio.run(main())