# Creator: Zortos
# Description: Geforce Now Queue Checker


import asyncio
import json
import time
import imaplib
import email
import re
import datetime
import os
import Globals
import itertools
import Stuffs
import Personal # This is my personal file with my API key for my website 
from playwright.async_api import async_playwright
from requests import post, get, delete
from termcolor import colored
from dotenv import load_dotenv


IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993
EMAIL = os.getenv("EMAIL")
EMAIL_ONETIMEPASS = os.getenv("EMAIL_ONETIMEPASS")
global_bot_tokens_iterator = None


# This only works with Gmail one time passwords
async def Get_Verification_Code():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL, EMAIL_ONETIMEPASS)

    # Search for emails from a specific email address
    mail.select("inbox")
    result, data = mail.search(None, "FROM", "account@tmail.nvidia.com")

    # Get the latest email ID and fetch the email
    latest_email_id = data[0].split()[-1]
    result, data = mail.fetch(latest_email_id, "(RFC822)")

    # Parse the email message
    raw_email = data[0][1]
    email_message = email.message_from_bytes(raw_email)

    # Extract the URL from the email body
    url_match = re.search(
        r"https?://login\.nvgs\.nvidia\.com\S*(?<![>\s])",
        email_message.get_payload(decode=True).decode("utf-8"),
    )

    # Close the mailbox and logout
    mail.close()
    mail.logout()
    return url_match.group(0).rstrip(r">\r\n") if url_match else "No URL found in email"


async def Refresh_Tokens():
    Accounts = Stuffs.Bots
    for account in Accounts:
        print(colored(f"[*] Refreshing {account}", "yellow"))
        async with async_playwright() as p:
            token_found = False
            GFNTOKEN = None
            context = await p.chromium.launch_persistent_context(
                user_data_dir=f"/root/Bots/Appdata/{account.split('@')[0]}", # Change this to your own path
                ignore_default_args=["--headless"],
                args=["--headless=new"],
            )

            page = await context.new_page()

            async def handle_request(request):
                nonlocal GFNTOKEN, token_found
                if "GFNJWT" in str(request.headers.get("authorization", "")):
                    GFNTOKEN = request.headers["authorization"]
                    token_found = True

            page.on("request", handle_request)
            await page.goto("https://www.nvidia.com/en-us/account/")
            await page.wait_for_timeout(10000)  # Implicit wait

            # Check if choose account screen exists
            try:
                if await page.query_selector(
                    "//html/body/nv-oauth-app/div[1]/div/div/div/nv-oauth-app-v1/account-list/div/form/div[2]/div[1]/div/div/div[2]/button"
                ):
                    await page.click(
                        "//html/body/nv-oauth-app/div[1]/div/div/div/nv-oauth-app-v1/account-list/div/form/div[2]/div[1]/div/div/div[2]/button",
                        timeout=10000,
                    )
                else:
                    print(colored("[X] No Choose Account Screen", "red"))
            except Exception as e:
                continue
            # Login
            try:
                if await page.query_selector('//*[@id="emailAddress"]'):
                    await page.type('//*[@id="emailAddress"]', account)
                    await page.click('//*[@id="loginNextButton"]')
                    await page.fill('//*[@id="signinPassword"]', Stuffs.BotsPassword)
                    await page.click('//*[@id="passwordLoginButton"]')
                    await page.wait_for_timeout(10000)
                    # This part might need adjustment for Playwright
                    print(colored("[-] Waiting for Verification Email", "orange"))
                    link = await Get_Verification_Code()
                    print(colored("[-] Got Verification Email", "green"))
                    await page.evaluate("window.open('%s', '_blank')" % link)
                    await page.wait_for_timeout(10000)
                else:
                    print(colored("[X] No Login Needed", "red"))
            except Exception as e:
                continue

            await page.goto("https://play.geforcenow.com/mall/#/layout/games")
            await page.wait_for_timeout(5000)
            # GFN Agree Screen
            try:
                if await page.query_selector(
                    '//*[@id="mat-dialog-1"]/gfn-oobe/div/gfn-oobe-welcome/div/div[3]/button'
                ):
                    await page.click(
                        '//*[@id="mat-dialog-1"]/gfn-oobe/div/gfn-oobe-welcome/div/div[3]/button',
                    )
                elif await page.query_selector(
                    '//*[@id="mat-dialog-0"]/gfn-oobe/div/gfn-oobe-welcome/div/div[3]/button'
                ):
                    await page.click(
                        '//*[@id="mat-dialog-0"]/gfn-oobe/div/gfn-oobe-welcome/div/div[3]/button',
                    )
                else:
                    print(colored("[X] No GFN Agree Screen", "red"))
            except Exception as e:
                print(colored("[X] No GFN Agree Screen", "red"))
            # Browse Games Button 
            await page.wait_for_timeout(1000)
            try:
                if await page.query_selector(
                    '//*[@id="mat-dialog-1"]/nv-hig-dialog/div/div/div/div[2]/div[2]/button'
                ):
                    await page.click(
                        '//*[@id="mat-dialog-1"]/nv-hig-dialog/div/div/div/div[2]/div[2]/button',
                    )
                elif await page.query_selector(
                    '//*[@id="mat-dialog-0"]/nv-hig-dialog/div/div/div/div[2]/div[2]/button'
                ):
                    await page.click(
                        '//*[@id="mat-dialog-0"]/nv-hig-dialog/div/div/div/div[2]/div[2]/button',
                    )
            except Exception as e:
                print(colored("[X] No Browse Games Button", "red"))
            await page.wait_for_timeout(1000)
            # Help Bubbles
            try:
                # /html/body/gfn-root/gfn-main-content/div/div/gfn-navigation/gfn-desktop-navigation/div/nv-product-tour/tour-step-template/popper-content/div/div[1]/div[2]/button
                # /html/body/gfn-root/gfn-main-content/div/div/gfn-navigation/gfn-desktop-navigation/div/nv-product-tour/tour-step-template/popper-content/div/div[1]/div[2]/button
                if await page.query_selector(
                    "//html/body/gfn-root/gfn-main-content/div/div/gfn-navigation/gfn-desktop-navigation/div/nv-product-tour/tour-step-template/popper-content/div/div[1]/div[2]/button"
                ):
                    await page.click(
                        "//html/body/gfn-root/gfn-main-content/div/div/gfn-navigation/gfn-desktop-navigation/div/nv-product-tour/tour-step-template/popper-content/div/div[1]/div[2]/button",
                    )
                    await page.click(
                        "//html/body/gfn-root/gfn-main-content/div/div/gfn-navigation/gfn-desktop-navigation/div/nv-product-tour/tour-step-template/popper-content/div/div[1]/div[2]/button",
                    )
            except Exception:
                print(colored("[X] No Help Bubbles", "red"))

            # Login to GFN
            try:
                if await page.query_selector("//html/body/gfn-root/gfn-main-content/div/div/gfn-navigation/gfn-desktop-navigation/div/gfn-toolbar/nv-app-bar/div[3]/div[3]/div/button[2]"):
                    await page.click(
                        "//html/body/gfn-root/gfn-main-content/div/div/gfn-navigation/gfn-desktop-navigation/div/gfn-toolbar/nv-app-bar/div[3]/div[3]/div/button[2]",
                    )

                    if await page.query_selector('//*[@id="mat-dialog-1"]/nv-hig-dialog/div/div/div/div[2]/div[2]/button[2]'):
                        await page.click(
                            '//*[@id="mat-dialog-1"]/nv-hig-dialog/div/div/div/div[2]/div[2]/button[2]'
                        )
                    elif await page.query_selector('//*[@id="mat-dialog-2"]/nv-hig-dialog/div/div/div/div[2]/div[2]/button[2]'):
                        await page.click(
                            '//*[@id="mat-dialog-2"]/nv-hig-dialog/div/div/div/div[2]/div[2]/button[2]'
                        )
                    await page.click('//*[@id="user_name_btn_0"]')
                    await page.click(
                        '//*[@id="root"]/div[2]/div/div[5]/form/button')
                else:
                    print(colored("[X] Already logged in", "red"))
            except Exception:
                print(colored("[X] Already logged in", "red"))

            # Browse Games Button
            try:
                if await page.query_selector(
                    '//*[@id="mat-dialog-1"]/nv-hig-dialog/div/div/div/div[2]/div[2]/button'
                ):
                    await page.click(
                        '//*[@id="mat-dialog-1"]/nv-hig-dialog/div/div/div/div[2]/div[2]/button',
                    )
                elif await page.query_selector(
                    '//*[@id="mat-dialog-0"]/nv-hig-dialog/div/div/div/div[2]/div[2]/button'
                ):
                    await page.click(
                        '//*[@id="mat-dialog-0"]/nv-hig-dialog/div/div/div/div[2]/div[2]/button',
                    )
            except Exception as e:
                print(colored("[X] No Browse Games Button", "red"))

            # Click on Demos
            try:
                if await page.query_selector(
                    "//html/body/gfn-root/gfn-main-content/div/div/gfn-navigation/gfn-desktop-navigation/div/gfn-sidebar/mat-drawer-container/mat-drawer-content/div/div/gfn-layout/div/div[1]/div/div/gfn-game-section[7]/div/div/div[2]/button"
                ):
                    await page.click(
                        "//html/body/gfn-root/gfn-main-content/div/div/gfn-navigation/gfn-desktop-navigation/div/gfn-sidebar/mat-drawer-container/mat-drawer-content/div/div/gfn-layout/div/div[1]/div/div/gfn-game-section[7]/div/div/div[2]/button",
                    )
                else:
                    print(colored("[X] No Demos", "red"))
            except Exception:
                print(colored("[X] No Demos", "red"))
            # Check if the token was found
            if token_found and GFNTOKEN:
                data = {}
                now = datetime.datetime.now()
                request_data = {
                    "Token": GFNTOKEN,
                    "Last Updated": now.strftime("%Y-%m-%d %H:%M:%S"),
                }
                try:
                    with open("BotTokens.json", "r+") as f:
                        data = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError):
                    print(colored("[*] Couldent Find BotTokens.json", "red"))

                data[account] = request_data

                with open("BotTokens.json", "w+") as f:
                    json.dump(data, f, indent=4)
                print(colored("[*] Found GFN Token", "green"))
            else:
                print(colored("[X] No GFN Token Found", "red"))

            await context.close()


# =============================
#           GFN Utils
# =============================
def clean_session(server, session_id, Token):
    headers = {
            "User-Agent": "ZortosQueueBot/1.0",
            "Cache-Control": "private, no-store, max-age=0",
            "Authorization": Token,
    }
    get_session_url = (
        f"https://{server}.cloudmatchbeta.nvidiagrid.net/v2/session/{session_id}"
    )
    response = delete(get_session_url, headers=headers)
    return response.status_code == 200


def create_session(server, Token):
    headers = {
            "User-Agent": "ZortosQueueBot/1.0",
            "Cache-Control": "private, no-store, max-age=0",
            "Authorization": Token,
    }
    response = post(
        f"https://{server}.cloudmatchbeta.nvidiagrid.net/v2/session?keyboardLayout=en-US&languageCode=en_US", headers=headers, data=json.dumps(Globals.session_static_json)
    )
    session_id = response.json()["session"]["sessionId"]

    if response.status_code != 200:
        return [response.json()["requestStatus"]["statusDescription"], session_id]
    get_session_url = (
        f"https://prod.cloudmatchbeta.nvidiagrid.net/v2/session/{session_id}"
    )
    time.sleep(3)
    get_session_post = get(get_session_url, headers=headers)
    get_session_response_JSON = get_session_post.json()
    return [get_session_response_JSON, session_id]


async def check_queue(server,Region):
    # Check if the the tokens are fresh enough to be used (3H) if not refresh them
    global global_bot_tokens_iterator

    token_info = next(global_bot_tokens_iterator)
    last_updated = datetime.datetime.strptime(
        token_info["Last Updated"], "%Y-%m-%d %H:%M:%S"
    )
    now = datetime.datetime.now()
    if (now - last_updated).total_seconds() > 10800:
        os.system("cls" if os.name == "nt" else "clear")
        print(colored("[*] Refreshing Tokens", "yellow"))
        await Refresh_Tokens()
        setupBotPool() 
        check_queue_possition(server, token_info["Token"],Region)


    else:
        print(f"[*] Checking Queue Position for {server}")
        check_queue_possition(server, token_info["Token"],Region)
        # Check queue position using token pool

def check_queue_possition(server, Token,Region):
    try:
        session = create_session(server, Token)
    except Exception as e:
        print(colored(f"[*] Queue Error: {e}", "red"))
        data = {}
        now = int(time.time())
        with open("QueueInfo.json", "r+") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                pass
        data[server] = {"QueuePosition": 1, "Last Updated": now,"Region": Region}
        with open("QueueInfo.json", "w+") as f:
            json.dump(data, f, indent=4)
        return "Null"
    if isinstance(session[0], str):
        print(colored(f"[*] Queue Error: {session[0]}", "red"))
        data = {}
        now = int(time.time())
        with open("QueueInfo.json", "r+") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                pass
        data[server] = {"QueuePosition": 1, "Last Updated": now,"Region": Region}
        with open("QueueInfo.json", "w+") as f:
            json.dump(data, f, indent=4)
        clean_session(server, session[1],Token)
        return "Null"
    
    try:
        queue_position = session[0]["session"]["seatSetupInfo"]["queuePosition"]
        # if queue_position isent int then its a error
        if queue_position > 0:
            print(colored(f"[*] Queue Position: {queue_position }", "green"))
            data = {}
            now = int(time.time())
            with open("QueueInfo.json", "r+") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    pass
            data[server] = {"QueuePosition": queue_position, "Last Updated": now,"Region": Region}
            with open("QueueInfo.json", "w+") as f:
                json.dump(data, f, indent=4)
            clean_session(server, session[1],Token)
            return queue_position
        else:
            print(colored(f"[*] Queue Error: {session[0]}", "red"))
            clean_session(server, session[1],Token)
            return "Null"
    except Exception as e:
        clean_session(server, session[1],Token)
        print(colored(f"[*] Queue Error: {e} \n {session[1]}", "red"))
        return "Null"


# =============================
#          Queue Stuff
# =============================


async def Check_US():
    for server in Globals.US_FREE_LIST:
        await check_queue(server , "NA")
    time.sleep(20)

async def Check_EU():
    for server in Globals.EU_FREE_LIST:
        await check_queue(server , "EU")
    time.sleep(20)

async def Check_CA():
    for server in Globals.CA_FREE_LIST:
        await check_queue(server, "CA")
    time.sleep(20)


async def Check_ALL():
    for server in Globals.US_FREE_LIST:
        await check_queue(server, "NA")
    for server in Globals.EU_FREE_LIST:
        await check_queue(server, "EU")
    for server in Globals.CA_FREE_LIST:
        await check_queue(server, "CA")
    await Personal.UploadQueue() # This is my personal file with my API key for my website 
    time.sleep(20)

def setupBotPool():
    global global_bot_tokens_iterator

    # Initialize the iterator if it hasn't been already
    data = {}
    with open("BotTokens.json", "r+") as f:
        data = json.load(f)
    global_bot_tokens_iterator = itertools.cycle(data.values())



if __name__ == "__main__":
    # Uncomment if you want to check a specific region
    # asyncio.run(Check_US())
    # asyncio.run(Check_EU())
    # asyncio.run(Check_CA())
    # asyncio.run(Check_ALL())
    load_dotenv()
    setupBotPool()
    time.sleep(20) # Wait before starting the Loop
    while True:
        asyncio.run(Check_ALL())
        
    
