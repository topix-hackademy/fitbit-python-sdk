import logging, os, sys, json
from configparser import ConfigParser
from os.path import expanduser


class Config(object):

    _instance = None

    client_id = ""
    client_secret = ""

    def __init__(self):
        # singleton init
        if not self._instance:
            self._instance = super(Config, self).__init__()

        # load configuration from file
        try:
            parser = ConfigParser()
            parser.read(os.path.dirname(os.path.realpath(__file__))+"/config.ini")

            self.client_id = parser.get('fitbit', 'client_id')
            self.client_secret = parser.get('fitbit', 'client_secret')

        except Exception, message:
            sys.exit(message.message + "\n" + configuration_error_message())

    def print_configuration(self):
        logging.info("""
Loaded config:
[fitbit]
{client_id}
{client_secret}
""".format(client_id=self.client_id,
           client_secret=self.client_secret,
           ))


def configuration_error_message():
    return """Your configuration file is absent or incorrect.
Please create a config.ini file with the following structure:

    [fitbit]
    client_id = "..."
    client_secret = "..."
"""
