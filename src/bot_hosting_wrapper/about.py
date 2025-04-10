import requests

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
    "changeSoftware": "https://bot-hosting.net/api/servers/changeSoftware",
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

    def coins_amount(self) -> (Any | dict[str, str] | str):
        """
        Gets the total amount of your coins.
        Returns:
            The coin amount
            or a dictionary with an error message and status code if the request failed. {Error, Message}
        """

        try:
            response = requests.get(urls["me"], headers=self._headers, timeout=6)
            if response.status_code == 200:
                coins_amount = response.json().get('coins', None)  # defaulting to 0 if 'coins' key is missing
                return coins_amount
            else:
                return {"Error": f"Received status code {response.status_code} from API.", "Message": response.text}
        except requests.exceptions.RequestException as e:
            return f"Request failed: {e}"

    def affiliate_data(self)-> (dict[str, Any] | str):
        """
        Returns affiliate data (coins/referral, uses and your link)
        Returns:
            If status code is 200 and no error occurs: a dict containing {coinsPerReferral, enabled, link, uses}
            If status code is not 200: an error dict containing {Error, Message}
        """
        try:
            data = requests.get(urls["affiliate"], headers=self._headers, timeout=6).json()
            if data.status_code != 200:
                return {"Error": f"Received status code {data.status_code} from API.", "Message": data.text}
        except requests.exceptions.RequestException as e:
            return f"Request failed: {e}"

        AffiliateData = {
            "coinsPerReferral": data["coinsPerReferral"],
            "enabled": data["enabled"],
            "link": data["link"],
            "uses": data["uses"],
        }
        return AffiliateData

    def about(self):
        """
        Will give you a quick overview of your account.
        Returns:
            A dictionary with account details or an 'error' message if something goes wrong.
        """

        response = requests.get(urls["me"], headers=self._headers, timeout=6)

        if response.status_code == 200:
            try:
                user_info = response.json()
                return {
                    "username": user_info.get('username', 'Unknown'),
                    "id": user_info.get('id', 'Unknown'),
                    "coins": user_info.get('coins', 'Unknown'),
                    "avatar": user_info.get('avatar', 'No Avatar')
                }
            except ValueError as e:
                return {"error": f"Error parsing response JSON: {e}"}
        else:
            return {"error": f"Received status code {response.status_code} from API: {response.text}"}

    def id_check(self, about=False):
        """
        Checks if your Auth ID is valid.
        Params:
        about (bool): If True, print user info in the console. Default is False.
        """
        success = False
        try:
            response = requests.get(urls["me"], headers=self._headers, timeout=6)
            if response.status_code == 200:
                try:
                    success = True
                    user_info = response.json()

                    # print user info if requested
                    if about:
                        print("Username:", user_info.get('username', 'Unknown'), "| ID:", user_info.get('id', 'Unknown'))
                except ValueError as e:
                    return "Error parsing response. Auth ID is most likely invalid: {e}"
            return {"Success": success, "Status Code": response.status_code}
        
        except requests.exceptions.RequestException as e:
            return "Failed to contact the API. Please check your internet connection or the API URL: {e}"
        
    def sftp_pass(self):
        """
        This will generate a new SFTP password
        Returns:
            The new SFTP password
        """
        password = requests.post(urls["newPassword"], headers=self._headers, timeout=6).json()["password"]
        return password

    def claimable(self):
        """
        Check if free coins are claimable and the time left
        Returns:
            A dict containing {claimable, timeLeft}
        """
        response = requests.get(urls["freeCoinsStatus"], headers=self._headers, timeout=6)

        if response.status_code == 200:
            data = response.json()
            return {
                "claimable": data["claimable"],
                "timeLeft": data["timeLeft"]
            }
        else:
            return {"Status-Code": f"{response.status_code} from API.", "Message": response.text}



class Server:
    def __init__(self, auth_id):
        self.auth_id = auth_id
        self._headers = {
            "Authorization": self.auth_id,
            "content-type": "application/json"
        }

    def change_language(self, language=None, server_id: str = None):
        """
        Changes the programming language of a specified server.

        Params:
            language (str, required): The programming language to switch to (java, python, nodejs, lua, deno, nodemon).
            server_id (str, required): The server ID.

        Returns:
            dict: Success or error message.
        """
        if not server_id:
            return {"error": True, "message": "Error at change_language: You must enter a server ID!"}

        if not language:
            return {"error": True, "message": "Error at change_language: You must enter a programming language!"}

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
            return {"error": True, "message": f"Invalid programming language: {language}. Supported: {', '.join(language_to_egg.keys())}"}

        # constructing api request
        payload_change_software = {
            "id": server_id,
            "egg": str(egg)
        }

        response = requests.post(server_urls["changeSoftware"], headers=self._headers, json=payload_change_software, timeout=6)

        if response.status_code == 200:
            return {"success": True, "message": "Software change request successful!"}
        else:
            return {"error": True, "status_code": response.status_code, "message": response.text}

    def get_info(self, specific_info=None, everything=False, selected_server_id: str = None) -> dict | str:
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

        response_list = requests.get(urls["servers"], headers=self._headers, timeout=6)
        if response_list.status_code != 200:
            return {"error": True, "status_code": response_list.status_code, "message": response_list.text}

        if not selected_server_id:
            return {"error": True, "message": "Error! No server ID provided."}

        response_details = requests.get(f"{urls['servers']}{selected_server_id}", headers=self._headers, timeout=6)

        if response_details.status_code != 200:
            return {"error": True, "status_code": response_details.status_code, "message": response_details.text}

        data = response_details.json()

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
                renewal_numeric = int(''.join(c for c in next_renewal if c.isdigit()))
                unix_timestamp = renewal_numeric / 1000
                server_info["Next Renewal"] = datetime.fromtimestamp(unix_timestamp, timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
            except ValueError:
                server_info["Next Renewal"] = "Error: Invalid renewal date format"

        # returning full server info if needed
        if everything:
            return server_info

        # else returning specific info
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

            if specific_info in key_map:
                return server_info[key_map[specific_info]]
            else:
                return {"error": True, "message": f"Error! Invalid specific_info value: {specific_info}"}

        return {"error": True, "message": "Error! specific_info cannot be None when everything=False"}

    def show(self):
        """
        Shows all your servers
        Returns:
            The whole response parsed as a json dict
            If response isn't 200, it returns an error dict
        """

        response = requests.get(urls["servers"], headers=self._headers, timeout=6)

        if response.status_code == 200:
            response = response.json()
            return response
            # TODO: check if it works correctly
        else:
            return {"error": response.status_code, "message": response.text}

    def delete(self, server_id: int):
        """
        This function gets all your server ids and on your request deletes a certain one (only with your confirmation)
        Returns:
            If server id provided: response content
        """

        if server_id is None:
            return "Value ServerID cannot be None"

        data = {
            "id": int(server_id)
        }

        r = requests.post(server_urls["delete"], json=data, headers=self._headers, timeout=6)
        return r.content
