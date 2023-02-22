#!/usr/bin/env python3
from annorepo.client import AnnoRepoClient


def main():
    print("""class ContainerAdapter:

    def __init__(self, ar_client: AnnoRepoClient, container_name: str):
        self.client = ar_client
        self.container_name = container_name
""")
    for name, obj in vars(AnnoRepoClient).items():
        if not name.startswith("_"):
            function_parameters = [(pname, pclass.__name__) for (pname, pclass) in obj.__annotations__.items()]

            if function_parameters:
                par_str = ", ".join(
                    f"{t[0]}:{t[1]}" for t in function_parameters if t[0] not in ["return", "container_name"])
                if par_str:
                    par_str = ", " + par_str

                return_instruction = ""
                if "return" in obj.__annotations__:
                    return_class = obj.__annotations__["return"]
                    return_instruction = f" -> {return_class.__name__}"

                call_params = ", ".join([f"{t[0]}={t[0]}" for t in function_parameters if t[0] != "return"]) \
                    .replace("=container_name", "=self.container_name")
                print(f"    def {name}(self{par_str}){return_instruction}:")
                print(f"        return self.client.{name}({call_params})")
                print()


if __name__ == '__main__':
    main()
