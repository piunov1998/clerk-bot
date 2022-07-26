import json


def json_dumps(*args, **kwargs) -> str:
    kwargs.update(ensure_ascii=False)
    return json.dumps(*args, **kwargs)


class JsonDump(json.JSONEncoder):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ensure_ascii = False
