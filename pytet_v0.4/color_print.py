class TextColor():
    red    = "\033[31m"
    green  = "\033[32m"
    yellow = "\033[33m"
    blue   = "\033[34m"
    purple = "\033[35m"
    cyan   = "\033[36m"
    white  = "\033[37m"
    pink   = "\033[95m"
### end of class TextColor():

print(TextColor().red    + '■', end='')
print(TextColor().green  + '■', end='')
print(TextColor().yellow + '■', end='')
print(TextColor().blue   + '■', end='')
print(TextColor().purple + '■', end='')
print(TextColor().cyan   + '■', end='')
print(TextColor().white  + '■', end='')
print(TextColor().pink   + '■', end='')
print()
