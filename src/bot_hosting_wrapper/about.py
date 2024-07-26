import webbrowser
from datetime import datetime, timezone
import os
import requests
from colorama import Fore

urls = {
    "servers": "https://bot-hosting.net/api/servers/",
    "affiliate": "https://bot-hosting.net/api/affiliate",
    "newPassword": "https://bot-hosting.net/api/newPassword",
    "freeCoinsStatus": "https://bot-hosting.net/api/freeCoinsStatus"
}


class Account:
    def __init__(self, auth_id):
        self.auth_id = auth_id
        self._headers = {
            "Authorization": self.auth_id,
            "content-type": "application/json"
        }

    @staticmethod
    def get_auth_id():
        """A quick instruction on how to get the auth id
        """
        print(Fore.WHITE + "Please follow the instructions to get your auth id.")
        print("1. Open your browser's console (usually by pressing F12 or pressing Control + Shift + I)")
        print("2. Navigate to the 'Console' tab")
        print("3. Paste in the following code:")
        print(Fore.CYAN + """var token = localStorage.getItem('token');
console.log('Your Auth ID:', token);
          """)
        print(Fore.WHITE + "Now you got your Auth ID and can use all the scripts, congrats!")

        input("Pressing Enter will open the link where you can do all that :)")
        link_to_open = "https://bot-hosting.net/panel/"
        webbrowser.open(link_to_open)
        return

    def coins_amount(self):
        """
        Will show you the total amount of your coins
        """
        url = "https://bot-hosting.net/api/me"

        response = requests.get(url, headers=self._headers)

        if response.status_code == 200:
            coins_amount = response.json().get('coins')
            return coins_amount
        else:
            print(f"Error: {response.status_code}")
            print(response.text)

    def affiliate_data(self):
        """
        Return your affiliate data (coins/referral, uses and your link)
        """

        data = requests.get(urls["affiliate"], headers=self._headers).json()

        class AffiliateData:
            coinsPerReferral = data["coinsPerReferral"]
            enabled = data["enabled"]
            link = data["link"]
            uses = data["uses"]

        return AffiliateData

    def about(self):
        """
        Will give you a quick overview over your account
        """
        url = "https://bot-hosting.net/api/me"

        response = requests.get(url, headers=self._headers)

        if response.status_code == 200:
            try:
                user_info = response.json()
                print("Sent Request!")
                print("Username: ", user_info['username'], " | ID: ", user_info['id'])
                print("Current coins amount:", user_info['coins'])
                print("Avatar:", user_info['avatar'])
            except Exception as e:
                print(f"Error parsing response JSON: {e}")
                print("auth_id invalid")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)

    def id_check(self, about=None):
        """
        Checks if your Auth ID is valid
        """
        url = "https://bot-hosting.net/api/me"

        response = requests.get(url, headers=self._headers)

        if response.status_code == 200:
            try:
                user_info = response.json()
                if about is not None:
                    if about:
                        print("Username: ", user_info['username'], " | ID: ", user_info['id'])
                return "Auth ID is valid."
            except Exception as e:
                print(f"Error parsing response JSON: {e}")
                print("Auth ID is most likely invalid.")
        else:
            print("Auth_id is not valid. Please check your authentication credentials.")

    def sftp_pass(self):
        """
        This will generate a new SFTP password
        """
        password = requests.post(urls["newPassword"], headers=self._headers).json()["password"]
        return password

    def claimable(self):
        """
        Check if free coins are claimable and the time left
        """
        response = requests.get(urls["freeCoinsStatus"], headers=self._headers)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "claimable": data["claimable"],
                "timeLeft": data["timeLeft"]
            }
        else:
            print(f"Error: {response.status_code}")
            print(response.text)


class Server:
    def __init__(self, auth_id):
        self.auth_id = auth_id
        self._headers = {
            "Authorization": self.auth_id,
            "content-type": "application/json"
        }

    def change_language(self, language=None, server_id: str = None):
        """Gets all your servers, lets you select one, after that you select a language, and it'll change the server to that
        """
        url_list = "https://bot-hosting.net/api/servers"

        response_list = requests.get(url_list, headers=self._headers)

        if response_list.status_code == 200:

            if server_id is None:
                return print("Error at change_language: You must enter a server ID!")

            if language is None:
                return print("Error at change_language: You must enter a programming language!")  # (java, python, nodejs, lua, deno, nodemon)
            else:
                programming_language = language
                language_to_egg = {
                    "nodejs": 16,
                    "python": 17,
                    "java": 18,
                    "deno": 19,
                    "nodemon": 20,
                    "lua": 21
                }

            egg = language_to_egg.get(programming_language.lower(), "Unknown Language")
            # print(f"Selected server ID: {selected_server_id}, Programming Language: {programming_language}, Egg: {egg}")
            change_software_url = f"{urls['servers']}/changeSoftware"
            payload_change_software = {
                "id": server_id,
                "egg": str(egg)
            }

            response_change_software = requests.post(change_software_url, headers=self._headers,
                                                     json=payload_change_software)

            if response_change_software.status_code == 200:
                return "Software change request successful!"
            else:
                print(f"Failed to change software. Status code: {response_change_software.status_code}")
                print(response_change_software.text)

    def get_info(self, specific_info=None, everything=None, selected_server_id: str = None):
        """
        First gets all your servers, then you can select a certain one, and it shows you the specific info about it\n
        Such as: Renewal, Identifier, Server ID, if its suspended, etc.\n
        Example Usage of Params: specific_info="cpu" or all=True\n
        specific info can either be name | id | identifier | coins/month | suspended | ram | storage | cpu | nextrenewal
        """
        renewal_numeric = None
        url_list = "https://bot-hosting.net/api/servers"

        response_list = requests.get(url_list, headers=self._headers)

        if response_list.status_code == 200:

            url_details = f"{urls['servers']}{selected_server_id}"

            response_details = requests.get(url_details, headers=self._headers)

            if response_details.status_code == 200:
                data = response_details.json()

                identifier = data.get("identifier")
                suspended = data.get("suspended")
                name = data.get("name")
                coins_per_month = data.get("plan", {}).get("coinsPerMonth")
                storage = data.get("plan", {}).get("storage")
                ram = data.get("plan", {}).get("ram")
                cpu = data.get("plan", {}).get("cpu")

                next_renewal = data.get("nextRenewal")

                if next_renewal is not None:
                    renewal_date_first = next_renewal
                    renewal_numeric = int(''.join(c for c in renewal_date_first if c.isdigit()))
                else:
                    print(response_details.json())

                if next_renewal is not None:
                    unix_timestamp = renewal_numeric / 1000
                    renewal_date = datetime.fromtimestamp(unix_timestamp, timezone.utc).strftime(
                        '%Y-%m-%d %H:%M:%S UTC')

                    if everything:
                        server_info = {
                            "Identifier": identifier,
                            "Server ID": selected_server_id,
                            "Is suspended?": suspended,
                            "Server Name": name,
                            "Coins per month": coins_per_month,
                            "Storage": f"{storage} MB",
                            "Ram": f"{ram} MB",
                            "CPU": f"{cpu}%",
                            "Next Renewal": renewal_date
                        }
                        return server_info
                    else:
                        if specific_info is None:
                            return print(
                                "Error! Specific Info cannot be None while all is False | Function used: get_info")
                        else:
                            if specific_info.lower() == "identifier":
                                return identifier
                            elif specific_info.lower() == "id":
                                return selected_server_id
                            elif specific_info.lower() == "suspended":
                                return suspended
                            elif specific_info.lower() == "name":
                                return name
                            elif specific_info.lower() == "coins/month":
                                return coins_per_month
                            elif specific_info.lower() == "storage":
                                return f"{storage} MB"
                            elif specific_info.lower() == "ram":
                                return f"{ram} MB"
                            elif specific_info.lower() == "cpu":
                                return f"{cpu}%"
                            elif specific_info.lower() == "nextrenewal":
                                return renewal_date
                            else:
                                return print("Error! Invalid specific_info value provided.")
                else:
                    if everything:
                        server_info = {
                            "Identifier": identifier,
                            "Server ID": selected_server_id,
                            "Is suspended?": suspended,
                            "Server Name": name,
                            "Coins per month": coins_per_month,
                            "Storage": f"{storage} MB",
                            "Ram": f"{ram} MB",
                            "CPU": f"{cpu}%",
                            "Next Renewal": "NoneType Error"
                        }
                        return server_info
                    else:
                        if specific_info is None:
                            return print(
                                "Error! Specific Info cannot be None while all is False | Function used: get_info")
                        else:
                            if specific_info == "Identifier":
                                return identifier
                            elif specific_info == "Server ID":
                                return selected_server_id
                            elif specific_info == "Is suspended?":
                                return suspended
                            elif specific_info == "Server Name":
                                return name
                            elif specific_info == "Coins per month":
                                return coins_per_month
                            elif specific_info == "Storage":
                                return f"{storage} MB"
                            elif specific_info == "Ram":
                                return f"{ram} MB"
                            elif specific_info == "CPU":
                                return f"{cpu}%"
                            elif specific_info == "Next Renewal":
                                if next_renewal is not None:
                                    unix_timestamp = renewal_numeric / 1000
                                    renewal_date = datetime.fromtimestamp(unix_timestamp, timezone.utc).strftime(
                                        '%Y-%m-%d %H:%M:%S UTC')
                                else:
                                    renewal_date = "Error Getting Renewal Date: Renewal Date = None"
                                return renewal_date
                            else:
                                return print("Error! Invalid specific_info value provided.")
            else:
                print(f"Error: {response_details.status_code}")
                print(response_details.text)

        else:
            print(f"Error: {response_list.status_code}")
            print(response_list.text)

    def show(self):
        """Shows all your servers
        """
        url = "https://bot-hosting.net/api/servers"

        response = requests.get(url, headers=self._headers)

        if response.status_code == 200:
            print("Request successful!")
            responsee = response.json()
            return responsee
        else:
            print(f"Error: {response.status_code}")
            print(response.text)

    def delete(self, server_id=None):
        """
        This function gets all your server ids and on your request deletes a certain one (only with your confirmation)
        If server_id is provided, deletes that server directly; otherwise, prompts user for server selection.
        """
        url_list = "https://bot-hosting.net/api/servers"

        response_list = requests.get(url_list, headers=self._headers)

        if response_list.status_code == 200:

            if server_id is None:
                return "Value ServerID cannot be None"
            else:
                selected_server_id = str(server_id)

            url_delete = "https://bot-hosting.net/api/servers/delete"

            data = {
                "id": int(selected_server_id)
            }

            r = requests.post(url_delete, json=data, headers=self._headers)
            return r.content

class Interactive:
    def __init__(self, auth_id):
        self.auth_id = auth_id
        self._headers = {
            "Authorization": self.auth_id,
            "content-type": "application/json"
        }
    
    def cls(self):
        os.system('cls' if os.name=='nt' else 'clear')

    def get_info(self):
        """
        First gets all your servers, then you can select a certain one and it shows you the specific info about it
        Such as: Renewal, Identifier, Server ID, if its suspended, etc.
        """
        url_list = "https://bot-hosting.net/api/servers"

        response_list = requests.get(url_list, headers=self._headers)

        if response_list.status_code == 200:
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

            response_details = requests.get(url_details, headers=self._headers)

            if response_details.status_code == 200:
                data = response_details.json()

                identifier = data.get("identifier")
                suspended = data.get("suspended")
                name = data.get("name")
                coins_per_month = data.get("plan", {}).get("coinsPerMonth")
                storage = data.get("plan", {}).get("storage")
                ram = data.get("plan", {}).get("ram")
                cpu = data.get("plan", {}).get("cpu")

                next_renewal = data.get("nextRenewal")
                if next_renewal:
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
                else:
                    print("Error: 'nextRenewal' is missing or None")
            else:
                print(f"Error: {response_details.status_code}")
                print("Response:")
                print(response_details.text)

        else:
            print(f"Error: {response_list.status_code}")
            print("Response:")
            print(response_list.text)