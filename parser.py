import os,json,logging
import json

def parse_conf(FileName='./conf/conf.example'):
    with open(FileName) as setting_file:
        lines=map(filter_comment,setting_file.readlines())
        setting_str = ''.join(lines)
        logging.debug('configure file :\n%s'%(setting_str))
        return json.loads(setting_str)

def filter_comment(Line):
    if '#' in Line:
        if Line.index('#') == 0:
            return '\n'
        elif Line.split("#")[0].count('"') % 2 == 0 and Line.split("#")[0].count("'") %2 == 0:
            return Line.split('#')[0] + '\n'

    return Line
