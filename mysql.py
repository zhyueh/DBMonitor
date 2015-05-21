import MySQLdb,traceback
import logging
import sys

def handle(task,settings={}):
    try:
        if task.has_key("sql"):
            with get_conn(settings.get("db_settings")) as cursor:
                sql = task.get("sql")
                logging.debug("execute sql " + sql)
                return process(task,cursor,sql)
        else:
            logging.error("task: do not have sql")
    except Exception, e:
        str_exc = traceback.format_exc()
        logging.error("task occur exception:\n%s"%(str_exc))
    sys.exit(1)

def get_conn(db_setting):
    _host = db_setting.get('host',"localhost")
    _user = db_setting.get("user","root")
    _password = db_setting.get("password","root")
    _select_db = db_setting.get("select_db","mysql")
    _charset = db_setting.get("charset","utf8")

    return MySQLdb.connect(host=_host, user=_user, passwd=_password, db=_select_db, charset=_charset)

def process(task,cursor,sql):
    logging.debug("query sql:%s"%(sql))
    count = cursor.execute(sql)
    return response(count,cursor,task)


def response(count,cursor,task):
    logging.debug("after process,count:%d"%(count))
    _response_args = format_dataset([ i[0] for i in cursor.description],cursor.fetchall()) 

    logging.debug("resposne %s after query"%(_response_args))
    return _response_args

def format_dataset(header,rows):
    return {"header":header,"rows":rows}
