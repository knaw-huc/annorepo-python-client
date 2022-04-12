#!/usr/bin/env python3
import argparse

from annorepo.client import AnnoRepoClient


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate the AnnoRepo server at the given URL",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("url",
                        help="The URL of the AnnoRepo server to evaluate",
                        type=str)
    args = parser.parse_args()

    if args.url:
        print(f"evaluating {args.url}")
        client = AnnoRepoClient(args.url)

        about = client.get_about()
        print("> get_about:")
        print(about)

        homepage = client.get_homepage()
        print("> get_homepage:")
        print(homepage)

        robots = client.get_robots_txt()
        print("> get_robots_txt:")
        print(robots)

        # favicon = client.get_favicon()
        # print("> get_favicon:")
        # print(favicon)

        swagger = client.get_swagger_json()
        print("> get_swagger_json:")
        print(swagger)

        swagger = client.get_swagger_yaml()
        print("> get_swagger_yaml:")
        print(swagger)

        print("done!")


if __name__ == '__main__':
    main()
