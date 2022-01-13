#!/usr/bin/env python3
import argparse
import logging

import paho.mqtt.client as mqtt

parser = argparse.ArgumentParser(
    description="Subscribe to an MQTT topic and log the messages."
)
parser.add_argument(
    "-H",
    "--host",
    default="test.mosquitto.org",
    help="The broker host. Default: %(default)s",
)
parser.add_argument(
    "-p", "--port", default=1883, type=int, help="The broker port. Default: %(default)s"
)
parser.add_argument(
    "-u", "--username", default=None, help="The broker username. Default: %(default)s"
)
parser.add_argument(
    "-P", "--password", default=None, help="The broker password. Default: %(default)s"
)
parser.add_argument(
    "-t",
    "--topic",
    default="$SYS/#",
    help="The topic to subscribe to. Default: %(default)s",
)
parser.add_argument(
    "-q",
    "--qos",
    default=0,
    type=int,
    help="The QoS level to request. Default: %(default)s",
)
parser.add_argument(
    "-l",
    "--logfile",
    default=None,
    help="The logfile to write to. Default: %(default)s (stdout)",
)
parser.add_argument("--tls", action="store_true", help="Use TLS")
args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG, filename=args.logfile)
logger = logging.getLogger("mqtt_logger")


def on_message(client, userdata, msg):
    logger.info("Received message: (%s) %s", msg.topic, msg.payload)


mqttc = mqtt.Client()
mqttc.enable_logger(logger)
mqttc.on_message = on_message

if args.username:
    mqttc.username_pw_set(args.username, args.password)
if args.tls:
    import certifi

    mqttc.tls_set(certifi.where())

mqttc.connect(args.host, args.port, 60)
mqttc.subscribe(args.topic, args.qos)
mqttc.loop_forever()
