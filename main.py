import smtplib
import dns.resolver
import re
import random
from faker import Faker
from colorama import init, Fore, Style
from datetime import datetime
import threading

# Configuration
domains = ['gmail.com']
THREAD_COUNT = 10
EMAIL_PATTERNS = [
    "{first_name}.{last_name}@",
    "{first_name}_{last_name}@",
    "{last_name}.{first_name}@",
    "{last_name}.{number}@",
    "{last_name}_{first_name}@",
    "{first_name}{number}@",
    "{first_name}{last_name}{number}@",
    "{first_name}.{number}@",
    "{last_name}_{number}@",
    "{first_name[0]}{last_name}@",
    "{first_name[0]}{last_name}{number}@",
    "{first_name}_{last_name[0]}@",
    "{first_name[0]}_{last_name}@",
    "{last_name}_{first_name[0]}@"
]


def print_header():
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header_art = f"""
{Fore.MAGENTA}  _____   ______      ________  _____ 
{Fore.MAGENTA} |  __ \ / __ \ \    / /  ____|/ ____|
{Fore.MAGENTA} | |  | | |  | \ \  / /| |__  | (___  
{Fore.MAGENTA} | |  | | |  | |\ \/ / |  __|  \___ \ 
{Fore.MAGENTA} | |__| | |__| | \  /  | |____ ____) |
{Fore.MAGENTA} |_____/ \____/   \/   |______|_____/                                     
{Fore.CYAN}=================================================
{Fore.CYAN}== {Style.BRIGHT}Script Title: Email Authenticator: Advanced Email Verification System
{Fore.CYAN}== {Style.BRIGHT}Created by: DON DOVES [METADOR]
{Fore.CYAN}== {Style.BRIGHT}Date: {current_date}
{Fore.CYAN}== {Style.BRIGHT}Version: V2.2
{Fore.CYAN}== {Style.BRIGHT}Description: An educational tool for generating and verifying email addresses. Utilizes DNS and SMTP protocols alongside the Faker library to simulate real-world email verification processes.
{Fore.CYAN}== {Style.BRIGHT}Additional Info: This script is for educational use only, respecting ethical and legal standards. It provides technical verification of email addresses without guaranteeing their actual existence.
{Fore.CYAN}=================================================
    """
    print(header_art)


init(autoreset=True)


def generate_realistic_email():
    fake = Faker()
    first_name = fake.first_name().lower()
    last_name = fake.last_name().lower()
    number = str(random.randint(1, 99)) if random.choice([True, False]) else ''
    pattern = random.choice(EMAIL_PATTERNS)
    email = pattern.format(first_name=first_name, last_name=last_name, number=number)
    return email + random.choice(domains)


def is_email_real(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False

    domain = email.split('@')[1]
    try:
        records = dns.resolver.resolve(domain, 'MX')
        mx_record = str(records[0].exchange)
    except Exception:
        return False

    server = smtplib.SMTP()
    server.set_debuglevel(0)
    try:
        server.connect(mx_record)
        server.helo(server.local_hostname)
        server.mail('me@domain.com')
        code, message = server.rcpt(str(email))
        server.quit()

        if code == 250:
            return True
        else:
            return False
    except Exception:
        return False


hit_count = 0
hit_count_lock = threading.Lock()


def check_email_thread():
    global hit_count
    while True:
        email_to_test = generate_realistic_email()
        if is_email_real(email_to_test):
            print(Fore.GREEN + Style.BRIGHT + f"The email {email_to_test} seems to be real.")
            with open('real_emails.txt', 'a') as file:
                file.write(email_to_test + '\n')

            with hit_count_lock:
                hit_count += 1

            print(Fore.YELLOW + Style.BRIGHT + f"Hit count: {hit_count}")
        else:
            print(Fore.RED + Style.BRIGHT + f"The email {email_to_test} seems to be fake or inactive.")


# Main Execution
if __name__ == "__main__":
    init(autoreset=True)
    print_header()

    hit_count = 0
    hit_count_lock = threading.Lock()

    threads = [threading.Thread(target=check_email_thread) for _ in range(THREAD_COUNT)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
