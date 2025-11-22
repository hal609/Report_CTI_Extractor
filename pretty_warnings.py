import os, sys, warnings, traceback
from colorist import Color, Effect, ColorRGB, effect_bold, BrightColor, BgColor, print_color, style_text

# def apply_styles(text:str, *args):
#     return "".join(map(str, args)) + text + Color.OFF
    
def ANSI(code, data=""):
    return f'\x1b[{code}m{data}\x1b[0m'

def warn(message, warn_type):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    frame = exc_traceback.tb_frame
    # print(frame.f_code.co_filename)
    # print(frame.f_lineno)
    line_of_code = traceback.extract_tb(exc_traceback)[0].line
    # print(line_of_code)
    o = f'  File "{frame.f_code.co_filename}", line {frame.f_lineno}\n'
    o += f'     {line_of_code}\n'
    o += f'{effect_bold(warn_type, Color.YELLOW)}: {message}'
    print(o)

def error_causer():
    int("sd")

def test_func_caller():
    error_causer()

def catcher():
    try:
        test_func_caller()
    except Exception as e:
        warn("This warning is present", "TestWarning")
        
def raise_warning(warning_type, message):
    print_color(warning_type, Color.YELLOW, effect=Effect.BOLD)
    print_color(message, Color.MAGENTA)
    text = style_text(warning_type, Color.YELLOW, Effect.BOLD) + \
          style_text(message, Color.MAGENTA)
    print(style_text("Warning", Color.YELLOW, Effect.BOLD) + 
        style_text("Example warning", Color.MAGENTA))
    print(f"{Color.YELLOW}{Effect.BOLD}Warning:{Color.OFF}{Effect.OFF}\
          {Color.MAGENTA}Example warning{Color.OFF}")
    
dusty_pink = ColorRGB(194, 145, 164)

print("\033[0m", end="")
# print(dusty_pink.join(["a", "b"]))
# catcher()
# effect_bold("Test1")
# print(f"{effect_bold("Test2")}")
# print(apply_styles("Test",  BgColor.GREEN, BrightColor.YELLOW, Effect.BOLD))
# print_color("Test",  BgColor.GREEN, Effect.BOLD)
# print([char for char in f"{Color.GREEN}Text{Color.OFF}"])
# print(f"I want {Effect.BOLD}emphasized {Color.GREEN}text{Effect.BOLD_OFF}and{Color.OFF}stuff.")
# print(f"I want {Effect.BOLD}emphasized {Color.GREEN}text{Effect.BOLD_OFF}and{Color.OFF}stuff.")
# print(f"{BgColor.GREEN}{Color.YELLOW}I want yellow text on a green background{Color.OFF}")
# print(f"I want {apply_styles(f"emphasized {apply_styles("text", Color.GREEN)}", Effect.BOLD)} {apply_styles("and", Color.GREEN)} stuff.")
print(f"{Effect.BOLD}Bold text with a {Color.RED}red{Color.OFF} word.{Effect.OFF}")
print(style_text(f"Bold text with a {style_text("red")} word."))
raise_warning("TestWarning", "This is a warning")
print("Normal text")