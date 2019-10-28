import pickle

class User:
    def __init__(self, kiuid):
        self._tickets = []
        self.kiuid = kiuid
        self.to_file()
    def add_ticket(self, ticket):
        self._tickets.append(ticket)

    @classmethod
    def from_file(cls, id):
        user = None
        try:
            with open('objects/users/%s.pkl'%id, 'rb') as fr:
                user = pickle.load(fr)
                fr.close()
        except FileNotFoundError:
            return None
        return user
        
    
    def to_file(self):
        with open('objects/users/%s.pkl'%self.kiuid, 'wb') as fw:
            pickle.dump(self, fw)
            fw.close()

