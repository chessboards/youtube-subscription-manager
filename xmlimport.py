from libs.webbot import Browser 
from htmlparser import htxmlParser

from time import sleep
from random import randint
import os

from libs.colored import fg, bg, attr

# functional programming
#option = "Is your subscription file exported from youtube, or webcrawled?"
def introduction():
    """Introduces the user to the program, creates browser window"""
    confirm = input(f"""
    {fg(196)}youtube-subscription-manager{attr(0)} importer

    Signing in normally through Google is blocked when automating. A workaround is to sign in through a different application with Google. For the tool to work,
    you will need to find a website that allows signing in with Google. Some examples are Khan Academy, Stack Overflow, Github. In no way is this program
    affiliated with the sites mentioned, nor attempting to create traffic for them.

    Allowing sync is also required so that the sign in works for the scope of the entire browser. Please Enable 'Allow Chrome sign-in' at chrome://settings/syncSetup.

    Enter any character to proceed: \n> """)

    global web   #object used in subscribe()
    global bell  #bool used in subscribe()

    web = Browser()
    print("Browser window created.\n")
    print(f"{fg(196)}WARNING{attr(0)}: Do not resize the window.\n")

    confirm = input("Once you have successfully logged in using the newly created browser window, enter any character to proceed:\n> ")

    web.go_to("https://www.youtube.com/")
    web.switch_to_tab(1)

    confirm = input("\nIf you have multiple brand accounts, please choose the account you wish to use by clicking your icon in the top right. In either case, please any character to proceed:\n> ")

    bell = input("\nWould you like to enable push notifications when you subscribe?(y/n)\n> ")

def _read():
    """Creates a feedable value to use in the parser"""
    working_dir = os.path.dirname(os.path.realpath(__file__))

    print("\nReading file contents...")

    with open(working_dir + r"\subscription_manager.xml", 'r') as fileobject:
        global contents

        contents = fileobject.read()
        print(f"{fg(40)}Done!\n{attr(0)}")

def _parse():
    """Feeds xml file into parser, expands the scope of the end url list result"""
    print("Parsing file contents...")
    parser = htxmlParser()
    parser.feed(contents)
    global subscription_urls
    subscription_urls = parser.subscription_urls
    
    print(f"{fg(40)}Done!\n{attr(0)}")

def process_file():
    """Refactor, reads and parses subscription xml file."""
    _read()
    _parse()


# broken? https://www.w3schools.com/cssref/css_selectors.asp
def can_subscribe_check():
    """Returns values based upon if the channel is found to be banned, already subscribed to, or not. Also detects throttling."""
    if web.exists(text="Too many recent subscriptions"):
        return 3
    else:
        if web.exists(text='This account has been terminated'):
            return 2
        elif web.exists(text='SUBSCRIBED', css_selector="ytd-subscribe-button-renderer .ytd-c4-tabbed-header-renderer > yt-formatted-string"): # to right mini could be subscribed; more specific
            return 1
        else:
            return 0


def bell_check():
    """Returns a boolean based upon if push notifications can be enabled."""
    #https://developer.mozilla.org/en-US/docs/Web/CSS/Attribute_selectors    Detects the state of bell notifications.
    if web.exists(tag='button', css_selector='[aria-label*="Current setting is personalized notifications. Tap to change your notification setting for"]',loose_match=False):
        return 1 # can enable push notifications
    else:
        return 0 # already enabled


def enable_bell_notifications():
    """Enables all bell notifications for a subscription. The print is a"""
    if bell_check(): #push notification. Even if already subscribed, bell notifications may not be enabled.
        web.click(text='All', tag='yt-formatted-string', classname='ytd-menu-service-item-renderer', number=1, loose_match=False, multiple=False)
        print("\t%sPush notifications %s.%s"  %  (fg(45), 'enabled', attr(0)) )
    else:
        print("\t%sPush notifications %s.%s"  %  (fg(11), 'already enabled', attr(0)) )

def subscribe():
    """Opens every url in global subscription_urls, and checks if subscribable. If so, subscribes."""
    print("Youtube throttles subscription requests, most likely to prevent bots from creating false popularity. The process of importing your subscriptions may take awhile.\n")
    sleep(4)

    print("Opening URLs...")

    for url in subscription_urls:
        web.go_to(url)
        if can_subscribe_check() == 0:
            web.click(text='SUBSCRIBE', tag='paper-button', id='button', classname='style-blue-text', number=1, loose_match=False, multiple=False)
            # end='' to append the next print function, as one line would be way too long
            print("\t%s(%i/%i)%s Subscribed."  %  (fg(40), subscription_urls.index(url)+1, len(subscription_urls)+1, attr(0) ), end="") # though outdated, the quickest/simplest format.

            if bell_check():
                web.click(text='All', tag='yt-formatted-string', classname='ytd-menu-service-item-renderer', number=1, loose_match=False, multiple=False)
                print("\t%sPush notifications %s.%s"  %  (fg(45), 'enabled', attr(0)) )
            else:
                print("\t%sPush notifications %s.%s"  %  (fg(11), 'already enabled', attr(0)) )

            sleep(randint(4,9)) # simulate human clickage delay


        elif can_subscribe_check() == 1:
            # end='' to append the next print function, as one line would be way too long
            print("\t%s(%i/%i)%s Cannot subscribe: already subscribed."  %  (fg(196), subscription_urls.index(url)+1, len(subscription_urls)+1, attr(0) ), end=""),

            if bell_check(): # push notification. Even if already subscribed, bell notifications may not be enabled.
                web.click(text='All', tag='yt-formatted-string', classname='ytd-menu-service-item-renderer', number=1, loose_match=False, multiple=False)
                print("\t%sPush notifications %s.%s"  %  (fg(45), 'enabled', attr(0)) )
            else:
                print("\t%sPush notifications %s.%s"  %  (fg(11), 'already enabled', attr(0)) )

        elif can_subscribe_check() == 2:
            print("\t%s(%i/%i) Cannot subscribe: channel terminated.%s"  %  (fg(196), subscription_urls.index(url)+1, len(subscription_urls)+1, attr(0) ) )
            pass

        elif can_subscribe_check() == 3:
            print("\t%s(%i/%i) Cannot subscribe: requests being throttled.%s"  %  (fg(209), subscription_urls.index(url)+1, len(subscription_urls)+1, attr(0) ) )
            
    print(f"{fg(40)}Done!\n{attr(0)}")
    
    print("You may now exit the browser window.")
    print(f"The subscriptions should now be imported to your account. Thank you for using my tool! {fg(192)}:-]{attr(0)}")





def main():
    try:
        introduction()
        process_file()
        subscribe()
    except FileNotFoundError:
        print("\nError: subscription_manager.xml was not found. Did you place it in the same directory as xmlimport.py?")
    except Exception as e:
        print(f"\n[!] Uncaught Error: {e}")

if __name__ == "__main__":
    main()