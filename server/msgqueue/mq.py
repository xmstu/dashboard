# conding=utf-8
# author=veficos


try:
    import simplejson as json
except ImportError:
    import json

from server import log

from kafka import KafkaConsumer, KafkaProducer
from kafka.coordinator.assignors.roundrobin import RoundRobinPartitionAssignor
from kafka.coordinator.assignors.range import RangePartitionAssignor


class ConsumerQueue(object):
    def __init__(self, bootstrap_servers, topic, group_id, client_id):
        self.client = KafkaConsumer(topic,
                                    client_id=client_id,
                                    group_id=group_id,
                                    bootstrap_servers=bootstrap_servers,
                                    partition_assignment_strategy=[RangePartitionAssignor,RoundRobinPartitionAssignor])

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            try:
                item = next(self.client)

                log.debug('获取到kafka消息: [topic: %s][partition: %s][offset: %s][key: %s][value: %s]' %
                          (item.topic, item.partition, item.offset, item.key, item.value))

                value = json.loads(item.value)
                return value
            except Exception as e:
                log.warn('获取到格式错误的消息：[error: %s]' % (e, ), exc_info=True)


class ProducerQueue(object):
    def __init__(self, bootstrap_servers):
        def partitioner(key_bytes, all_partitions, available_partitions):
            return int(key_bytes) % len(available_partitions)

        self.client = KafkaProducer(bootstrap_servers=bootstrap_servers,
                                    acks='all',
                                    partitioner=partitioner)

    def push(self, topic, msg):
        try:
            if isinstance(msg, dict):
                self.client.send(topic=topic, key=str(msg['id']).encode(), value=json.dumps(msg).encode())
            elif isinstance(msg, str):
                self.client.send(topic=topic, key=str(msg['id']).encode(), value=msg.encode())
            else:
                log.warn('推送的消息格式错误: [msg: %s][msg_type: %s]' % (msg, type(msg)))
        except Exception as e:
            log.warn('推送消息失败: [error: %s]' % (e, ), exc_info=True)
