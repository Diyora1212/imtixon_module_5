import httpx
import asyncio
import os
import aiofiles

class AsFileManager:
    def __init__(self, path, mode):
        self.path = path
        self.mode = mode

    async def __aenter__(self):
        self.file = await aiofiles.open(self.path, mode=self.mode)
        return self.file

    async def __aexit__(self, *args, **kwargs):
        await self.file.close()

async def meva_data(url, payload):
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=payload)
        return response

async def process_file(file_path, url):
    async with AsFileManager(file_path, "r") as file:
        name = await file.readline()
        price = await file.readline()
        description = await file.read()
        payload = {'name': name.strip(), 'price': price.strip(), 'description': description.strip()}
        print(payload)
        
        response = await meva_data(url, payload)

        if response is not None:
            response_file_name = f"Response {os.path.basename(file_path)} {response.status_code}.txt"
            async with AsFileManager(response_file_name, "w") as response_file:
                await response_file.write(f"Status Code: {response.status_code}\n")
                await response_file.write("Response Content:\n")
                await response_file.write(response.text)

async def main():
    url = "https://164.92.64.76"
    descriptions_folder = "descriptions"
    tasks = []

    for file_name in os.listdir(descriptions_folder)[:10]:
        file_path = os.path.join(descriptions_folder, file_name)
        tasks.append(process_file(file_path, url))
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
