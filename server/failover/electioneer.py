# coding=utf-8
# author=veficos

from kazoo.client import KazooClient
from threading import Thread


class ElectioneerKazooEngine(KazooClient):
    def __init__(self, timeout=10.0, *args, **kwargs):
        super(ElectioneerKazooEngine, self).__init__(timeout=timeout, *args, **kwargs)
        self.start(timeout)

    def __del__(self):
        self.stop()


class Electioneer(Thread):
    def __init__(self, engine, path, identifier, election_func, *args, **kwargs):
        super(Electioneer, self).__init__()
        self._election = engine.Election(path)
        self._identifier = identifier
        self._election_func = election_func
        self._args = args
        self._kwargs = kwargs

    def run(self):
        # blocks until the election is won, then calls
        # election_func()
        self._election.run(self._election_func,
                           *self._args,
                           **self._kwargs)


if __name__ == '__main__':
    import uuid
    import time

    my_id = uuid.uuid4()

    def leader_func():
        print("I am the leader {}".format(str(my_id)))
        while True:
            print("{} is working! ".format(str(my_id)))
            time.sleep(3)


    _engine = ElectioneerKazooEngine(hosts='192.168.10.139:31081')

    election = Electioneer(engine=_engine,
                           path='/election',
                           identifier=None,
                           election_func=leader_func)

    election.start()

    while True:
        time.sleep(30)

