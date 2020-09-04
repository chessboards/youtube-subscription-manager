from libs.webbot import Browser 
from htmlparser import htxmlParser

from time import sleep
from random import randint
import os
import codecs # when opening file, convert to unicode to prevent errors with multi-lingual keyboards or channel names that have strange characters

from libs.colored import fg, bg, attr

# functional programming for now v1
#option = "Is your subscription file exported from youtube, or webcrawled?" v2 example
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
    if bell.lower() != 'y' and bell.lower() != 'n': # Ensure input is y/n. If not, raise valueerror. Handled near eof
        raise ValueError()

def _read():
    """Creates a feedable value to use in the parser"""
    working_dir = os.path.dirname(os.path.realpath(__file__))

    print("\nReading file contents...")

    with codecs.open(working_dir + r"\subscription_manager.xml", 'r', encoding='utf-8') as fileobject:
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


def _bell_check():
    """Returns a boolean based upon if push notifications can be enabled. Called by _enable_bell_notifications()."""
    #https://developer.mozilla.org/en-US/docs/Web/CSS/Attribute_selectors and https://www.w3schools.com/cssref/css_selectors.asp if broken

    # ERROR: the method should detect based on the aria-label css_selector if the button exists. Either it is youtube or the webbot library, but the css selector doesn't seem to work here. Tested in an
    #environment with the button's element and a JS querySelector with the same css_selector, it works fine.
    return 1 # returning 1 goes through many unneeded clicks, but nonetheless sets all subscriptions to all notifications.

    if web.exists(tag='button', classname='yt-icon-button', css_selector='button[aria-label*="Current setting is all notifications."]', number=1, loose_match=False): #aria-label differs based on bell state
        return 0 # can't enable push notifications
    else:
        return 1


# can it be optimized? checking every subscription for if y is chosen may cause lag.
def _enable_bell_notifications():
    """Enables all bell notifications for a subscription. Returns message of type string based on the status of push notifications; if the user chose not to enable them, returns false.
    Called by subscribe()."""

    if _bell_check() == True: # push notifications. Even if already subscribed, bell notifications may not be enabled.
        web.click(tag='div', css_selector='#notification-preference-button', number=1, loose_match=False, multiple=False) # dropdown
        web.click(text='All', tag='yt-formatted-string', classname='ytd-menu-service-item-renderer', number=1, loose_match=False, multiple=False) # choose all push notifications
        message = "\t%sPush notifications %s.%s"  %  (fg(45), 'enabled', attr(0)) 
    else:
        message = "\t%sPush notifications %s.%s"  %  (fg(221), 'already enabled', attr(0)) 

    return message



# optimize for unneeded != characters
def subscribe():
    """Opens every url in global subscription_urls, and checks if subscribable. If so, subscribes."""
    print("Youtube throttles subscription requests, most likely to prevent bots from creating false popularity. The process of importing your subscriptions may take awhile.\n")
    sleep(4)

    print("Opening URLs...")

    for url in subscription_urls:
        web.go_to(url)
        if can_subscribe_check() == 0:
            web.click(text='SUBSCRIBE', tag='paper-button', id='button', classname='style-blue-text', number=1, loose_match=False, multiple=False)

            message = "\t%s(%i/%i)%s Subscribed."  %  (fg(40), subscription_urls.index(url)+1, len(subscription_urls)+1, attr(0) )

            if bell == 'y': # if user chose to enable push notifications
                message2 = _enable_bell_notifications()

                message += message2

            print(message) # confirmation

            sleep(randint(4,9)) # simulate human clickage delay to attempt to prevent throttling


        elif can_subscribe_check() == 1:
            message = "\t%s(%i/%i)%s Cannot subscribe: already subscribed."  %  (fg(196), subscription_urls.index(url)+1, len(subscription_urls)+1, attr(0) )
            message2 = _enable_bell_notifications()

            if message2 != 0:
                message += message2

            print(message) # confirmation

            # why no delay? I suppose subscribing is a more suspicious request than enabling push notifications, but I'm not sure if they both count as the same type of request.
            # also speed


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
    except ValueError:
        print("\nError: Choice of push notifications must be 'y' or 'n'.")
    except Exception as e:
        print(f"\n[!] Uncaught Error: {e}")

if __name__ == "__main__":
    main()
