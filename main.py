import os
import random
import string
import time

import requests


def CodeGen(length):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


def update_title(checks, successes):
    os.system(
        f"title Chess.com code generator: Total: {checks} - Successes: {successes} // @ezbooz"
    )


def save_valid_code(coupon):
    with open("valid_codes.txt", "a") as file:
        file.write(f"https://www.chess.com/offer?coupon=DISCORD124-{coupon}\n")


def main():
    checks = 0
    successes = 0

    while True:
        checks += 1
        coupon = CodeGen(5)
        try:
            r = requests.get(f"https://www.chess.com/offer?coupon=DISCORD124-{coupon}")
            status_code = r.status_code
            text = r.text

            if status_code == 200:
                if (
                    "We're sorry. This code is not valid. Please try a different code."
                    in text
                ):
                    print(
                        f"[-] Invalid coupon code: {coupon} - This code does not exist or is incorrect."
                    )
                elif "We're sorry. This special offer is no longer available." in text:
                    print(
                        f"[-] Expired coupon code: {coupon} - The offer has ended or the code is no longer valid."
                    )
                elif "Login to Your Chess Account" in text:
                    successes += 1
                    print(
                        f"[+] Valid coupon code: {coupon} - The code is valid and the offer is available!"
                    )
                    save_valid_code(coupon)
                else:
                    print(
                        f"[!] Unexpected content for coupon code: {coupon} - Please review the response manually."
                    )
            else:
                status_messages = {
                    429: "[!!!] Rate limit exceeded. Too many requests in a short period. Please wait before trying again.",
                    404: "[!!!] Page not found. The coupon link may be broken or the offer might have been removed.",
                    409: "[!!!] Request blocked. You might be temporarily banned from making requests. Check your IP status.",
                }
                print(
                    f"\n{status_messages.get(status_code, f'[!!!] Received an unexpected HTTP status code: {status_code}.')}"
                )

            update_title(checks, successes)

        except requests.RequestException as e:
            print(f"\n[!] Error occurred during the request: {e}.")
            input("Press Enter to retry the request or Ctrl+C to exit...")

        time.sleep(0.5)


if __name__ == "__main__":
    main()
