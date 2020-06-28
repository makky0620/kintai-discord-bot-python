from repository.sheet_repository import SheetRepository
import datetime


class KintaiService:
    def __init__(self):
        self.sheet_repository = SheetRepository()

    def start(self, member, voice_state):
        record = self.to_start_record(member, voice_state)
        self.sheet_repository.register(record)

    def end(self, member, voice_state):
        record = self.to_end_record(member, voice_state)
        self.sheet_repository.update_by_id(member.discriminator, record)
        
        pass

    def to_start_record(self, member, voice_state):
        return {
            'user_id': member.discriminator,
            'user': member.name,
            'start': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'end': '',
            'room': voice_state.channel.name
        }
    
    def to_end_record(self, member, voice_state):
        return {
            'end': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'room': voice_state.channel.name
        }
