# Bot-Hosting.net API Wrapper
Important: Your account token expires every 2 weeks! If something isnt working, make sure you use an up-to-date token :)

A simple API Wrapper for certain information in python for bot-hosting.net
Information: This is made by @vortexsys on discord, staff member but not developer of bot-hosting.net
## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Change Log](#changelog)
- [License](#license)
- [Contribution](#contributing)

## Installation
Dependencies :
- requests
- colorama
- datetime

## Usage
### How to get the Authorization key
Please follow the instructions to get your auth id:
- Login to your account and go to [this page](https://bot-hosting.net/panel/)
- Open your browser's console (usually by pressing F12 or pressing Control + Shift + I)
- Navigate to the 'Console' tab
- Paste in the following code:
```
var token = localStorage.getItem('token');
console.log('Your Auth ID:', token);
```
Now you got your Auth ID and can use all the scripts, congrats!
### Servers Information
Show all Servers and some Information about them:
```
from bot_hosting_wrapper import show_servers

auth_key = "your_authorization_key"
show_servers(auth_key)
```
### Specific Server Information
View general information about a Server:
```
from bot_hosting_wrapper import get_server_info

auth_key = "your_authorization_key"
get_server_info(auth_key)
```
Change your server's Coding Language:
```
from bot_hosting_wrapper import change_language

auth_key = "your_authorization_key"
change_language(auth_key)
//Optionally like this (already including the new coding language)
//change_language(auth_id, language="example") //options: java, python, nodejs, lua, deno, nodemon
```
### Account Information
Getting genuine Account Information:
```
from bot_hosting_wrapper import about_account

auth_key = "your_authorization_key"
about_account(auth_key)
```
Checking if AUTH ID is valid:
```
from bot_hosting_wrapper import id_check 

auth_key = "your-authorization_key"
id_check(auth_key)
```
Getting your current coins amount:
```
from bot_hosting_wrapper import coins_amount
auth_key = "your_authorization_key"
coins_amount(auth_key)
```
## Changelog
- Updated Usage (added id_check, optimised about_account, etc.)
- Tested for optimisation
- Updated/fixed the README file
## License
MIT License

Copyright (c) 2024 Vortex

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Contributing
- Follow these simple steps for contributing via [Github](https://github.com/vortexsys/bot-hosting-wrapper)
- Fork the repository.
- Create a new branch: git checkout -b feature/my-feature.
- Commit your changes: git commit -am 'Add my feature'.
- Push to the branch: git push origin feature/my-feature.
- Submit a pull request.