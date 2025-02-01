import bot_hosting_wrapper
from bot_hosting_wrapper import Account, Server, Interactive, Panel

def main() -> None:
    bot_hosting_wrapper.LOGGING_ENABLED = False
    auth_id = input("Enter your auth id: ")
    api_key = input("Enter your API key for Panel: ") # https://control.bot-hosting.net/account/api
    acc = Account(auth_id)
    serv = Server(auth_id)
    server_id = 123
    panel = Panel(api_key, server_id) # server_id is optional 
    #interactive includes console/input required stuff like the old version did
    interactive = Interactive(auth_id)
    interactive.get_info()
    server_identifier = input("\nEnter server name or identifier to get UUID: ")
    server_uuid = panel.get_server_uuid(identifier=server_identifier) or panel.get_server_uuid(name=server_identifier)
    print(f"UUID for {server_identifier}: {server_uuid}")
    # Delete a specific server by ID
    # serv.delete("serverid") # Uncomment and replace "serverid" with the actual server ID if needed
    # show all servers
    serv.show()
    # Get specific information about a server (example: next renewal date)
    server_info = serv.get_info(everything=False, specific_info="nextrenewal", selected_server_id="serverid")
    print(server_info)
    
    info = Server.get_info(everything=True, selected_server_id="12345")
    print(info)

    # Get only the server's CPU usage
    cpu = Server.get_info(specific_info="cpu", selected_server_id="12345")
    print(cpu)

    # Handle errors properly
    response = Server.get_info(specific_info="invalid_key", selected_server_id="12345")
    if "error" in response:
        print(f"Error: {response['message']}")
    # Get current coins amount
    acc.coins_amount()
    # Get account overview
    acc.about()
    # Check if AUTH ID is valid
    valid_auth = acc.id_check()
    print(valid_auth)    
    # Generate a new SFTP password (careful, this resets the SFTP password)
    # acc.sftp_pass()    
    # Change server's coding language (example: change to Python)
    # serv.change_language(language="python") # Uncomment if needed    
    # Get affiliate data
    affiliate_data = acc.affiliate_data()
    print("Coins per referral:", affiliate_data.coinsPerReferral)
    print("Enabled:", affiliate_data.enabled)
    print("Link:", affiliate_data.link)
    print("Number of uses:", affiliate_data.uses)
main()