import sys
from cx_Freeze import Executable, setup
options = {
    'build_exe': {'path': sys.path + ['modules']}
}
setup(name='miner',
version = '1.0', 
description= 'miner app',
options=options,
executables= [Executable("app.py"), Executable("Block.py"), Executable("Worker.py")])