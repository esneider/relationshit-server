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

    models.Message.query.filter_by(userId = userId).delete()
    db.session.commit()

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

    contacts = populate_contacts(userId)
    result = []

    # top friends graphs
    result.append( ( "Most texts sent to", top_friends(contacts, "sentTexts", True) ) )
    result.append( ( "Most texts received from", top_friends(contacts, "receivedTexts", True) ) )
    result.append( ( "Longest messages sent to", top_friends(contacts, "sentMsgLength", True) ) )
    result.append( ( "Longest messages received from", top_friends(contacts, "receivedMsgLength", True)))
    result.append( ( "Top friends", compound_friend_score(contacts) ) )

    return result

def compound_friend_score(contacts):
    scores = {}

    for key, value in contacts.iteritems():
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
    maxval = float(result[0][1])
    result = [(result[0], int((float(score[1])/maxval)*100)) for res in result]
    return result

'''Returns properties specific to a single contact'''
def contact_query(user_id, phoneNumber):
    sentMsgs = []
    rcvdMsgs = []
    
    q = models.Message.query.filter_by(userId = user_id, phoneNumber = phoneNumber)
    numSentTexts = q.filter_by(direction = "send").count()
    numRecTexts = q.filter_by(direction = "receive").count()

    for x in q.all():
        if (x.direction == 'send'):
            sentMsgs.append(x)
        else:
            rcvdMsgs.append(x)

    sentMsgLen = sum(sentMsgs) / len(sentMsgs)
    rcvdMsgLen = sum(rcvdMsgs) / len(rcvdMsgs)
    return numSentTexts, numRecTexts, sentMsgLen, rcvdMsgLen

'''The sender was actually waiting for an answer between msg1 and msg2
Both messages were sent by the (same) user'''
def was_waiting_for_answer(msg1, msg2):
    delay = msg2.timestamp - msg1.timestamp
    if (msg1.direction != msg2.direction):
        return False
    acceptable = 60 + len(msg2)/2
    return delay > acceptable

'''How many times do you have to text him till he replies? (worst case)'''
def max_unreplied_messages(db, user_id, phoneNumber):
    q = models.Message.query.filter_by(userId = user_id, phoneNumber = phoneNumber)
    all_messages = q.order_by(models.Message.timestamp).all()
    maxcount = 0
    currentcount = 0
    first = True
    for msg in all_messages:
        if (first):
            first = False
        else:
            if (msg.direction == "send" and was_waiting_for_answer(last, msg)):
                currentcount += 1
            else:
                maxcount = max(currentcount, maxcount)
                currentcount = 0
        last = msg
    return maxcount

def populate_contacts(user_id):
    contacts = {}
    q = db.session.query(models.Message.phoneNumber).filter_by(userId = user_id).distinct()
    uniqueNumbers = [m.phoneNumber for m in q]
    for uniqueNumber in uniqueNumbers:
        numSentTexts, numRecTexts, sentMsgLength, receivedMsgLength = contact_query(user_id, uniqueNumber)
        contacts[uniqueNumber] = {"sentTexts":numSentTexts, "receivedTexts":numRecTexts, "sentMsgLength":sentMsgLength, "receivedMsgLength":receivedMsgLength}
    return contacts


def graph_stats(user_id, phone_number):
    all_texts = db.session.query(models.Message.timestamp).filter_by(userId = user_id).filter_by(phoneNumber = phone_number)
    sent_times = all_texts.filter_by(direction = 'send').all()
    rcvd_times = all_texts.filter_by(direction = 'received').all()
    return sent_times, rcvd_times


def user_data(contacts):
    result = []

    for phone, data in contacts.iteritems():
        contact = [("phoneNumber", phone), ("sentTexts", data["sentTexts"]), ("receivedTexts", data["receivedTexts"]), ("sentMsgLength", data["sentMsgLength"]), ("receivedMsgLength", data["receivedMsgLength"])]
        result.append(contact)

    return result


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
