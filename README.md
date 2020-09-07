<p align="center">
  <img src="/logo.png" alt="Logo" />
</p>

# youtube-subscription-manager
Manually opening new tabs, signing into your new account, subscribing, browser lag, closing tabs, repeat. If you've ever experienced this process, you know it's time consuming. 

I couldn't find any working tool that met this need, so I decided to create a reliable youtube subscription manager.
# How to use

This tool is made for Google Chrome on Windows. Ensure that it is installed.

## Warning
Do not resize the browser window. This will cause Selenium to stop functioning.

Signing in normally through Google is blocked when automating. A workaround is to sign in through a different application with Google. For the tool to work,
you will need to find a website that allows signing in with Google. Some examples are Khan Academy, Stack Overflow, Github. In no way is this program
affiliated with the sites mentioned, nor attempting to create traffic for them.

Allowing sync is also required so that the sign in works for the scope of the entire browser. Please Enable 'Allow Chrome sign-in' at chrome://settings/syncSetup.

## Exporting

1. Visit https://www.youtube.com/subscription_manager, or [direct download](https://www.youtube.com/subscription_manager?action_takeout=1)

2. Scroll to the bottom, and click *Export subscriptions* under *Export to RSS readers*. You will now have an XML file containing your subscriptions.

## Importing
1. Place your XML file in the current directory. 
2. Run xmlimport.py
3. Follow the instructions in the terminal window.

# FAQ / Help
* Do I need to install any external dependencies?
    
    - Not at all! All dependencies are included when downloading this reposititory.

* How do I run .py files?

    1. Download the latest version of Python3 from https://www.python.org/
    2. If prompted to add python to your path, select yes.
    3. Open a terminal (cmd if on Windows)
    4. Type `python (file).py`
        * if this doesn't work, try `python3 (file).py`

* Not all my subscriptions were imported.

    - You may need to run the program again after a few hours/days. Youtube throttles subscription requests, most likely to prevent bots from creating false popularity.

    - Could this have been the result of your internet connection at the time?

    - Have you selected the correct brand account?

* Google services like Youtube comments, Google classroom aren't working!

    - Visit the pinned issue under Issues at the top of the page. There you will find instructions.

* `Push notifications enabled.` is displayed even when the channel already has them enabled.

    - Currently the css selector to detect whether or not that is the case is broken. Either it is Youtube blocking such a search, or the library being used.

* What version of Python was this project created in?

    - Python v3.8.5
    
If you have any other questions or problems, refer to the Issues tab. If there isn't an issue already created, feel free to do so.

# Upcoming??

* Webcrawl option for export if xml download button breaks (v2)
* Webcrawl option for import if ?sub_comfirmation=1 breaks (v2)
* Updated readme/tutorial reflecting (v2) changes
* Class based refactor (v2)
---
* Optimizations
* readme flare
* easy to read comments/docstrings

# Credits
This project is built using [webbot](https://github.com/nateshmbhat/webbot), a wrapper for Selenium browser automation. The license used is inherited from webbot.

Color library used: [colored](https://pypi.org/project/colored/).
