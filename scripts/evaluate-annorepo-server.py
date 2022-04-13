#!/usr/bin/env python3
import argparse

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
        print(f"{Fore.RED}failure{Fore.RESET}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate the AnnoRepo server at the given URL",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("url",
                        help="The URL of the AnnoRepo server to evaluate",
                        type=str)
    args = parser.parse_args()

    if args.url:
        print(f"{Fore.BLUE}evaluating {Fore.YELLOW}{args.url}{Fore.RESET}")
        print()
        client = AnnoRepoClient(args.url, verbose=True)

        evaluate_task('get_about', client.get_about)
        evaluate_task('get_homepage', client.get_homepage)
        evaluate_task('get_robots_txt', client.get_robots_txt)
        evaluate_task('get_swagger_json', client.get_swagger_json)
        evaluate_task('get_swagger_yaml', client.get_swagger_yaml)

        print()
        print(f"{Fore.GREEN}{success_counter} successes{Fore.RESET}")
        print(f"{Fore.RED}{failure_counter} failures{Fore.RESET}")
        print()
        print(f"{Fore.BLUE}done!{Fore.RESET}")


if __name__ == '__main__':
    main()
