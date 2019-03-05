
#This controller is taken from Terrabit Solutions module 'Access Control MQTT'
# https://www.odoo.com/apps/modules/11.0/terrabit_access_control_mqtt/

import logging
import time
import json
from threading import Thread, Lock
import threading

try:
    from queue import Queue, Empty
except ImportError:
    from Queue import Queue, Empty  # pylint: disable=deprecated-module

from odoo.tools.config import config

_logger = logging.getLogger(__name__)

try:
    import paho.mqtt.client as mqtt

except (ImportError, IOError) as err:
    _logger.debug(err)


class MQTT(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.queue = Queue()
        self.lock = Lock()
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def lockedstart(self):
        with self.lock:
            if not self.isAlive():
                self.daemon = True
                self.start()

    def push_task(self, task, topic=None, data=None):
        self.lockedstart()
        self.queue.put((time.time(), task, topic, data))

    def run(self):
        while True:
            try:
                timestamp, task, topic, data = self.queue.get(True)
                if task == 'connect':
                    self.connect(data)
                elif task == "start":
                    self.start_mtqq()
                elif task == "stop":
                    self.stop_mtqq()
                elif task == 'subscribe':
                    self.subscribe(topic)
                elif task == 'publish':
                    self.publish(topic, data)
            except Exception as e:
                _logger.error('Error: %s' % str(e))

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        _logger.info("Connected with result code " + str(rc))

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        _logger("INFO: llegó un mensaje!")
        _logger.info("Mensaje: " + msg.topic + " " + str(msg.payload))
    #data es un diccionario que tiene el host, el puerto y el ttl
    def connect(self, data):
        self.client.connect(data['host'], data['port'], data['ttl'])

    def start_mtqq(self):
        self.client.loop_start()
        _logger.info('MQTT Interface Started')

    def stop_mtqq(self):
        self.client.loop_stop()
        _logger.info('MQTT Interface Stop')

    def subscribe(self, topic):

        _logger.info('MQTT subscribe %s' % topic)
        self.client.subscribe(topic)

    def publish(self, topic,  data):

        _logger.info('MQTT publish %s' % topic)
        self.client.publish(topic, str(json.dumps(data)).strip().strip('"'))

interface = MQTT()
