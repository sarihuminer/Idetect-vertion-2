# Imports the Google Cloud client library
from google.cloud import datastore
import json


def connect_to_sql(site, con):
    print("connect to sql site{} confif {}".format(site, con))
    # Instantiates a client
    datastore_client = datastore.Client()
    # The kind for the new entity
    kind = 'configuration'
    # The name/ID for the new entity
    id = site
    # The Cloud Datastore key for the new entity
    task_key = datastore_client.key(kind, id)

    # Prepares the new entity
    task = datastore.Entity(key=task_key)
    # divide the fiels to all cards
    con = json.loads(con)
    # with open('C:\\Users\\sari\\Documents\\IDetectaml\\server\\pasport_card_config.json')as passport:
    # passport = json.load(passport)
    # for value in con.values():
    keys = con.keys()
    passportCard = {}
    visaUsa = {}
    greenCard = {}
    if 'Card no' in keys:
        passportCard['Passport Card no'] = con['Card no']
        visaUsa['Passport Number'] = con['Card no']
    if 'Nationality' in keys:
        passportCard['Nationality'] = con['Nationality']
        visaUsa['Nationality'] = con['Nationality']
    if 'Last name' in keys:
        passportCard['Surname'] = con['Last name']
        visaUsa['Surname'] = con['Last name']
        greenCard['Surname'] = con['Last name']
    if 'First name' in keys:
        passportCard['Given Names'] = con['First name']
        visaUsa['Given Name'] = con['First name']
        greenCard['Given Name'] = con['First name']
    if 'Sex' in keys:
        passportCard['Sex'] = con['Sex']
        visaUsa['Sex'] = con['Sex']
        greenCard['Sex'] = con['Sex']
    if 'Date of Birth' in keys:
        passportCard['Date of Birth'] = con['Date of Birth']
        visaUsa['Birth Date'] = con['Date of Birth']
        greenCard['Date of Birth'] = con['Date of Birth']
    if 'Date of expiration' in keys:
        passportCard['Expires on'] = con['Date of expiration']
        visaUsa['Expiration Date'] = con['Date of expiration']
        greenCard['Card Expires'] = con['Date of expiration']
    if 'Place of Birth' in keys:
        passportCard['Place of Birth'] = con['Place of Birth']
        greenCard['Country of Birth'] = con['Place of Birth']
    if 'Age' in keys:
        passportCard['Age'] = con['Age']
        visaUsa['Age'] = con['Age']
        greenCard['Age'] = con['Age']
    if 'FullName' in keys:
        passportCard['FullName'] = con['FullName']
        visaUsa['FullName'] = con['FullName']
        greenCard['FullName'] = con['FullName']
    # keys=json_file.keys()

    task['passportCard'] = passportCard
    task['visaUsa'] = visaUsa
    task['greenCard'] = greenCard
    # Saves the entity
    datastore_client.put(task)
    # print('Saved {}: passport /n visaUsa {}'.format(task.key.name, task['passport'],task['visaUsa']))


def check_sql(site_name):
    # The kind for the new entity
    kind = 'configuration'
    # The name/ID for the new entity
    site = str(site_name)
    datastore_client = datastore.Client()
    key = datastore_client.key(kind, site)
    conf = datastore_client.get(key)
    if conf == None:
        return "false"
    return "true"


def get_config(site, type_certificate):
    datastore_client = datastore.Client()
    # The kind for the new entity
    kind = 'configuration'
    # The name/ID for the new entity
    id = site
    key = datastore_client.key(kind, site)
    conf = datastore_client.get(key)

    if conf == None:
        return None
    return conf[type_certificate]
