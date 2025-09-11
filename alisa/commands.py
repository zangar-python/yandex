

class AlisaMethods():
    def __init__(self,user):
        self.user = user
        pass
    
    def command(self,command:str):
        if "find_user/" in command:
            return
        if "find_blog/" in command:
            return 
        if command.lower() == "hello":
            return
        if command.lower() == "commands":
            return
        if command.lower() == "my_account":
            return
        else:
            return