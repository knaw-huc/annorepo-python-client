import subprocess
import sys

project_init_file = 'annorepo_client/__init__.py'


def hello(who=None):
    if not who:
        who = sys.argv[1]
    print(f"Hello, {who}")


def update_version(argv=None):
    if not argv:
        argv = sys.argv
    parameter = argv[1]
    result = subprocess.run(["poetry", "version", parameter], capture_output=True)
    stdout_decode = result.stdout.decode().strip()
    print(stdout_decode)
    new_version = stdout_decode.split()[-1]
    with open(project_init_file) as f:
        lines = f.readlines()
    with open(project_init_file, 'w') as f:
        init_has_version = False
        for l in lines:
            if l.startswith('__version__'):
                init_has_version = True
                f.write(f"__version__ = '{new_version}'\n")
            else:
                f.write(l)
        if not init_has_version:
            f.write(f"__version__ = '{new_version}'\n")
