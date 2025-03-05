from marzpy import Marzban
import asyncio
        
async def main():
    panel = Marzban("username","password","https://example.com")
    token = await panel.get_token()
    #await panel.anyfunction(token)

asyncio.run(main())
