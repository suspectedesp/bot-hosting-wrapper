```python
from bot-hosting-wrapper import Account, Server, Interactive

def main() -> None:
    auth_id = input("Enter your auth id: ")
    acc = Account(auth_id)
    serv = Server(auth_id)
    #interactive includes console/input required stuff like the old version did
    interactive = Interactive(auth_id)
    interactive.get_info()

    # Delete a specific server by ID
    # serv.delete("serverid") # Uncomment and replace "serverid" with the actual server ID if needed
    # show all servers
    serv.show()
    # Get specific information about a server (example: next renewal date)
    server_info = serv.get_info(everything=False, specific_info="nextrenewal", selected_server_id="serverid")
    print(server_info)
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
```