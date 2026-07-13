from repositories import JsonRepository


class BaseService:
    def __init__(self):
        self.repo = JsonRepository()