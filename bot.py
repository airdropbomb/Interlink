from aiohttp import (
    ClientResponseError,
    ClientSession,
    ClientTimeout
)
from aiohttp_socks import ProxyConnector
from datetime import datetime
from colorama import *
import asyncio, base64, time, json, os, pytz

wib = pytz.timezone('Asia/Jakarta')

class Interlink:
    def __init__(self) -> None:
        self.headers = {
            "User-Agent": "okhttp/4.12.0",
            "Accept-Encoding": "gzip"
        }
        self.BASE_API = "https://prod.interlinklabs.ai/api/v1"
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Auto Claim {Fore.BLUE + Style.BRIGHT}Interlink - BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    def load_accounts(self):
        filename = "accounts.json"
        try:
            if not os.path.exists(filename):
                self.log(f"{Fore.RED}File {filename} Not Found.{Style.RESET_ALL}")
                return

            with open(filename, 'r') as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
                return []
        except json.JSONDecodeError:
            return []
    
    def save_accounts(self, new_accounts):
        filename = "accounts.json"
        try:
            if not os.path.exists(filename):
                with open(filename, 'w') as file:
                    json.dump(new_accounts, file, indent=4)
                return

            with open(filename, 'r') as file:
                existing_accounts = json.load(file)

            if isinstance(existing_accounts, list):
                existing_accounts.extend(new_accounts)
            else:
                existing_accounts = new_accounts

            with open(filename, 'w') as file:
                json.dump(existing_accounts, file, indent=4)

        except Exception as e:
            return []
    
    async def load_proxies(self, use_proxy_choice: int):
        filename = "proxy.txt"
        try:
            if use_proxy_choice == 1:
                async with ClientSession(timeout=ClientTimeout(total=30)) as session:
                    async with session.get("https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt") as response:
                        response.raise_for_status()
                        content = await response.text()
                        with open(filename, 'w') as f:
                            f.write(content)
                        self.proxies = content.splitlines()
            else:
                if not os.path.exists(filename):
                    self.log(f"{Fore.RED + Style.BRIGHT}File {filename} Not Found.{Style.RESET_ALL}")
                    return
                with open(filename, 'r') as f:
                    self.proxies = f.read().splitlines()
            
            if not self.proxies:
                self.log(f"{Fore.RED + Style.BRIGHT}No Proxies Found.{Style.RESET_ALL}")
                return
        
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Failed To Load Proxies: {e}{Style.RESET_ALL}")
            self.proxies = []

    def check_proxy_schemes(self, proxies):
        schemes = ["http://", "https://", "socks4://", "socks5://"]
        if any(proxies.startswith(scheme) for scheme in schemes):
            return proxies
        return f"http://{proxies}"

    def get_next_proxy_for_account(self, token):
        if token not in self.account_proxies:
            if not self.proxies:
                return None
            proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
            self.account_proxies[token] = proxy
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.account_proxies[token]

    def rotate_proxy_for_account(self, token):
        if not self.proxies:
            return None
        proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
        self.account_proxies[token] = proxy
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy
    
    def decode_token(self, token: str):
        try:
            header, payload, signature = token.split(".")
            decoded_payload = base64.urlsafe_b64decode(payload + "==").decode("utf-8")
            parsed_payload = json.loads(decoded_payload)
            exp_time = parsed_payload.get("exp", None)
            
            return exp_time
        except Exception as e:
            return None
    
    def mask_account(self, account):
        if "@" in account:
            local, domain = account.split('@', 1)
            mask_account = local[:3] + '*' * 3 + local[-3:]
            return f"{mask_account}@{domain}"
        
    def print_question(self):
        while True:
            try:
                print(f"{Fore.WHITE + Style.BRIGHT}1. Add Account in accounts.json{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}2. Use Current accounts.json{Style.RESET_ALL}")
                runner = int(input(f"{Fore.BLUE + Style.BRIGHT}Choose [1/2] -> {Style.RESET_ALL}").strip())

                if runner in [1, 2]:
                    run_type = (
                        "Add Account in " if runner == 1 else 
                        "Use Current"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}{run_type} accounts.json Selected.{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1 or 2.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1 or 2).{Style.RESET_ALL}")

        while True:
            try:
                print(f"{Fore.WHITE + Style.BRIGHT}1. Run With Monosans Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}2. Run With Private Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}3. Run Without Proxy{Style.RESET_ALL}")
                choose = int(input(f"{Fore.BLUE + Style.BRIGHT}Choose [1/2/3] -> {Style.RESET_ALL}").strip())

                if choose in [1, 2, 3]:
                    proxy_type = (
                        "Run With Monosans Proxy" if choose == 1 else 
                        "Run With Private Proxy" if choose == 2 else 
                        "Run Without Proxy"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}{proxy_type} Selected.{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1, 2 or 3.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1, 2 or 3).{Style.RESET_ALL}")

        return runner, choose
    
    def login_question(self):
        while True:
            interlink_id = input(f"{Fore.WHITE + Style.BRIGHT}Enter Interlink ID [ without xxxx@ ] -> {Style.RESET_ALL}").strip()
            if interlink_id:
                break
            else:
                print(f"{Fore.RED + Style.BRIGHT}Please enter a positive number.{Style.RESET_ALL}")

        while True:
            passcode = input(f"{Fore.WHITE + Style.BRIGHT}Enter Your 6 Digits Passcode         -> {Style.RESET_ALL}").strip()
            if len(passcode) == 6:
                break
            else:
                print(f"{Fore.RED + Style.BRIGHT}Please enter 6 digits number.{Style.RESET_ALL}")

        while True:
            try:
                email = input(f"{Fore.WHITE + Style.BRIGHT}Enter Your Registered Email          -> {Style.RESET_ALL}").strip().lower()
                if "@" in email:
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter a valid email.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input.{Style.RESET_ALL}")

        return interlink_id, passcode, email
            
    async def send_otp(self, interlink_id: str, passcode: str, email: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/auth/send-otp-email-verify-login"
        payload = {"loginId":int(interlink_id), "passcode":int(passcode), "email":email}
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=self.headers, json=payload) as response:
                        response.raise_for_status()
                        result = await response.json()
                        return result["data"]["success"]
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return print(
                    f"{Fore.RED + Style.BRIGHT}Sending OTP Failed:{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )
            
    async def verify_otp(self, interlink_id: str, otp: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/auth/check-otp-email-verify-login"
        payload = {"loginId":int(interlink_id), "otp":int(otp)}
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=self.headers, json=payload) as response:
                        response.raise_for_status()
                        result = await response.json()
                        return result["data"]["jwtToken"]
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return print(
                    f"{Fore.RED + Style.BRIGHT}Verifying OTP Failed:{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )
            
    async def token_balance(self, token: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/token/get-token"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}"
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return None
            
    async def claimable_check(self, token: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/token/check-is-claimable"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}"
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return None
            
    async def claim_airdrop(self, token: str, proxy=None, retries=1):
        url = f"{self.BASE_API}/token/claim-airdrop"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}"
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, json={}) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return None
        
    async def process_add_accounts(self, use_proxy: bool):
        accounts = []

        interlink_id, passcode, email = self.login_question()

        proxy = self.get_next_proxy_for_account(email) if use_proxy else None

        print(f"{Fore.YELLOW + Style.BRIGHT}Start Setting Up With Proxy {proxy}{Style.RESET_ALL}")
        await asyncio.sleep(1)

        print(f"{Fore.YELLOW + Style.BRIGHT}Try To Sending OTP...{Style.RESET_ALL}", end="\r", flush=True)
        await asyncio.sleep(1)

        send_otp = await self.send_otp(interlink_id, passcode, email, proxy)
        if not send_otp:
            return []
        
        print(f"{Fore.GREEN + Style.BRIGHT}Sending OTP Success, Check Your Email{Style.RESET_ALL}")
        await asyncio.sleep(1)
    
        while True:
            otp = input(f"{Fore.WHITE + Style.BRIGHT}Enter 6 Digits OTP -> {Style.RESET_ALL}").strip()
            if len(otp) == 6:
                break
            else:
                print(f"{Fore.RED + Style.BRIGHT}Please enter 6 digits number.{Style.RESET_ALL}")

        print(f"{Fore.YELLOW + Style.BRIGHT}Verifying OTP...{Style.RESET_ALL}", end="\r", flush=True)
        await asyncio.sleep(1)

        token = await self.verify_otp(interlink_id, otp, proxy)
        if not token:
            return []

        accounts.append({"InterlinkID":interlink_id, "Passcode":passcode, "Email":email, "Token":token})

        self.save_accounts(accounts)

        print(f"{Fore.GREEN + Style.BRIGHT}Verifying OTP Success, Your Data Has Been Saved in accounts.json{Style.RESET_ALL}")
        await asyncio.sleep(3)

        return True
    
    async def process_accounts(self, email: str, token: str, use_proxy: bool):
        proxy = self.get_next_proxy_for_account(email) if use_proxy else None

        self.log(
            f"{Fore.CYAN+Style.BRIGHT}Proxy  :{Style.RESET_ALL}"
            f"{Fore.WHITE+Style.BRIGHT} {proxy} {Style.RESET_ALL}"
        )

        balance = await self.token_balance(token, proxy)
        if balance:
            token_balance = balance.get("data", {}).get("interlinkTokenAmount", 0)
            silver_balance = balance.get("data", {}).get("interlinkSilverTokenAmount", 0)
            gold_balance = balance.get("data", {}).get("interlinkGoldTokenAmount", 0)
            diamond_balance = balance.get("data", {}).get("interlinkDiamondTokenAmount", 0)

            self.log(f"{Fore.CYAN+Style.BRIGHT}Balance:{Style.RESET_ALL}")
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT}  ● {Style.RESET_ALL}"
                f"{Fore.BLUE+Style.BRIGHT}Interlink Token:{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {token_balance} {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT}  ● {Style.RESET_ALL}"
                f"{Fore.BLUE+Style.BRIGHT}Silver Token   :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {silver_balance} {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT}  ● {Style.RESET_ALL}"
                f"{Fore.BLUE+Style.BRIGHT}Gold Token     :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {gold_balance} {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT}  ● {Style.RESET_ALL}"
                f"{Fore.BLUE+Style.BRIGHT}Diamond Token  :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {diamond_balance} {Style.RESET_ALL}"
            )

        else:
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}Balance:{Style.RESET_ALL}"
                f"{Fore.YELLOW+Style.BRIGHT} N/A {Style.RESET_ALL}"
            )

        check = await self.claimable_check(token, proxy)
        if check:
            is_claimable = check.get("data", {}).get("isClaimable", False)

            if is_claimable:
                claim = await self.claim_airdrop(token, proxy)
                if claim and claim.get("data", False):
                    self.log(
                        f"{Fore.CYAN+Style.BRIGHT}Mining :{Style.RESET_ALL}"
                        f"{Fore.GREEN+Style.BRIGHT} Claimed Successfully {Style.RESET_ALL}"
                    )
                else:
                    self.log(
                        f"{Fore.CYAN+Style.BRIGHT}Mining :{Style.RESET_ALL}"
                        f"{Fore.RED+Style.BRIGHT} Not Claimed {Style.RESET_ALL}"
                    )
            else:
                next_frame_ts = check.get("data", {}).get("nextFrame", 0) / 1000
                next_frame_wib = datetime.fromtimestamp(next_frame_ts).astimezone(wib).strftime('%x %X %Z')

                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Mining :{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} Already Claimed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.CYAN+Style.BRIGHT} Next Claim at: {Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT}{next_frame_wib}{Style.RESET_ALL}"
                )
        else:
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}Mining :{Style.RESET_ALL}"
                f"{Fore.YELLOW+Style.BRIGHT} Check Claimable Status Failed {Style.RESET_ALL}"
            )
        
    async def main(self):
        try:
            runnner, use_proxy_choice = self.print_question()

            use_proxy = False
            if use_proxy_choice in [1, 2]:
                use_proxy = True

            if use_proxy:
                await self.load_proxies(use_proxy_choice)

            if runnner == 1:
                await self.process_add_accounts(use_proxy)

            accounts = self.load_accounts()
            if not accounts:
                print(f"{Fore.YELLOW + Style.BRIGHT}No Accounts Loaded{Style.RESET_ALL}")
                return
            
            while True:
                self.clear_terminal()
                self.welcome()

                separator = "=" * 23
                for account in accounts:
                    if account:
                        email = account["Email"]
                        token = account["Token"]

                        if "@" in email and token:
                            self.log(
                                f"{Fore.CYAN + Style.BRIGHT}{separator}[{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} {self.mask_account(email)} {Style.RESET_ALL}"
                                f"{Fore.CYAN + Style.BRIGHT}]{separator}{Style.RESET_ALL}"
                            )

                            exp_time = self.decode_token(token)
                            if exp_time and int(time.time()) > exp_time:
                                self.log(
                                    f"{Fore.CYAN+Style.BRIGHT}Status :{Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT} Token Expired {Style.RESET_ALL}"
                                )
                                continue

                            await self.process_accounts(email, token, use_proxy)
                            await asyncio.sleep(3)

                self.log(f"{Fore.CYAN + Style.BRIGHT}={Style.RESET_ALL}"*68)
                seconds = 4 * 60 * 60
                while seconds > 0:
                    formatted_time = self.format_seconds(seconds)
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.BLUE+Style.BRIGHT}All Accounts Have Been Processed.{Style.RESET_ALL}",
                        end="\r"
                    )
                    await asyncio.sleep(1)
                    seconds -= 1

        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error: {e}{Style.RESET_ALL}")
            raise e

if __name__ == "__main__":
    try:
        bot = Interlink()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT}[ EXIT ] Interlink - BOT{Style.RESET_ALL}                                       "                              
        )