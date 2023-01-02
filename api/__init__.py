import aiohttp


async def create_link(source: str, redirect: str):
    async with aiohttp.ClientSession() as session:
        url = f"http://localhost:6575/api/create_link"
        data = {
            'source': source,
            'redirect': redirect
        }
        async with session.post(url, data=data) as resp:
            response = await resp.json()
            return response


async def is_link_exist(link: str) -> bool:
    async with aiohttp.ClientSession() as session:
        url = f"http://localhost:6575/api/check_link"
        params = {"link": link}
        async with session.get(url, params=params) as resp:
            print("Checking link...")
            print(resp.status)
            print(False if resp.status == 200 else True)
            return False if resp.status == 200 else True


async def get_links():
    async with aiohttp.ClientSession() as session:
        url = f"http://localhost:6575/api/links"
        async with session.get(url) as resp:
            return await resp.json()
