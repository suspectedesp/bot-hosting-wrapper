import os
import requests
import subprocess

from datetime import datetime, timezone


class Interactive:
    def __init__(self, auth_id):
        self.auth_id = auth_id
        self._headers = {
            "Authorization": self.auth_id,
            "content-type": "application/json"
        }


    @staticmethod
    def cls():
        subprocess.run(['cls'] if os.name == 'nt' else ['clear'])


    def get_info(self) -> None:
        """
        First gets all your servers, then you can select a certain one, and it shows you the specific info about it
        Such as: Renewal, Identifier, Server ID, if its suspended, etc.
        """
        url_list = "https://bot-hosting.net/api/servers"
        response_list = requests.get(url_list, headers=self._headers, timeout=6)
        if response_list.status_code != 200:
            print(f"Error: {response_list.status_code}")
            print("Response:")
            print(response_list.text)
            return

        server_list = response_list.json()
        print("Available Servers:")

        for index, server_info in enumerate(server_list, start=1):
            print(f"{index}. Server ID: {server_info['serverid']}, Name: {server_info['name']}")

        print("Select your server ID or list number: ")
        selection_input = input("[>]")
        self.cls()

        try:
            selection = int(selection_input)
            selected_server_id = str(server_list[selection - 1]['serverid'])
        except (ValueError, IndexError):
            selected_server_id = selection_input

        url_details = f"https://bot-hosting.net/api/servers/{selected_server_id}"
        response_details = requests.get(url_details, headers=self._headers, timeout=6)
        if response_details.status_code != 200:
            print(f"Error: {response_details.status_code}")
            print("Response:")
            print(response_details.text)
            return

        data = response_details.json()

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
