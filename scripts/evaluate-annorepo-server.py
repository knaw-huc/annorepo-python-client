#!/usr/bin/env python3
import argparse
import traceback

from colorama import Fore

from annorepo.client import AnnoRepoClient

success_counter = 0
failure_counter = 0


def evaluate_task(name, method):
    global failure_counter, success_counter
    print(f"{Fore.YELLOW}> {Fore.CYAN}{name}{Fore.YELLOW}:{Fore.RESET}")
    try:
        result = method()
        print(f"{Fore.GREEN}success{Fore.RESET}")
        success_counter += 1
        print(f"{Fore.BLUE}method returned:{Fore.RESET}")
        print(result)
    except Exception:
        failure_counter += 1
        print(f"{Fore.RED}failure:\n{traceback.format_exc()}{Fore.RESET}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate the AnnoRepo server at the given URL",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("url",
                        help="The URL of the AnnoRepo server to evaluate",
                        type=str)
    parser.add_argument("admin_url",
                        nargs='?',
                        help="The admin URL of the AnnoRepo server to evaluate",
                        type=str)
    args = parser.parse_args()

    if args.url:
        base_url = args.url
        admin_url = args.admin_url
        print(f"{Fore.BLUE}Evaluating the AnnoRepo server at {Fore.YELLOW}{base_url}{Fore.RESET}")
        if admin_url:
            print(f"{Fore.BLUE}with admin access at {Fore.YELLOW}{args.admin_url}{Fore.RESET}")

        print()
        client = AnnoRepoClient(base_url, admin_url=admin_url, verbose=True)

        evaluate_task('get_about', client.get_about)
        evaluate_task('get_homepage', client.get_homepage)
        evaluate_task('get_robots_txt', client.get_robots_txt)
        evaluate_task('get_swagger_json', client.get_swagger_json)
        evaluate_task('get_swagger_yaml', client.get_swagger_yaml)
        evaluate_task('get_healthcheck', client.get_healthcheck)
        evaluate_task('get_ping', client.get_ping)

        print()
        print(f"{Fore.BLUE}{success_counter + failure_counter} tasks run:{Fore.RESET}")
        print(f"  {Fore.GREEN}{success_counter} successes{Fore.RESET}")
        print(f"  {Fore.RED}{failure_counter} failures{Fore.RESET}")
        print()
        print(f"{Fore.BLUE}evaluation done!{Fore.RESET}")


if __name__ == '__main__':
    main()
