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


def connect_and_extract(returnLang):
    parser=argparse.ArgumentParser()
    parser.add_argument('--uri', help = 'Endpoint URI of the NEO4J database.')
    parser.add_argument('--username', help = 'NEO4J username.')
    parser.add_argument('--password', help = 'NEO4J password.')
    parser.add_argument('--database', help = 'NEO4J database.')
    parser.add_argument('--nodeid', help = 'NEO4J nodeID containing the text.')
    parser.add_argument('--extractor', help = 'Which language detection engine should be used.')
    parser.add_argument('--textlabel', help = 'The label used to identify texts in your nodemodel.')
    parser.add_argument('--textproperty', help = 'The property used in your textnode to store the text.')
    if returnLang:
        parser.add_argument('--lang', help = 'NEO4J nodeID containing the text.')

    #set empty defaults
    text = ''
    lang = ''
    engine = 'spacy'

    args = parser.parse_args()
    data = vars(args)
    uri  = data['uri']          #
    db = data['database']       #
    usr = data['username']      #
    psw = data['password']      #
    node = data['nodeid']       #match on neo4J id(node)
    engine = data['extractor']
    texnode = data['textlabel']
    texprop = data['textproperty']
    if returnLang:
        lang = data['lang']
    #creating connection object to the NEO4J database
    driver = GraphDatabase.driver(uri, max_connection_lifetime=3600, auth=(usr, psw))
    session = driver.session()

    #get the text from the database based on the node id.
    #TODO: use from config.ini the texnodelabel and texnodeproeprty!!
    queryTextById = "MATCH (n:"+texnode+") WHERE id(n) = $nodeID RETURN n."+texprop+" AS text LIMIT 1"
    textdata = session.run(queryTextById, nodeID=int(node))

    #iterate over the NEO4J results: (contains only one record - only way of accessing over the api though)
    for record in textdata:
        text = record['text']
    return [text, lang, engine]
