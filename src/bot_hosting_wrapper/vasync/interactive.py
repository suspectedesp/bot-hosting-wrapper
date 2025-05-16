import aiohttp
import asyncio
import sys

from datetime import datetime, timezone
from os import name as os_name, system

class Interactive:
    def __init__(self, auth_id):
        """
        Initializes the interactive Class
        Args:
            auth_id (str): The auth id of the account.
        """
        self.auth_id = auth_id
        self._headers = {
            "Authorization": self.auth_id,
            "content-type": "application/json"
        }


    @staticmethod
    def cls():
        if os_name == 'nt':
            if sys.stdout.isatty():  # cause for some older versions it wont work properly
                try:
                    print("\033[H\033[J", end="") # "magic" ansi sequence
                except:
                    system('cls')
            else:
                system('cls')
        else:
            print("\033[H\033[J", end="")


    async def get_info(self) -> None:
        """
        Gets all servers, then lets you select one to show info.
        """
        async with aiohttp.ClientSession(headers=self._headers) as session:
            try:
                async with session.get("https://bot-hosting.net/api/servers", timeout=6) as resp_list:
                    if resp_list.status != 200:
                        print(f"Error: {resp_list.status}")
                        print("Response:")
                        print(await resp_list.text())
                        return
                    server_list = await resp_list.json()
            except Exception as e:
                print(f"Error fetching server list: {e}")
                return

            print("Available Servers:")
            for index, server_info in enumerate(server_list, start=1):
                print(f"{index}. Server ID: {server_info['serverid']}, Name: {server_info['name']}")

            print("Select your server ID or list number: ")
            loop = asyncio.get_event_loop()
            selection_input = await loop.run_in_executor(None, input, "[>] ")

            self.cls()

            try:
                selection = int(selection_input)
                selected_server_id = str(server_list[selection - 1]['serverid'])
            except (ValueError, IndexError):
                selected_server_id = selection_input

            try:
                async with session.get(f"https://bot-hosting.net/api/servers/{selected_server_id}", timeout=6) as resp_details:
                    if resp_details.status != 200:
                        print(f"Error: {resp_details.status}")
                        print("Response:")
                        print(await resp_details.text())
                        return
                    data = await resp_details.json()
            except Exception as e:
                print(f"Error fetching server details: {e}")
                return

            identifier = data.get("identifier")
            suspended = data.get("suspended")
            name = data.get("name")
            coins_per_month = data.get("plan", {}).get("coinsPerMonth")
            cpu = data.get("plan", {}).get("cpu")
            storage = data.get("plan", {}).get("storage")
            ram = data.get("plan", {}).get("ram")

            next_renewal = data.get("nextRenewal")
            if not next_renewal:
                print("Error: 'nextRenewal' is missing/None")
                return

            renewal_numeric = int(''.join(c for c in str(next_renewal) if c.isdigit()))
            unix_timestamp = renewal_numeric / 1000
            renewal_date = datetime.fromtimestamp(unix_timestamp, timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

            print(f"Identifier: {identifier}")
            print(f"Server ID: {selected_server_id}")
            print(f"Is suspended?: {suspended}")
            print(f"Server Name: {name}")
            print(f"Coins per month: {coins_per_month}")
            print(f"Storage: {storage} MB")
            print(f"Ram: {ram} MB")
            print(f"CPU: {cpu}%")
            print(f"Next Renewal: {renewal_date}")