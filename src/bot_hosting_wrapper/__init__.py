############# bot-hosting-wrapper files
from .about import *
from .interactive import *
from .panel import *
from .vasync import *
############# bot-hosting-wrapper files
import asyncio
import webbrowser

############# Functions

def get_auth_id_sync() -> None:
    """
    Recently renamed from get_auth_id to get_auth_id_sync
    Prints a quick instruction on how to get the auth id
    Returns:
        None
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

async def get_auth_id_async():
    """
    Async version for get_auth_id_sync
    """
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, get_auth_id_sync)