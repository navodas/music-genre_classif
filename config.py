from configparser import ConfigParser


def config_reader(filename='database.ini', section='postgresql'):
    
    # create a parser
    parser = ConfigParser()

    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db_conn_dict = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            #print(param)
            #key:value update in the dict
            db_conn_dict[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))


    return db_conn_dict
