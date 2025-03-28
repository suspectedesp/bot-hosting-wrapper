# Bot Hosting Wrapper
A simple yet powerful Python wrapper for bot-hosting.net's API

# 🚀Information
As of 20/01/2025, this library can only be used from bot-hosting.net's nodes. If you try to access it from elsewhere, Cloudflare will block your request with a 403 error.

⚠️ Important: Your account token expires every 2 weeks! If something isn't working, double-check that you're using an up-to-date Auth ID.

This is maintained by @suspectedesp on Github

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Change Log](#changelog)
- [License](#license)
- [Contribution](#contributing)
- [Credits](#credits)

## Installation
Dependencies | Make sure you have the following installed (+ used version in development):
```txt
requests==2.31.0
colorama==0.4.6
datetime==5.4
```
Install using pip:
```txt
pip install requests colorama datetime
```
## Usage
### Retrieving your Authorization key
Please follow the instructions to get your auth id:
- Login to your account and go to [this page](https://bot-hosting.net/panel/)
- Open your browser's console (usually by pressing F12 or pressing Control + Shift + I)
- Navigate to the 'Console' tab
- Paste in the following code:
```js
var token = localStorage.getItem('token');
console.log('Your Auth ID:', token);
```
Your Auth ID will now be displayed in the console and can use the module, congrats!

🔹 For a full list of commands and usage examples, check out the [Wiki](https://github.com/suspectedesp/bot-hosting-wrapper/wiki/Coding-Usage)

## Changelog
📢 Stay up to date with the latest changes! Find the latest release notes under the [Releases tab](https://github.com/suspectedesp/bot-hosting-wrapper/releases).

## License
MIT License

Copyright (c) 2024-2025 @suspectedesp on Github

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
- Follow these simple steps for contributing via [Github](https://github.com/suspectedesp/bot-hosting-wrapper)
- Fork the repository.
- Create a new branch: git checkout -b feature/my-feature.
- Commit your changes: git commit -am 'Add my feature'.
- Push to the branch: git push origin feature/my-feature.
- Submit a pull request.

## 💖Credits
Many thanks to:
- @mathiasDPX for giving me some ideas and remaking the code
- @pondwader for letting me upload this
- @Aidan-The-Dev for the useful PR

Thank you all! Your contributions mean a lot, I appreciate it <3
