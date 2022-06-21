#!/usr/bin/env python3
import argparse
import json
import random
import time

from colorama import Fore
from icecream import ic
from tabulate import tabulate

from annorepo.client import AnnoRepoClient


def main():
    parser = argparse.ArgumentParser(
        description="Do a load test on the AnnoRepo server at the given URL",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        allow_abbrev=True
    )
    parser.add_argument("-u", "--url",
                        required=True,
                        help="The URL of the AnnoRepo server to test",
                        type=str)
    parser.add_argument("-a", "--admin-url",
                        required=False,
                        help="The admin URL of the AnnoRepo server to test",
                        type=str)
    parser.add_argument("-f", "--annotations_file",
                        required=True,
                        help="The json file containing the annotations to use in the test",
                        type=str)
    parser.add_argument("-n", "--testsize",
                        help="The number of annotations to use in the test"
                             " (will be randomly selected from the annotations_file)",
                        default=10,
                        type=int)
    parser.add_argument("-d", "--delete-afterwards",
                        required=False,
                        action='store_true',
                        help="Remove the created container and annotations after the load test",
                        default=False)
    args = parser.parse_args()
    ic(args)

    if args.url:
        base_url = args.url
        admin_url = args.admin_url
        print(f"{Fore.BLUE}Load-testing the AnnoRepo server at {Fore.YELLOW}{base_url}{Fore.RESET}")
        if admin_url:
            print(f"{Fore.BLUE}with admin access at {Fore.YELLOW}{args.admin_url}{Fore.RESET}")

        print()

        print(f"reading from {args.annotations_file}: ", end='')
        with (open(args.annotations_file)) as f:
            annotations = json.load(f)
        print(f"{len(annotations)} annotations.")
        sample = [random.choice(annotations) for _ in range(args.testsize)]

        try:
            averages = {}
            client = AnnoRepoClient(base_url, admin_url=admin_url)
            print(f"creating container 'loadtest' (using postgres/elasticsearch)")
            container_name = client.create_container("loadtest")['name']

            annotation_names = []
            sample_size = len(sample)
            print(f"uploading {sample_size} annotations individually: (using postgres/elasticsearch)")
            start = time.perf_counter()
            for a in sample:
                try:
                    annotation_data = client.add_annotation(container_name=container_name, content=a)
                    annotation_name = annotation_data['id'].split('/')[-1]
                    annotation_names.append(annotation_name)
                except Exception:
                    print("something went wrong")
            end = time.perf_counter()
            duration = (end - start)
            avg = (duration / sample_size)
            averages[f"postgres/es: {sample_size} individually"] = (duration, avg)
            print(
                f"uploading individually (using postgres/elasticsearch) took {duration:0.4f} seconds: {avg :0.4f} s/annotation")

            print(f"uploading {sample_size} annotations in bulk (using postgres/elasticsearch):")
            start = time.perf_counter()
            # try:
            annotation_data = client.add_annotations(container_name, sample)
            # ic(annotation_data)
            # except:
            #     print("something went wrong")
            end = time.perf_counter()
            duration = (end - start)
            avg = (duration / sample_size)
            averages[f"postgres/es: {sample_size} in bulk"] = (duration, avg)
            print(
                f"uploading in bulk (using postgres/elasticsearch) took {duration:0.4f} seconds: {avg:0.4f} s/annotation")

        finally:
            if args.delete_afterwards:
                print("removing test container + annotations (using postgres/elasticsearch)")
                for name in annotation_names:
                    client.delete_annotation(container_name, name)
                client.delete_container(container_name)

        # try:
        #     print(f"creating container 'loadtest' (using mongodb)")
        #     container_name = client.m_create_container("loadtest")['name']
        #
        #     annotation_names = []
        #     sample_size = len(sample)
        #     print(f"uploading {sample_size} annotations individually: (using mongodb)")
        #     start = time.perf_counter()
        #     for a in sample:
        #         try:
        #             annotation_data = client.m_add_annotation(container_name=container_name, content=a)
        #             annotation_name = annotation_data['id'].split('/')[-1]
        #             annotation_names.append(annotation_name)
        #         except Exception:
        #             print("something went wrong")
        #     end = time.perf_counter()
        #     duration = (end - start)
        #     avg = (duration / sample_size)
        #     averages[f"mongodb: {sample_size} individually"] = (duration, avg)
        #     print(
        #         f"uploading individually (using mongodb) took {duration:0.4f} seconds: {avg:0.4f} s/annotation")
        #
        #     print(f"uploading {sample_size} annotations in bulk (using mongodb):")
        #     start = time.perf_counter()
        #     # try:
        #     annotation_data = client.m_add_annotations(container_name, sample)
        #     # ic(annotation_data)
        #     # except:
        #     #     print("something went wrong")
        #     end = time.perf_counter()
        #     duration = (end - start)
        #     avg = (duration / sample_size)
        #     averages[f"mongodb: {sample_size} in bulk"] = (duration, avg)
        #     print(
        #         f"uploading in bulk (using mongodb) took {duration:0.4f} seconds: {avg:0.4f} s/annotation")
        #
        # finally:
        #     if args.delete_afterwards:
        #         print("removing test container + annotations (using mongodb)")
        #         for name in annotation_names:
        #             client.m_delete_annotation(container_name, name)
        #         client.m_delete_container(container_name)

        print(f"{Fore.BLUE}load test done!{Fore.RESET}")

        headers = ["method", "duration", "seconds/annotation"]
        table = [[label, value[0], value[1]] for label, value in averages.items()]
        print(tabulate(table, headers=headers, tablefmt="fancy_grid"))


if __name__ == '__main__':
    main()

# results:
# ╒══════════════════════════════════╤════════════╤══════════════════════╕
# │ method                           │   duration │   seconds/annotation │
# ╞══════════════════════════════════╪════════════╪══════════════════════╡
# │ postgres/es: 100000 individually │ 4782.98    │          0.0478298   │
# ├──────────────────────────────────┼────────────┼──────────────────────┤
# │ postgres/es: 100000 in bulk      │   98.4091  │          0.000984091 │
# ├──────────────────────────────────┼────────────┼──────────────────────┤
# │ mongodb: 100000 individually     │ 1998.15    │          0.0199815   │
# ├──────────────────────────────────┼────────────┼──────────────────────┤
# │ mongodb: 100000 in bulk          │    6.79403 │          6.79403e-05 │
# ╘══════════════════════════════════╧════════════╧══════════════════════╛
