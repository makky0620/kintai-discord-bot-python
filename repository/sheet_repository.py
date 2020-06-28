from repository.sheet_dao import SheetDao


class SheetRepository:
    def __init__(self):
        self.sheet_dao = SheetDao()

    def find_sheet(self):
        return self.sheet_dao.find_sheet()

    def find_by_id(self, user_id):
        pass

    def register(self, record):
        self.sheet_dao.register(record)

    def update_by_id(self, user_id, record):
        self.sheet_dao.update_by_id(user_id, record)
