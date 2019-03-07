from odoo import models, fields, api, sql_db
import logging, time

from ..controllers.main import interface

_logger = logging.getLogger(__name__)


class MqttAbstractInterface(models.AbstractModel):
    controller = interface
    _name = "mqtt.abstract.interface"
    _description = "Provides Mqtt functionalities to another models."
    host = "localhost"
    port = 1883
    ttl = 60
    conect = False

    data = {'host': host, 'port': port, 'ttl': ttl}

    #method to start mqtt service and connect to a broker server
    #this method require a automatic acction in the inherited model
    @api.multi
    def action_start_mqtt(self, topic='#'):
        if self.conect == False:
            type(self).conect = True
            self.controller.client.on_message = self.on_message
            self.controller.push_task('connect', data=self.data)
            self.controller.push_task('start')
            self.subscribe(topic)
        elif self.conect:
            _logger.info("INFO: already connect to a mqtt broker!")

    @api.multi
    def publish(self, topic, msg):
        self.controller.push_task('publish', topic, msg)

    #method to stop mqtt service
    @api.multi
    def action_stop_mqtt(self):
        self.controller.push_task('stop')

    #method for subscribe to a Mqtt topic   
    @api.multi
    def subscribe(self, topic='#'):
        time.sleep(2)
        self.controller.push_task('subscribe', topic)

    def on_disconnect(self, client, userdata, rc):
        type(self).conect = False
        _logger.info("MQTT Client: Unexpected disconnection.")


# Methods that require implementation in the class that inherits

    #this callback throws when a message it's comming from a subscribe topic
    @api.multi
    def on_message(self, client, userdata, msg):
        _logger.info("WARNING: I need implementation!")

    # this method must be call in on_message, to create a record in a table.
    # Values its a dictionary with the parameters that comes in the payload message
    # the values must be the necesaries to create a new record in the model
    @api.model
    def create_record(self, values):
        _logger.info("WARNING: I need implementation!")

    #this method is optional, to extend the original publish method.
    @api.multi
    def mqtt_publish(self, toic, message):
        _logger.info("WARNING: I need implementation!")
