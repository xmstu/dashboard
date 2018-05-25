

from superconf.superconf import SuperConf
from superconf.kazooengine import KazooEngine
from superconf.jsonserialize import JsonSerialize
from superconf.jsonformatter import JsonFormatter

if __name__ == '__main__':
    conf = SuperConf(serialize=JsonSerialize(),
                     engine=KazooEngine(hosts='192.168.130.2:2181'))

    @conf.register('.production')
    def production(conf):
        print(JsonFormatter().dump(conf))

    @conf.register('.production.read_db')
    def production_read_db(conf):
        print(JsonFormatter().dump(conf))

    @conf.register('.production.write_db')
    def production_write_db(conf):
        print(JsonFormatter().dump(conf))

    @conf.register('.development')
    def development(conf):
        print(JsonFormatter().dump(conf))

    @conf.register('.development.read_db')
    def development_reload_db(conf):
        print(JsonFormatter().dump(conf))

    @conf.register('.development.write_db')
    def development_write_db(conf):
        write_db_conf = dict(conf)
        print(JsonFormatter().dump(conf))

    @conf.register('.')
    def root(conf):
        print(JsonFormatter().dump(conf))



    print(conf)
    print(conf.remote)
    print(conf.remote.production)
    print(conf.remote.development.read_db)
    print(conf.remote.development.get())
    print(conf.remote.development.get('read_db'))

    input('press any key to continue!')
