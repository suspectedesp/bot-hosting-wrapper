import os
import webbrowser
import requests
import time
from colorama import Fore
from datetime import datetime, timezone

urls = {
    "servers": "https://bot-hosting.net/api/servers/",
    "affiliate": "https://bot-hosting.net/api/affiliate",
    "newPassword": "https://bot-hosting.net/api/newPassword"
}

class Account:
    def __init__(self, auth_id):
        self.auth_id = auth_id

    def get_auth_id():
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

    def coins_amount(self):
        url = "https://bot-hosting.net/api/me"
        headers = {
            "Authorization": self.auth_id
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            print("Request successful!")
            coins_amount = response.json().get('coins')
            print("Your current coins amount:", coins_amount)
            input("Press enter to continue")
        else:
            print(f"Error: {response.status_code}")
            print("Response:")
            print(response.text)
    
    def about(self):
        url = "https://bot-hosting.net/api/me"
        headers = {
            "Authorization": self.auth_id
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            try:
                user_info = response.json()
                print("Sent Request!")
                print("Username: ", user_info['username'], " | ID: ", user_info['id'])
                print("Current coins amount:", user_info['coins'])
                print("Avatar:", user_info['avatar'])
                input("Press enter to continue")
            except Exception as e:
                print(f"Error parsing response JSON: {e}")
                print("auth_id invalid")
        else:
            print(f"Error: {response.status_code}")
            print("Response:")
            print(response.text)

    def id_check(self):
        url = "https://bot-hosting.net/api/me"
        headers = {
            "Authorization": self.auth_id
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            try:
                user_info = response.json()
                print("Sent Request!")
                print("Username: ", user_info['username'], " | ID: ", user_info['id'])
                print("Current coins amount:", user_info['coins'])
                print("Avatar:", user_info['avatar'])
                input("Press enter to continue")
            except Exception as e:
                print(f"Error parsing response JSON: {e}")
                print("Auth ID invalid.")
        else:
            print("Auth_id is not valid. Please check your authentication credentials.")
    
    def sftp_pass(self):
        i = input("Information: This resets your old one, are you sure? (yes/no)")
        if i == "yes":
            passwd = requests.post(urls["newPassword"], headers=self._headers).json()["password"]
            input(f"New Password: {passwd}  | Press Enter to continue")
        elif i == "no":
            print("Exiting then!")
            time.sleep(0.)
            exit()

class Server:
    def __init__(self, auth_id):
        self.auth_id = auth_id
    
    def cls(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
            
    def change_language(self, language=None):
        def cls():
            print("\033c")
        url_list = "https://bot-hosting.net/api/servers"
        headers_list = {
            "Authorization": self.auth_id
        }

        response_list = requests.get(url_list, headers=headers_list)

        if response_list.status_code == 200:
            server_list = response_list.json()
            print("Available Servers:")

            for index, server_info in enumerate(server_list, start=1):
                print(f"{index}. Server ID: {server_info['serverid']}, Name: {server_info['name']}")

            print("Select your server ID or list number: ")
            selection_input = input("[>]")
            cls()

            try:
                selection = int(selection_input)
                selected_server_id = str(server_list[selection - 1]['serverid'])
            except ValueError:
                selected_server_id = selection_input

            if language is None:
                programming_language = input("Enter the programming language (java, python, nodejs, lua, deno, nodemon): ")
            else:
                programming_language = language
            language_to_egg = {
                "java": 18,
                "python": 17,
                "nodejs": 16,
                "lua": 21,
                "deno": 19,
                "nodemon": 20
            }

            egg = language_to_egg.get(programming_language.lower(), "Unknown Language")
            print(f"Selected server ID: {selected_server_id}, Programming Language: {programming_language}, Egg: {egg}")
            change_software_url = f"{urls['servers']}/changeSoftware"
            headers_change_software = {
                "Authorization": self.auth_id,
                "Content-Type": "application/json"
            }
            payload_change_software = {
                "id": selected_server_id,
                "egg": str(egg)
            }

            response_change_software = requests.post(change_software_url, headers=headers_change_software, json=payload_change_software)

            if response_change_software.status_code == 200:
                print("Software change request successful!")
            else:
                print(f"Failed to change software. Status code: {response_change_software.status_code}")
                print(response_change_software.text)

    def get_info(self):
        def cls():
            print("\033c")

        url_list = "https://bot-hosting.net/api/servers"
        headers_list = {
            "Authorization": self.auth_id
        }

        response_list = requests.get(url_list, headers=headers_list)

        if response_list.status_code == 200:
            server_list = response_list.json()
            print("Available Servers:")

            for index, server_info in enumerate(server_list, start=1):
                print(f"{index}. Server ID: {server_info['serverid']}, Name: {server_info['name']}")

            print("Select your server ID or list number: ")
            selection_input = input("[>]")
            cls()

            try:
                selection = int(selection_input)
                selected_server_id = str(server_list[selection - 1]['serverid'])
            except ValueError:
                selected_server_id = selection_input

            url_details = f"{urls['servers']}/{selected_server_id}"
            headers_details = {
                "Authorization": self.auth_id
            }

            response_details = requests.get(url_details, headers=headers_details)

            if response_details.status_code == 200:
                data = response_details.json()

                identifier = data.get("identifier")
                suspended = data.get("suspended")
                name = data.get("name")
                coins_per_month = data.get("plan", {}).get("coinsPerMonth")
                storage = data.get("plan", {}).get("storage")
                ram = data.get("plan", {}).get("ram")
                cpu = data.get("plan", {}).get("cpu")

                renewal_numeric = int(''.join(c for c in data.get("nextRenewal") if c.isdigit()))

                if renewal_numeric:
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
                    input("Press enter to continue")
                else:
                    print("Error: Could not extract numeric values from nextRenewal")
            else:
                print(f"Error: {response_details.status_code}")
                print("Response:")
                print(response_details.text)

        else:
            print(f"Error: {response_list.status_code}")
            print("Response:")
            print(response_list.text)

    def show(self):
        url = "https://bot-hosting.net/api/servers"
        headers = {
            "Authorization": self.auth_id
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            print("Request successful!")
            print("Response:")
            print(response.json())
            input("Press enter to continue")
        else:
            print(f"Error: {response.status_code}")
            print("Response:")
            print(response.text)

    def delete(self):
        url_list = "https://bot-hosting.net/api/servers"
        headers_list = {
            "Authorization": self.auth_id
        }

        response_list = requests.get(url_list, headers=headers_list)

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
                

                url_delete = "https://bot-hosting.net/api/servers/delete"
                headers = {
                    "Authorization": self.auth_id,
                    "content-type": "application/json"
                }

                data = {
                    "id": int(selected_server_id)
                }

                r = requests.post(url_delete, json=data, headers=headers)
                print(r.content)

            except (ValueError, IndexError):
                print("Invalid selection. Please choose a valid server.")