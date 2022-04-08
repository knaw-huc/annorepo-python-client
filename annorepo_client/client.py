class AnnoRepoClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    @staticmethod
    def hello(who: str):
        print(f"hello, {who}")
