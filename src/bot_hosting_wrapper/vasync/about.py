import aiohttp

from colorama import Fore
from datetime import datetime, timezone

from typing import Any


urls = {
    "servers": "https://bot-hosting.net/api/servers/",
    "affiliate": "https://bot-hosting.net/api/affiliate",
    "newPassword": "https://bot-hosting.net/api/newPassword",
    "freeCoinsStatus": "https://bot-hosting.net/api/freeCoinsStatus",
    "me": "https://bot-hosting.net/api/me"
}

server_urls = {
    "delete": "https://bot-hosting.net/api/servers/delete",
    "changeSoftware": "https://bot-hosting.net/api/servers/changeSoftware"
}

class Account:
    def __init__(self, auth_id):
        """
        Initializes an Account object with the given auth id.
        Args:
            auth_id (str): The auth id of the account.
        """
        self.auth_id = auth_id
        self._headers = {
            "Authorization": self.auth_id,
            "content-type": "application/json"
        }

    async def coins_amount(self) -> (Any | dict[str, str] | str):
        """
        Gets the total amount of your coins.
        Returns:
            The coin amount
            or a dictionary with an error message and status code if the request failed. {Error, Message}
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(urls["me"], headers=self._headers, timeout=6) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('coins')
                    else:
                        return {"Error": f"Received status code {response.status}", "Message": await response.text()}
        except aiohttp.ClientError as e:
            return f"Request failed: {e}"

    async def affiliate_data(self)-> (dict[str, Any] | str):
        """
        Returns affiliate data (coins/referral, uses and your link)
        Returns:
            If status code is 200 and no error occurs: 
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(urls["affiliate"], headers=self._headers, timeout=6) as response:
                    data = await response.json()
                    if response.status != 200:
                        return {"Error": f"Received status code {response.status}", "Message": await response.text()}
        except aiohttp.ClientError as e:
            return f"Request failed: {e}"

        return {
            "coinsPerReferral": data["coinsPerReferral"],
            "enabled": data["enabled"],
            "link": data["link"],
            "uses": data["uses"]
        }

    async def about(self):
        """
        Will give you a quick overview of your account.
        Returns a dictionary with account details or an 'error' message if something goes wrong.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(urls["me"], headers=self._headers, timeout=6) as response:
                if response.status == 200:
                    try:
                        user_info = await response.json()
                        return {
                            "username": user_info.get('username', 'Unknown'),
                            "id": user_info.get('id', 'Unknown'),
                            "coins": user_info.get('coins', 'Unknown'),
                            "avatar": user_info.get('avatar', 'No Avatar')
                        }
                    except Exception as e:
                        return {"error": f"JSON parse error: {e}"}
                else:
                    return {"error": f"Status {response.status}: {await response.text()}"}

    async def id_check(self, about=False):
        """
        Checks if your Auth ID is valid.
        Params:
        about (bool): If True, print user info in the console. Default is False.
        """
        success = False
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(urls["me"], headers=self._headers, timeout=6) as response:
                    if response.status == 200:
                        user_info = await response.json()
                        success = True
                        if about:
                            print("Username:", user_info.get('username', 'Unknown'), "| ID:", user_info.get('id', 'Unknown'))
                    return {"Success": success, "Status Code": response.status}
        except aiohttp.ClientError as e:
            return f"Failed to contact the API: {e}"
        
    async def sftp_pass(self):
        """
        This will generate a new SFTP password
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(urls["newPassword"], headers=self._headers, timeout=6) as response:
                data = await response.json()
                return data.get("password")

    async def claimable(self):
        """
        Check if free coins are claimable and the time left
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(urls["freeCoinsStatus"], headers=self._headers, timeout=6) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "claimable": data["claimable"],
                        "timeLeft": data["timeLeft"]
                    }
                else:
                    return {"Status-Code": f"{response.status}", "Message": await response.text()}




class Server:
    def __init__(self, auth_id):
        self.auth_id = auth_id
        self._headers = {
            "Authorization": self.auth_id,
            "content-type": "application/json"
        }

    async def change_language(self, language=None, server_id: str = None):
        """
        Changes the programming language of a specified server.

        Params:
            language (str, required): The programming language to switch to (java, python, nodejs, lua, deno, nodemon).
            server_id (str, required): The server ID.

        Returns:
            dict: Success or error message.
        """
        if not server_id or not language:
            return {"error": True, "message": "Missing server_id or language"}

        language_to_egg = {
            "nodejs": 16,
            "python": 17,
            "java": 18,
            "deno": 19,
            "nodemon": 20,
            "lua": 21
        }

        # corresponding id
        egg = language_to_egg.get(language.lower())
        if egg is None:
            return {"error": True, "message": f"Invalid language '{language}'."}

        payload = {"id": server_id, "egg": str(egg)}

        async with aiohttp.ClientSession() as session:
            async with session.post(server_urls["changeSoftware"], headers=self._headers, json=payload, timeout=6) as response:
                if response.status == 200:
                    return {"success": True, "message": "Software change successful"}
                else:
                    return {"error": True, "status_code": response.status, "message": await response.text()}

    async def get_info(self, specific_info=None, everything=False, selected_server_id: str = None) -> dict | str:
        """
        Fetches details about a selected server.
        Params:
            specific_info (str, optional): The specific info to retrieve (e.g., "cpu", "ram").
            everything (bool, optional): Whether to return all server info.
            selected_server_id (str, optional): The server ID to query.

        Returns:
            dict or str: A dictionary with server info if everything=True, or a specific info string.
                         Returns a dictionary with an error message in case of failure.
        """
        if not selected_server_id:
            return {"error": True, "message": "No server ID provided"}

        async with aiohttp.ClientSession() as session:
            async with session.get(urls["servers"], headers=self._headers, timeout=6) as res1:
                if res1.status != 200:
                    return {"error": True, "status_code": res1.status, "message": await res1.text()}

            async with session.get(f"{urls['servers']}{selected_server_id}", headers=self._headers, timeout=6) as res2:
                if res2.status != 200:
                    return {"error": True, "status_code": res2.status, "message": await res2.text()}
                data = await res2.json()

        server_info = {
            "Identifier": data.get("identifier"),
            "Server ID": selected_server_id,
            "Is suspended?": data.get("suspended"),
            "Server Name": data.get("name"),
            "Coins per month": data.get("plan", {}).get("coinsPerMonth"),
            "Storage": f"{data.get('plan', {}).get('storage', 'Unknown')} MB",
            "Ram": f"{data.get('plan', {}).get('ram', 'Unknown')} MB",
            "CPU": f"{data.get('plan', {}).get('cpu', 'Unknown')}%",
            "Next Renewal": "Unknown"
        }

        next_renewal = data.get("nextRenewal")
        if next_renewal:
            try:
                unix_timestamp = int(''.join(c for c in next_renewal if c.isdigit())) / 1000
                server_info["Next Renewal"] = datetime.fromtimestamp(unix_timestamp, timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
            except ValueError:
                server_info["Next Renewal"] = "Invalid renewal date format"

        if everything:
            return server_info

        if specific_info:
            specific_info = specific_info.lower()
            key_map = {
                "identifier": "Identifier",
                "id": "Server ID",
                "suspended": "Is suspended?",
                "name": "Server Name",
                "coins/month": "Coins per month",
                "storage": "Storage",
                "ram": "Ram",
                "cpu": "CPU",
                "nextrenewal": "Next Renewal"
            }
            return server_info.get(key_map.get(specific_info), {"error": True, "message": "Invalid info key"})

        return {"error": True, "message": "Missing specific_info"}

    async def show(self):
        """
        Shows all your servers
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(urls["servers"], headers=self._headers, timeout=6) as response:
                if response.status == 200:
                    return await response.json()
                return {"error": response.status, "message": await response.text()}
            
    async def delete(self, server_id=None):
        """
        This function gets all your server ids and on your request deletes a certain one (only with your confirmation)
        If server_id is provided, deletes that server directly; otherwise, prompts user for server selection.
        """
        if not server_id:
            return "Value ServerID cannot be None"

        async with aiohttp.ClientSession() as session:
            async with session.post(
                server_urls["delete"],
                json={"id": int(server_id)},
                headers=self._headers,
                timeout=6
            ) as response:
                return await response.text()