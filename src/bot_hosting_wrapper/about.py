import webbrowser
import requests
from colorama import Fore
from datetime import datetime, timezone

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

def get_server_info(auth_id):
    def cls():
        print("\033c")

    # Get a list of available servers
    url_list = "https://bot-hosting.net/api/servers"
    headers_list = {
        "Authorization": auth_id
    }

    response_list = requests.get(url_list, headers=headers_list)

    if response_list.status_code == 200:
        server_list = response_list.json()
        print("Available Servers:")

        for index, server_info in enumerate(server_list, start=1):
            print(f"{index}. Server ID: {server_info['serverid']}, Name: {server_info['name']}")

        print("Select your server ID or list number: ")
        # Prompt user to select a server
        selection_input = input("[>]")
        cls()

        try:
            # Try to convert the input to an integer
            selection = int(selection_input)
            selected_server_id = str(server_list[selection - 1]['serverid'])
        except ValueError:
            # If not an integer, assume it's a server ID
            selected_server_id = selection_input

        # Get details for the selected server
        url_details = f"https://bot-hosting.net/api/servers/{selected_server_id}"
        headers_details = {
            "Authorization": auth_id
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

            # Extract numerical part from the strings and convert to int
            renewal_numeric = int(''.join(c for c in data.get("nextRenewal") if c.isdigit()))

            if renewal_numeric:
                unix_timestamp = renewal_numeric / 1000  # Assuming the timestamp is in milliseconds
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

def show_servers(auth_id):
    url = "https://bot-hosting.net/api/servers"
    headers = {
        "Authorization": auth_id
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

def show_coins(auth_id):
    url = "https://bot-hosting.net/api/me"
    headers = {
        "Authorization": auth_id
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
    
def about_account(auth_id):
    url = "https://bot-hosting.net/api/me"
    headers = {
        "Authorization": auth_id
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        user_info = response.json()
        print("Request successful!")
        print("Username: ", user_info['username'], " | ID: ", user_info['id'])
        print("Current coins amount:", user_info['coins'])
        print("Avatar:", user_info['avatar'])
        input("Press enter to continue")
    else:
        print(f"Error: {response.status_code}")
        print("Response:")
        print(response.text)