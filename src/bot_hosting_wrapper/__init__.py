############# bot-hosting-wrapper files
from .about import *
from .interactive import *
from .panel import *
from .vasync import *
############# bot-hosting-wrapper files
import webbrowser

############# Functions

def get_auth_id() -> None:
    """
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