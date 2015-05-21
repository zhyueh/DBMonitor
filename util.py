import logging

def is_match_pattern(string,pattern):
    str_items = string.split(' ')
    str_patterns=pattern.split(' ')
    if len(str_items) <> len(str_patterns):
        logging.error("length of %s is not equal as %s "%(string,pattern))
        return False
    else:
        result = True
        for index in range(len(str_items)):
            result = result and is_match_item(str_items[index],str_patterns[index])
            if result == False:
               break
        logging.debug("%s vs %s : %s"%(string,pattern,result))
        return result

def is_match_item(string,pattern):
    if pattern== "*":
        return True
    else:
        iTarget = int(string)
        if '[' in pattern:
            #trim [ and ]
            new_pattern = pattern.rstrip(']').lstrip('[')
            logging.debug("new pattern :%s"%(new_pattern))
            if ',' in new_pattern:
                return iTarget in map(int,new_pattern.split(','))
            elif '-' in new_pattern:
                mm = map(int,new_pattern.split('-'))
                return iTarget <= mm[1] and iTarget >= mm[0]
        else:
            return int(pattern) == iTarget

    return False

def format_datatable(dt):
    field_names = dt.get("header")
    if field_names == 0 or len(field_names) == 0:
        return ""

    ds = dt.get("rows")

    t_str= '<table border="1">'
    t_str = t_str + '<tr>'
    for i,title in enumerate(field_names):
        t_str = t_str + '<td>' + title + '</td>'
    t_str = t_str + '</tr>'
                                
    for row in ds:
        t_str = t_str + '<tr>'
        for i,column in enumerate(row):
            t_str = t_str + '<td>' + str(column) + '</td>'
        t_str = t_str + '</tr>'
                                                                                
    t_str= t_str + '</table>'
    return t_str

def dict_required(dic,fields):
    results = map(dic.has_key,fields)
    has_all = True
    for index,b in enumerate(results):
        if b == False:
            logging.error("do not has key:%s in dic:%s"%(fields[index],dic))
            has_all = False

    return has_all

def has_module_fun(module_name,fun_name):
    if module_name == "pass":
        logging.debug("pass module")
        return False
    try:
        obj = __import__(module_name)
        return hasattr(obj,fun_name)
    except:
        logging.error("can not import %s.%s"%(module_name,fun_name))
    return False 

def get_module_fun(module_name,fun_name):
    obj = __import__(module_name)
    return getattr(obj,fun_name)
