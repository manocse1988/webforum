"""
Author: Manoj Kumar Panneer Selvam
Purpose: This module has logic to connect and disconnect to Postgresql DB using json file with connection parameters
"""

import json
import psycopg2

def fconnect():
    config = {}
    with open("../src/config/connect.json","r") as configfile:
        configdata = json.load(configfile)

    connectionparam = psycopg2.connect(database = configdata["database"],
                                       user = configdata["user"],
                                       password = configdata["password"],
                                       host = configdata["host"],
                                       port = configdata["port"])
    return connectionparam


def fdisconnect(connectionparam):
    connectionparam.close()