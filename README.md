<div><a href='https://github.com/darideveloper/twitch-viwer-bot/blob/master/LICENSE' target='_blank'>
            <img src='https://img.shields.io/github/license/darideveloper/twitch-viwer-bot.svg?style=for-the-badge' alt='MIT License' height='30px'/>
        </a><a href='https://www.linkedin.com/in/francisco-dari-hernandez-6456b6181/' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=LinkedIn&color=0A66C2&logo=LinkedIn&logoColor=FFFFFF&label=' alt='Linkedin' height='30px'/>
            </a><a href='https://t.me/darideveloper' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Telegram&color=26A5E4&logo=Telegram&logoColor=FFFFFF&label=' alt='Telegram' height='30px'/>
            </a><a href='https://github.com/darideveloper' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=GitHub&color=181717&logo=GitHub&logoColor=FFFFFF&label=' alt='Github' height='30px'/>
            </a><a href='https://www.fiverr.com/darideveloper?up_rollout=true' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Fiverr&color=222222&logo=Fiverr&logoColor=1DBF73&label=' alt='Fiverr' height='30px'/>
            </a><a href='https://discord.com/users/992019836811083826' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Discord&color=5865F2&logo=Discord&logoColor=FFFFFF&label=' alt='Discord' height='30px'/>
            </a><a href='mailto:darideveloper@gmail.com?subject=Hello Dari Developer' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Gmail&color=EA4335&logo=Gmail&logoColor=FFFFFF&label=' alt='Gmail' height='30px'/>
            </a></div><div align='center'><br><br><img src='https://github.com/darideveloper/twitch-viwer-bot/blob/master/logo.png?raw=true' alt='Twitch Viwer Bot' height='80px'/>

# Twitch Viwer Bot

Python project who allow you to manage bots to comment and watch streams.

Project type: **client**

</div><br><details>
            <summary>Table of Contents</summary>
            <ol>
<li><a href='#buildwith'>Build With</a></li>
<li><a href='#relatedprojects'>Related Projects</a></li>
<li><a href='#media'>Media</a></li>
<li><a href='#details'>Details</a></li>
<li><a href='#roadmap'>Roadmap</a></li></ol>
        </details><br>

# Build with

<div align='center'><a href='https://www.python.org/' target='_blank'> <img src='https://cdn.svgporn.com/logos/python.svg' alt='Python' title='Python' height='50px'/> </a><a href='https://requests.readthedocs.io/en/latest/' target='_blank'> <img src='https://requests.readthedocs.io/en/latest/_static/requests-sidebar.png' alt='Requests' title='Requests' height='50px'/> </a><a href='https://www.selenium.dev/' target='_blank'> <img src='https://cdn.svgporn.com/logos/selenium.svg' alt='Selenium' title='Selenium' height='50px'/> </a></div>

# Related projects

<div align='center'><a href='https://github.com/darideveloper/comunidad-mc' target='_blank'> <img src='https://github.com/darideveloper/comunidad-mc/blob/master/app/static/app/imgs/logo_white.png?raw=true' alt='Comunidad MC' title='Comunidad MC' height='50px'/> </a><a href='https://github.com/darideveloper/twitch-cheer-bot' target='_blank'> <img src='https://github.com/darideveloper/twitch-cheer-bot/blob/master/logo.png?raw=true' alt='Twitch Cheer Bot' title='Twitch Cheer Bot' height='50px'/> </a><a href='https://github.com/darideveloper/twitch-cookies-getter' target='_blank'> <img src='https://github.com/darideveloper/twitch-cookies-getter/blob/master/logo.png?raw=true' alt='Twitch Cookies Getter' title='Twitch Cookies Getter' height='50px'/> </a></div>

# Media

![terminal](https://github.com/darideveloper/twitch-viwer-bot/blob/master/images/terminal.PNG?raw=true)

# Details

The bot manage multiple chrome windows for manage bots. 
It don't login with the accounts, instead of that, the bot use cookies already saved in a Backend service. 
All information required, like users, streams to watch, comments, donations, etc; its provided from a Django private app backend.

## Features

* Login with cookies
* Use proxies
* Watch streams during a specific time
* Comment streams (coming soon)

# Roadmap

- [x] Use cookies to avoid login
- [x] Run multiple bots with multithreading
- [x] Get data from backend
- [x] Show counters of bots running
- [x] Detect no streams found (no streams provided from the backend)
- [x] Detect no live streams
- [x] Detect no more active bots available
- [x] Detect proxy errors
- [x] Detect cookies errors
- [x] Take screen shots
- [x] Chrome in headless
- [x] Options from backend
- [x] Disable bots in backend, with invalid cookies
- [x] Debug mode
- [x] Mute streams
- [x] Kill all chrome process when starts
- [ ] Random comments in streams

