# Bot-Hosting.net API Wrapper

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contribution](#contributing)
- [License](#license)

## Installation
Dependencies :
- requests
- colorama
- datetime

## Usage
### Servers Information
```from bot_hosting_wrapper_vortexsys import show_servers

auth_key = "your_authorization_key"
show_servers(auth_key)
### Specific Server Information
```from bot_hosting_wrapper_vortexsys import show_servers

auth_key = "your_authorization_key"
get_server_info(auth_key)
### Account Information
```from bot_hosting_wrapper_vortexsys import about_account

auth_key = "your_authorization_key"
about_account(auth_key)

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