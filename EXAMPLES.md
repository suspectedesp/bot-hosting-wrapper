```py
from bot-hosting-wrapper import Account, Server

def main() -> None:
    auth_id = input("Enter your auth id")
    acc = Account(auth_id)
    serv = Server(auth_id)
    #serv.delete() # you can also do just serv.delete("serverid")
    serv.show()
    server_info = serv.get_info(all=False, specific_info="nextrenewal")
    print(server_info)
    acc.coins_amount()
    acc.about()
    valid_auth = acc.id_check()
    print(valid_auth)
    # acc.sftp_pass() # careful, this resets the sftp password
    # serv.change_language(language="python") # you can also do just serv.change_language()
    affiliate_data = acc.affiliate_data()
    print("Coins per referral:", affiliate_data.coinsPerReferral)
    print("Enabled:", affiliate_data.enabled)
    print("Link:", affiliate_data.link)
    print("Number of uses:", affiliate_data.uses)
main()
```