import os
import json

import asyncio
import traceback
import aiohttp
import urllib.parse

domain = 'https://www.partslink24.com'
proxy = 'https://127.0.0.1:8080'
urls = [
    # ('Jaguar', 'https://www.partslink24.com/p5jlr/extern/vehicle/models?lang=zh-TW&serviceName=jaguar_parts&upds=2023-02-14--09-36&_=1676796282460'),
    ('Land Rover', 'https://www.partslink24.com/p5jlr/extern/vehicle/models?lang=zh-TW&serviceName=landrover_parts&_=1676885404540'),
]


def save_to_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(f'{path}.json', 'w+') as f:
        f.write(json.dumps(content, indent=4))


async def crawl_depth(link, name):
    if not link:
        return
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.get(link, proxy=proxy, ssl=False) as response:
                # NOTE: check the reponse is json or not.
                if not response.headers.get('content-type', '').startswith('application/json'):
                    return 
                response_as_dict = await response.json()
                save_to_file(name, response_as_dict)
                type_details = response_as_dict.get('data', {}).get('records', [])
                for detail in type_details:
                    child_url = detail.get('link', {}).get('path', '')
                    component_value = detail.get('values', {})
                    component_name = component_value.get('name', '') or component_value.get('code', '')
                    if child_url and component_name:
                        await crawl_depth(
                            urllib.parse.urljoin(domain, child_url),
                            os.path.join(name, component_name, component_name)
                        )
    except Exception as e:
        print(traceback.format_exc())


async def main():
    async with asyncio.TaskGroup() as tg:
        for name, url in urls:
            tg.create_task(crawl_depth(url, f'{name}/{name}'))

asyncio.run(main())
