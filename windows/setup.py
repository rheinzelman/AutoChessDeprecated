import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = {"packages": ["os"], 'include_files': ["piece_images/", "src/", "gameEngine.py", "ioDriver.py"]}

# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="AutoChess",
    version="0.1",
    description="My Chess application!",
    options={"build_exe": build_exe_options},
    executables=[Executable("game.py", base=base)],
)