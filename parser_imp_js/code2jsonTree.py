import subprocess
import json
from utils import log
logger = log.setup_custom_logger("extractExpression")

def getTreeJson(expresstion_str):
    import os
    beforedir = os.getcwd()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)
    commands = ['node', f'code2jsonTreePy.js', '-e', expresstion_str]
    result = subprocess.run(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    result = result.stdout
   # print(result)
    os.chdir(beforedir)
    #print(result)
    # logger.info(expresstion_str)
    # logger.info(result)
    return json.loads(result)

