# Bot Hosting Wrapper
[![PyPI Downloads](https://static.pepy.tech/badge/bot-hosting-wrapper)](https://pepy.tech/projects/bot-hosting-wrapper)

A simple yet powerful Python wrapper for bot-hosting.net's API 

# 🚀Information
As of 20/01/2025, this library can only be used from bot-hosting.net's nodes. If you try to access it from elsewhere, Cloudflare will block your request with a 403 error.

⚠️ Important: Your account token expires every 2 weeks! If something isn't working, double-check that you're using an up-to-date Auth ID.

This is maintained by @suspectedesp on Github

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Change Log](#changelog)
- [Wiki](#wiki)
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

## Wiki
Need function documentation, known issues or coding usage? Check out the wiki under the [Wiki tab](https://github.com/suspectedesp/bot-hosting-wrapper/wiki)

## License
The Unlicense

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org>

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
