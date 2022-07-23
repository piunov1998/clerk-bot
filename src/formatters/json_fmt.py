import json


def json_dumps(*args, **kwargs) -> str:
    kwargs.update(ensure_ascii=False)
    return json.dumps(*args, **kwargs)


class JsonDump(json.JSONEncoder):

    def __init__(self):
        super().__init__()
        self.ensure_ascii = False
