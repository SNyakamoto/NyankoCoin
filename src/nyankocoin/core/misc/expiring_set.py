from collections.abc import Set

import simplejson as json

from nyankocoin.core.misc import ntp, logger


class ExpiringSet(Set):
    def __init__(self, expiration_time, filename=None):
        super().__init__()
        self.expiration_time = expiration_time
        self._data = dict()
        self._filename = filename
        self._load()

    def __contains__(self, x: object) -> bool:
        self._refresh()
        return x in self._data

    def __len__(self) -> int:
        self._refresh()
        return len(self._data)

    def __iter__(self):
        self._refresh()
        return self._data.keys().__iter__()

    def add(self, x):
        current_time = ntp.getTime()
        self._data[x] = current_time + self.expiration_time
        self._store()

    def _refresh(self):
        current_time = ntp.getTime()

        len_before = len(self._data)
        self._data = {k: v for k, v in self._data.items() if v > current_time}
        len_after = len(self._data)

        if len_before != len_after:
            self._store()

    def _store(self):
        if self._filename is not None:
            try:
                with open(self._filename, 'w') as f:
                    json.dump(self._data, f)
            except Exception as e:
                logger.error("not possible to save banned peers")
                logger.exception(e)

    def _load(self):
        if self._filename is not None:
            try:
                with open(self._filename, 'r') as f:
                    self._data = json.load(f)
                self._refresh()
            except FileNotFoundError:
                self._data = dict()