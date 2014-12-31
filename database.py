import sys
import models
from app import db
import json
import operator
import time
from datetime import datetime
from sqlalchemy import *

NUM_FRIENDS = 20

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


def process(userId):

    print 'heyy'
    sys.stdout.flush()

    contacts = populate_contacts(userId)
    result = []

    print 'heyy'
    sys.stdout.flush()

    # top friends graphs
    result.append( ( "Most texts sent to", top_friends(contacts, "sentTexts", True) ) )
    # result.append("Most texts received from", top_friends(contacts, "receivedTexts", True))
    # result.append("Longest messages", top_friends(contacts, "messageLength", False))
    # result.append("Top friends", compound_friend_score(contacts))

    print 'heyy'
    sys.stdout.flush()

    return result


def compound_friend_score(contacts):
    scores = {}

    for key, value in contacts.iteritems():
        print key, value
        scores[key] = sum(contacts[key].values())

    sorted_scores = sorted(scores.items(), key = operator.itemgetter(1), reverse = True)
    max = float(sorted_scores[0][1])
    normalized_scores = [(score[0], int((float(score[1])/max)*100)) for score in sorted_scores]
    return normalized_scores;


def top_friends(contacts, sortKey, desc):
    value_tuples = []
    for key, value in contacts.iteritems():
        value_tuples += [ (key, value[sortKey]) ]
    result = sorted(value_tuples, key = lambda x: x[1], reverse = desc)[:NUM_FRIENDS]

    return result


'''Returns properties specific to a single contact'''
def contact_query(user_id, phoneNumber):

    print 'bla 1'
    sys.stdout.flush()

    q = models.Message.query.filter_by(userId = user_id, phoneNumber = phoneNumber)

    print 'bla 2'
    sys.stdout.flush()

    numSentTexts = q.filter_by(direction = "send").count()

    print 'bla 3'
    sys.stdout.flush()

    numRecTexts = q.filter_by(direction = "receive").count()

    print 'bla 4'
    sys.stdout.flush()

    messages = q.query(models.Message.messageLength).all()

    print 'bla 5'
    sys.stdout.flush()
    msgLen = sum(msgs) / len(msgs)

    print 'bla 5'
    sys.stdout.flush()

    return numSentTexts, numRecTexts, msgLen


def populate_contacts(user_id):
    contacts = {}

    print 'heyy 1'
    sys.stdout.flush()

    q = db.session.query(models.Message.phoneNumber).filter_by(userId = user_id).distinct()

    print 'heyy 2'
    sys.stdout.flush()

    uniqueNumbers = [m.phoneNumber for m in q]

    print 'heyy 3', len(uniqueNumbers)
    sys.stdout.flush()

    for uniqueNumber in uniqueNumbers:

        print 'i', uniqueNumber
        sys.stdout.flush()

        numSentTexts, numRecTexts, msgLen = contact_query(user_id, uniqueNumber)

        contacts[uniqueNumber] = {"sentTexts":numSentTexts, "receivedTexts":numRecTexts, "messageLength":msgLen}

    print 'heyy'
    sys.stdout.flush()

    return contacts


def graph_stats(user_id, phone_number):
    all_texts = db.session.query(models.Message.timestamp).filter_by(userId = user_id).filter_by(phoneNumber = phone_number)
    sent_times = all_texts.filter_by(direction = 'send').all()
    rcvd_times = all_texts.filter_by(direction = 'received').all()
    return sent_times, rcvd_times


def user_data(user_id):
    result = {}
    all_users = db.session.query(models.Message.userId, models.Message.phoneNumber, models.Message.direction, func.count(timestamp), func.avg(messageLength)).filter_by(userId = user_id).group_by(userId, phoneNumber, direction).all()
    for tup in all_users:
        result[tup[0]] = {}

    for tup in all_users:
        if (tup[2] == 'send'):
            result[tup[0]]["sentTexts"] = tup[3]
            result[tup[0]]["sentMsgLen"] = tup[4]
        else:
            result[tup[0]]["receivedTexts"] = tup[3]
            result[tup[0]]["receivedMsgLen"] = tup[4]


'''def past_fifteen_days(user_id, phone_number):
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
'''

'''
def order_by_number_messages(user_id, direction):
    q = models.Message.query.filter_by(userId=user_id,direction=direction)

    results_list=q.all()
    ordered_numbers = [r.phoneNumber for r in results_list]
    ordered_values = [r.orderColumn for r in results_list]

    #return [ordered_numbers, ordered_values]
'''
