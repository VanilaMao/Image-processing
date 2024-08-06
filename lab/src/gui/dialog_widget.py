class DialogWidget:
    def __init__(self) -> None:
        self._result = None

    def __getattr__(self, attr):
        if attr=="result":
            return self._result
        return super(DialogWidget, self).__getattribute__(attr)