import json
import logging

import pika

from message_handler.message_handler import MessageHandler
from initializer.initialization import apply_initialization

EXCHANGE_NAME = "initializer"


def receive_initialization_callback(channel, method, properties, body):
    logging.debug(body)  # TODO: remove
    amount = body.get("payload")
    logging.info("rMQ:{queue_}: Received initialization request for {amount_} individuals".format(
        queue_=EXCHANGE_NAME,
        amount_=amount,
    ))

    # TODO 106: generate individuals and retrieve the amount
    generated_individuals = apply_initialization(amount)

    remaining_destinations = body.get("destinations")
    send_message_to_queue(
        channel=channel,
        destinations=generated_individuals,
        payload=generated_individuals
    )


def send_message_to_queue(channel, destinations, payload):
    # This will create the exchange if it doesn't already exist.
    logging.debug(destinations)  # TODO: remove logs
    next_recipient = destinations.pop(index=0)
    logging.debug(destinations)

    # Route the message to the next queue in the model.
    channel.exchange_declare(exchange="", routing_key=next_recipient, auto_delete=True, durable=True)

    # Send message to given recipient.
    amount = payload  # TODO 106: generate individuals and retrieve the amount
    logging.info("rMQ: Sending {amount_} individuals to destinations {dest_}.".format(
        amount_=amount,
        dest_=destinations,
    ))
    channel.basic_publish(
        exchange="",
        routing_key=next_recipient,
        body=json.dumps({
            "destinations": destinations,
            "payload": payload
        }),
        # Delivery mode 2 makes the broker save the message to disk.
        # This will ensure that the message be restored on reboot even
        # if RabbitMQ crashes before having forwarded the message.
        properties=pika.BasicProperties(
            delivery_mode=2,
        ),
    )


class RabbitMessageQueue(MessageHandler):
    def __init__(self, pga_id):
        # Establish connection to rabbitMQ.
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host="rabbitMQ--{id_}".format(id_=pga_id),
            socket_timeout=30,
        ))

    def receive_messages(self):
        # Define communication channel.
        channel = self.connection.channel()

        # Create queue for initialization and bind it to broadcast exchange.
        queue = channel.queue_declare(auto_delete=True, durable=True)
        channel.queue_bind(queue, exchange=EXCHANGE_NAME)

        # Actively listen for messages in queue and perform callback on receive.
        channel.basic_consume(
            queue=queue,
            on_message_callback=receive_initialization_callback,
            auto_ack=True
        )
        logging.info("rMQ:{queue_}: Waiting for initialization requests.".format(
            queue_=EXCHANGE_NAME
        ))
        channel.start_consuming()

        # Close connection when finished. TODO: check if prematurely closing connection
        logging.info("rMQ: CLOSING CONNECTION")
        self.connection.close()

    def send_message(self, pair, remaining_destinations):
        # Define communication channel.
        channel = self.connection.channel()
        send_message_to_queue(
            channel=channel,
            destinations=remaining_destinations,
            payload=pair
        )
