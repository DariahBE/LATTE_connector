import argparse
from neo4j import GraphDatabase
##function imported into main-files to extract the text:
#takes commandline arguments to log in in the NEO4J database.
#and returns the text based on a given NODE ID!
import os
import configparser


##read the config.ini file to extract additional languages: 
scriptdir = os.path.dirname(os.path.abspath(__file__))
config = configparser.ConfigParser()
config.read(os.path.join(scriptdir, '../config.ini'))



settings = {}
for section in config.sections():
    settings[section] = {}
    for key, value in config.items(section):
        settings[section][key.strip()] = value


def connect_and_extract(conndata):

    uri  = conndata['uri']          #
    db = conndata['database']       #
    usr = conndata['username']      #
    psw = conndata['password']      #
    node = conndata['nodeid']       #match on neo4J id(node)
    texnode = conndata['textlabel']
    texprop = conndata['textproperty']

    #creating connection object to the NEO4J database
    driver = GraphDatabase.driver(uri, max_connection_lifetime=3600, auth=(usr, psw))
    session = driver.session()

    #get the text from the database based on the node id.
    #TODO: use from config.ini the texnodelabel and texnodeproeprty!!
    queryTextById = "MATCH (n:"+texnode+") WHERE id(n) = $nodeID RETURN n."+texprop+" AS text LIMIT 1"
    textdata = session.run(queryTextById, nodeID=int(node))
    text = ''
    #iterate over the NEO4J results: (contains only one record - only way of accessing over the api though)
    for record in textdata:
        text = record['text']
    return text
