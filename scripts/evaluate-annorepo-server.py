#!/usr/bin/env python3
import argparse
import traceback

from colorama import Fore
from icecream import ic

from annorepo.client import AnnoRepoClient

success_counter = 0
failure_counter = 0

test_annotation = {
    "@context": "http://www.w3.org/ns/anno.jsonld",
    "type": "Annotation",
    "body": {
        "type": "TextualBody",
        "value": "I like this page!"
    },
    "target": "http://www.example.com/index.html"
}


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


def create_container_with_generated_name(client: AnnoRepoClient):
    container_data = client.create_container()
    ic(container_data)
    container_name = container_data['name']
    ic(container_name)
    result1 = client.read_container(container_name)
    ic(result1)
    result2 = client.delete_container(container_name)
    ic(result2)
    result3 = client.read_container(container_name)
    ic(result3)
    assert result3 is None
    return result3


def create_container_with_a_given_name(client: AnnoRepoClient):
    container_data = client.create_container("test_container")
    ic(container_data)
    container_name = container_data['name']
    ic(container_name)
    # assert container_name == "test_container"
    result = client.read_container(container_name)
    ic(result)
    result = client.delete_container(container_name)
    ic(result)
    result = client.read_container(container_name)
    ic(result)
    assert result is None
    return result


def create_annotation_with_generated_name(client: AnnoRepoClient):
    container_data = client.create_container()
    ic(container_data)
    container_name = container_data['name']
    ic(container_name)

    annotation_data = client.add_annotation(container_name=container_name, content=test_annotation)
    ic(annotation_data)
    annotation_name = annotation_data['name']

    result = client.read_annotation(container_name, annotation_name)
    ic(result)

    result = client.delete_annotation(container_name, annotation_name)
    ic(result)

    result = client.delete_container(container_name)
    ic(result)

    result = client.read_container(container_name)
    ic(result)
    assert result is None
    return result


def create_annotation_with_a_given_name(client: AnnoRepoClient):
    given_annotation_name = "my-annotation"
    container_data = client.create_container()
    ic(container_data)
    container_name = container_data['name']
    ic(container_name)

    annotation_data = client.add_annotation(container_name=container_name, content=test_annotation,
                                            name=given_annotation_name)
    ic(annotation_data)
    annotation_name = annotation_data['name']

    result = client.read_annotation(container_name, annotation_name)
    ic(result)

    result = client.delete_annotation(container_name, annotation_name)
    ic(result)

    result = client.delete_container(container_name)
    ic(result)

    result = client.read_container(container_name)
    ic(result)
    assert result is None
    return result


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
        evaluate_task('test_container_with_generated_name', lambda: create_container_with_generated_name(client))
        evaluate_task('test_container_with_given_name', lambda: create_container_with_a_given_name(client))
        evaluate_task('test_add_annotation_with_generated_name', lambda: create_annotation_with_generated_name(client))
        evaluate_task('test_add_annotation_with_given_name', lambda: create_annotation_with_a_given_name(client))

        print()
        print(f"{Fore.BLUE}{success_counter + failure_counter} tasks run:{Fore.RESET}")
        print(f"  {Fore.GREEN}{success_counter} successes{Fore.RESET}")
        print(f"  {Fore.RED}{failure_counter} failures{Fore.RESET}")
        print()
        print(f"{Fore.BLUE}evaluation done!{Fore.RESET}")


if __name__ == '__main__':
    main()
