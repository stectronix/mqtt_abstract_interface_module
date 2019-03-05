=========================================
Documentation for Mqtt Abstract Interface
=========================================

Contents:
---------
- How works this module?
- Requirements
- What contains this module?
- What must I implement?
- How use it?
- State of the module and future updates.

-----------------------------------

How works this module?
----------------------

| This is a Abstract technical module for **Developers**,
  that allows other models / modules to have Mqtt communication with
  devices through a broker.
|
| For this, the module that must have connectivity through
  mqtt, must inherit this interface in one of its models
  and implement the methods that will be described later in the documentation.

Requirements
------------

This module require external dependencies:

- Paho-mqtt_ library for python (install with pip).
- A Broker server (like Mosquitto_)

.. _Paho-mqtt: https://pypi.org/project/paho-mqtt/
.. _Mosquitto: https://mosquitto.org/


What contains this module?
--------------------------

This model only contains two files:

Main.py:
    |
    | This python file acts as a controller for the MqttAbstractInterface model,
      it contains all the methods necessaries to connect to a broker
      and subscribe to topics.
    | The controller start a thread, that receives "tasks"
      from the model (subscribe, publish, connect, etc..) and put them
      in a queue where they are executed one by one by the model.
    |

Mqtt_abstract_interface_model.py:
    |
    | This file contains the MqttAbstractInterface class (the abstract model)
      that is inherited by another's models. This class has 3 methods that
      requires implemententation:

    - on_message(self, client, userdata, msg):
        This method is a callback executed when there are a incoming
        message from a topic, this message contain a
        payload (msg.payload) that must by processed in this method
        to extract the necessaries parameters and pass it to the
        "create record" method.
    - create_record(self, values):
        This method is responsible for the creation of records in
        the database, from the "values" dictionary that contains the
        data needed for the model.
    - mqtt_publish(self, toic, message):
        This is a optional method for adding functionalities to the
        original "publish" method (It's necessary include the original
        method)

What must I implement?
----------------------

In addition to the methods already mentioned it's necessary serve the broker
and create an automated action with the model that inherit the abstract
interface which includes the followings methods:

- action_start_mqtt(self):
    | This method initiates the mqtt client in a thread and starts a connection
      with the broker. The defaults values are:

            | Server : locallhost
            | Port : 1883
            | Ttl :60

    | **The changes in this values must be done directly in the font code.**

- subscribe(self, topic):
    This method subscribes the client to a topic, the "topic" parameter is
    optional, with default value '#' (for subscribe to **all** topics.

How use it
----------

It can be easily initialized:

1. Download and install paho-mqtt library.
2. Extend your custom model with the abstract interface.
3. Implement the methods previously described.
4. Create automatized actions to start Mqtt and subscribes topics

State of the module and future updates.
---------------------------------------

| This technicall module is a beta version and many features will be
  impleted in the future.
| Some of this features will be:

    - Multi connection to brokers and a manage wizard for its.
    - Auto creation of the automatized action.
