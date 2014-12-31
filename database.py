import sys
import models
from app import db
import json
import time
from datetime import datetime
from sqlalchemy import *


def upload_messages(userId, messageList):

    for message in messageList:
        direction     = message["direction"]
        phoneNumber   = message["phoneNumber"]
        timestamp     = message["timestamp"]
        messageLength = message["messageLength"]

        message_obj = models.Message(userId, direction, phoneNumber, timestamp, messageLength)
        db.session.add(message_obj)

    db.session.commit()


def upload_contacts(userId, contactList):

    for contact in contactList:
        phoneNumber = contact["phoneNumber"]
        contactType = contact["contactType"]

        contact_obj = models.Contacts(userId, phoneNumber, contactType)
        db.session.add(contact_obj)

    db.session.commit()


def process(db, userId):
    print "before populate contacts"
    contacts = populate_contacts(db, userId)
    print "after populate_contacts"

    contacts = json.dumps(contacts)
    return contacts


def populate_graphs(db, userId, graphs):
    '''friend_score =
    top_ten_recipients = db.session.query(db.func.distinct(models.Message.phoneNumber).filter(models.Message.direction == 'send'),
                         db.func.count(models.Message.phoneNumber)).filter(models.Message.direction == 'send').label("count")).group_by(models.Message.phoneNumber).order_by(count).limit(10)
    top_ten_senders = db.session.query(db.func.distinct(models.Message.phoneNumber).filter(models.Message.direction == 'receive'),
                         db.func.count(models.Message.phoneNumber)).filter(models.Message.direction == 'receive').label("count")).group_by(models.Message.phoneNumber).order_by(count).limit(10)

    graph1 = {}
    graph1['name'] = "Top Recipients"
    graph1['data'] = top_ten_recipients
    graphs.append(graph1)

    graph2 = {}
    graph1['name'] = "Top Senders"
    graph1['data'] = top_ten_senders
    graphs.append(graph2)'''
    pass


def past_fifteen_days(db, user_id, phone_number):
    sent_texts = []
    rcvd_texts = []
    for i in range(15):
        sent_texts.append(0)
        rcvd_texts.append(0)

    seconds_per_day = 3600 * 24
    current_time = int(time.time())
    fifteen_days_ago = current_time - seconds_per_day * 15 # this needs to be floored or whatever
    all_sent_messages = db.session.query(models.Message.timestamp).filter_by(userId=user_id).filter_by(phoneNumber=phone_number).filter_by(direction='send').filter_by(int(timestamp) >= fifteen_days_ago)
    all_sent_messages = all_sent_messages.column_descriptions

    all_rcvd_messages = db.session.query(models.Message.timestamp).filter_by(userId=user_id).filter_by(phoneNumber=phone_number).filter_by(direction='receive').filter_by(int(timestamp) >= fifteen_days_ago)
    all_rcvd_messages = all_rcvd_messages.column_descriptions

    for stamp in all_sent_messages:
        sent_texts[((int(stamp) - current_time))/seconds_per_day] += 1

    for stamp in all_rcvd_messages:
        rcvd_texts[((int(stamp) - current_time))/seconds_per_day] += 1


def test_query(db):
    print "before first query"
    try_this = models.Message.query.filter_by(phoneNumber='32507')
    #filter_by(userId="352584060592000")
    print "after first query"
    print "hi" + str(try_this.column_descriptions)


# contacts: {phoneNumber: {sentTexts: #, receivedTexts: #, etc.})}
def populate_contacts(db, user_id):
    contacts = {}

    print "before first query"
    try_this = db.session.query(models.Message).filter_by(userId=user_id)
    print "hi" + str(try_this)
    #all_sent_contacts = db.session.query(models.Message.phoneNumber, db.func.count(models.Message.phoneNumber).label("sent_count")).filter_by(userId=user_id).filter_by(direction='send').group_by(phoneNumber).order_by(db.desc("sent_count"))
    print "after first query"
    '''all_sent_contacts = all_sent_contacts.column_descriptions
    print all_sent_contacts

    for entry in all_sent_contacts:
        contacts[entry.phoneNumber] = {}
        contacts[entry.phoneNumber]["sentTexts"] = entry.sent_count

    all_rcvd_contacts = db.session.query(models.Message.phoneNumber, db.func.count(models.Message.phoneNumber).label("rcvd_count")).filter_by(userId=user_id).filter_by(direction='receive').group_by(phoneNumber).order_by(db.desc("rcvd_count"))
    all_rcvd_contacts = all_rcvd_contacts.column_descriptions
    print all_rcvd_contacts

    for entry in all_rcvd_contacts:
        if (contacts[entry.phoneNumber] == None):
            contacts[entry.phoneNumber] = {}
        contacts[phoneNumber]["receivedTexts"] = entry.rcvd_count

    return contacts    '''
    return try_this


def contacts_to_json(contacts):
    result = []
    for number in contacts:
        c = {}
        c["phoneNumber"] = number
        if (contacts[number]["sentTexts"] == None):
            c["sentTexts"] = 0
        else:
            c["sentTexts"] = contacts[number]["sentTexts"]
        if (contacts[number]["receivedTexts"] == None):
            c["receivedTexts"] = 0
        else:
            c["receivedTexts"] = contacts[number]["receivedTexts"]
        result.append(c)
