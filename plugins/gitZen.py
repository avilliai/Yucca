import aiohttp


async def get_zen(timeout=10):
    url = 'https://api.github.com/zen'
    timeout = aiohttp.ClientTimeout(total=timeout)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url=url) as resp:
            return await resp.text()