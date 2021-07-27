from .base_session import BaseSession


class EmptySession(BaseSession):
    def auth(self, *args):
        pass
