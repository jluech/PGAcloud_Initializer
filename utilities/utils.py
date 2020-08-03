import logging
import os
from re import match

import yaml

__CONTAINER_CONF = None
__PROPERTIES = {}


def parse_yaml(yaml_file_path):
    with open(yaml_file_path, mode="r", encoding="utf-8") as yaml_file:
        content = yaml.safe_load(yaml_file) or {}
    return content


def get_messaging_source():
    if not __CONTAINER_CONF:
        __retrieve_container_config()
    return __CONTAINER_CONF["source"]


def get_messaging_target():
    if not __CONTAINER_CONF:
        __retrieve_container_config()
    return __CONTAINER_CONF["target"]


def get_pga_id():
    if not __CONTAINER_CONF:
        __retrieve_container_config()
    return __CONTAINER_CONF["pga_id"]


def __retrieve_container_config():
    # Retrieve locally saved config file.
    files = [f for f in os.listdir("/") if match(r'[0-9]+--initializer-config\.yml', f)]
    # https://stackoverflow.com/questions/2225564/get-a-filtered-list-of-files-in-a-directory/2225927#2225927
    # https://regex101.com/

    if not files.__len__() > 0:
        raise Exception("Error retrieving the container config: No matching config file found!")
    config = parse_yaml("/{}".format(files[0]))
    global __CONTAINER_CONF
    __CONTAINER_CONF = {
        "pga_id": config.get("pga_id"),
        "source": config.get("source"),
        "target": config.get("target")
    }
    logging.info("Container config retrieved: {conf_}".format(conf_=__CONTAINER_CONF))


def get_property(property_key):
    return __PROPERTIES[property_key]


def set_property(property_key, property_value):
    __PROPERTIES[property_key] = property_value
    logging.info("Successfully set property '{prop_}'={val_}".format(
        prop_=property_key,
        val_=__PROPERTIES[property_key],
    ))
