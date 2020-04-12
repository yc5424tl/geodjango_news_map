from re import compile
import sys

class DBConnectionStr:
    """
    Formats:
        sqlite3://path/to/file
        dbtype://dbuser/dbname
        dbtype://dbuser:dbpassword/dbname
        dbtype://dbuser:dbpassword@dbhost/dbname
        dbtype://dbuser:dbpassword@dbhost:port/dbname
        dbtype://dbuser(ROLE):dbpassword@dbhost/dbname
    Example:
       c = DBConnection('sqlite3:///tmp/db.sqlite3')
    """
    def __init__(self, cstr):
        __re_dbstr = compile(r'^(?P<engine>[^:]+)://((?P<user>[^\(:]+)(\((?P<role>.+)\))?(:(?P<password>[^@]+))?(@(?P<host>[^\/:]+)(:(?P<port>\d+))?)?)?/(?P<name>.+)')
        try:
            print('line before self.__db assignment')
            self.__db = __re_dbstr.search(cstr).groupdict()
            print('line below should be self.__db value')
            print(f'{self.__db}')
            # Fix for sqlite path
            if self.__db['engine'].startswith('sqlite'):
                self.__db['name'] = "/%s" % self.__db['name']
        except:
            print(Exception)
            self.__db = {}
            #raise AttributeError #me
            #raise SomeException()

    def keys(self):
       return self.__db.keys()

    def items(self):
       return self.__db.items()

    def __getitem__(self, key):
        return self.__db.get(key, None)

    def __getattr__(self, key):
        return self.__db.get(key, None)

#c = DBConnectionStr('sqlite3:///:memory:')
#c = DBConnectionStr('sqlite3:///tmp/django.sqlite3')
#c = DBConnectionStr('mysql://user1/django')
#c = DBConnectionStr('mysql://user1:password1/django')
#c = DBConnectionStr('mysql://user1:password1@host1/django')
#c = DBConnectionStr('mysql://user1:password1@host1:1234/django')
#c = DBConnectionStr('postgresql://user1(role1):password1@host1/django')
# c = DBConnectionStr('postgresql://user1(role1):password1@host1:1234/django')
# for i in c.items():
#     print "%-8s: %s" % i
# or
#print c.engine, c.name

# engine  : postgresql
# name    : django
# host    : host1
# role    : role1
# user    : user1
# password: password1
# port    : 1234

def parse_connection_string():
    c = DBConnectionStr(cstr=sys.argv[1])
    print('next line is sys.argv[1]')
    print(f'{sys.argv[1]}')
    return [c.user, c.password, c.host, c.port, c.name]

if __name__ == '__main__':
    parse_connection_string()





