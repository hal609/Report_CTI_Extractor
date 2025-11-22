class ANSI:
    ESCAPE = "\033["
    STOP = "\033[0m"
    CODE = ""
    
    def __init__(self, text:str):
        self.text = text
        # self.code = ""
    
    def __repr__(self):
        return f"{self.ESCAPE}{self.CODE}m{self.text}{self.STOP}"

class RESET(ANSI): 
    CODE = "0"
    STOP = "\033[0m"
class BOLD(ANSI):
    CODE = "1"


print("\033[0m", end="")
# print([char for char in (str(BOLD("Text")))])
print(BOLD("Text"))
# ['\x1b', '[', '3', '2', 'm', 'T', 'e', 'x', 't', '\x1b', '[', '0', 'm']
print("\x1b[32mText\x1b[0m")