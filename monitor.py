#!/usr/bin/python

import os,sys,time
import parser,util
import logging,logging.config
import mysql
import emailex
from datetime import datetime

reload(sys)   
sys.setdefaultencoding('utf8')


class Monitor:
    conf={}

    def run(self):
        self.load_conf()
        self.process()

    def process(self):
        task = self.conf.get("task")
        self.handle_response(mysql.handle(task, self.conf))
        logging.debug("task completed")

    def handle_response(self,args):
        emailex.response(args, self.conf)

    def load_conf(self):
        try:
            config_name = "monitor.conf"
            if len(sys.argv) > 1:
                config_name = sys.argv[1] + ".conf"

            conf_path = os.path.join(sys.path[0], "conf", config_name)
            logging.debug("config file path:" + conf_path)
            if os.path.exists(conf_path):
                self.conf = parser.parse_conf(conf_path)
            else:
                logging.critical("no config file name:" + config_name)
                sys.exit(1)
        except Exception,e:
            logging.critical('parse configure file failed {0}'.format(str(e)))
            sys.exit(1)

if __name__ == '__main__':
    logging_config_path = os.path.join(sys.path[0], "logging.conf")
    logging.config.fileConfig(logging_config_path)

    if len(sys.argv) < 2:
        logging.info("no define config name")

    m = Monitor()
    m.run()

    sys.exit(0)

