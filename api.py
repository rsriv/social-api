import pymysql
import sys
from datetime import datetime
from getpass import getpass


class API:
    def __init__ (self, password, unix_socket):
        if unix_socket != '':
            self.db = pymysql.connect(host="localhost", user="root", password=password, db="social", unix_socket=unix_socket)
            self.cursor = self.db.cursor()
        else:
            self.db = pymysql.connect(host="localhost", user="root", password=password, db="social")
            self.cursor = self.db.cursor()

    def handleInput(self):
        input = sys.argv
        api_method = input[1]

        # cases for each api_method input
        if api_method == 'post':
            userID = int(sys.argv[2])
            topicIDs = [int(id) for id in sys.argv[3][1:-1].split(',')]
            title = sys.argv[4]
            contentText = sys.argv[5]
            attachmentURLs = sys.argv[6][1:-1].split(',')
            self.post(userID, topicIDs, title, contentText, attachmentURLs)
        elif api_method == 'respond':
            userID = int(sys.argv[2])
            respondedByID = int(sys.argv[3])
            topicIDs = [int(id) for id in sys.argv[4][1:-1].split(',')]
            title = sys.argv[5]
            contentText = sys.argv[6]
            attachmentURLs = sys.argv[7][1:-1].split(',')
            self.respond(userID, respondedByID, topicIDs, title, contentText, attachmentURLs)
        elif api_method == 'subscribe_topic':
            userID = int(sys.argv[2])
            topicID = int(sys.argv[3])
            self.subscribe_topic(userID, topicID)
        elif api_method == 'follow_user':
            followerID = int(sys.argv[2])
            followedByID = int(sys.argv[3])
            self.follow_user(followerID, followedByID)
        elif api_method == 'join_group':
            userID = int(sys.argv[2])
            groupID = int(sys.argv[3])
            self.join_group(userID, groupID)
        elif api_method == 'like':
            userID = int(sys.argv[2])
            postID = int(sys.argv[3])
            value = int(sys.argv[4])
            self.like(userID, postID, value)
        elif api_method == 'read':
            userID = int(sys.argv[2])
            postID = int(sys.argv[3])
            self.read(userID, postID)
        elif api_method == 'get_unread_posts':
            userID = int(sys.argv[2])
            maxResults = int(sys.argv[3])
            unread_posts = self.get_unread_posts(userID, maxResults)
            print(unread_posts)
        elif api_method == 'get_likes':
            postID = int(sys.argv[2])
            likes = self.get_likes(postID)
            print(likes)
        elif api_method == 'get_post':
            postID = int(sys.argv[2])
            posts = self.get_post(postID)
            print(posts)
        elif api_method == 'get_responses':
            postID = int(sys.argv[2])
            responses = self.get_responses(postID)
            print(responses)
        elif api_method == 'get_followers':
            userID = int(sys.argv[2])
            followers = self.get_followers(userID)
            print(followers)
        elif api_method == 'get_members':
            groupID = int(sys.argv[2])
            member = self.get_members(groupID)
            print(member)
        elif api_method == 'get_subscribers':
            topicID = int(sys.argv[2])
            subscribers = self.get_subscribers(topicID)
            print(subscribers)
        elif api_method == 'get_attachments':
            postID = int(sys.argv[2])
            attachments = self.get_attachments(postID)
            print(attachments)
        elif api_method == 'get_user':
            userID = int(sys.argv[2])
            user = self.get_user(userID)
            print(user)
        else:
            print('ERROR: unsupported method')
            return
        print('OK: ' + str(input[1:]))

    # DB CRUD operations
    def post(self, userID, topicIDs, title, contentText, attachmentURLs):
        self.cursor.execute('INSERT INTO Post (createdAt, title, contentText, userID) values (\'{}\', \'{}\', \'{}\', {})'.format(str(datetime.now()), title, contentText, userID))
        postID = self.cursor.lastrowid
        for topicID in topicIDs:
            self.cursor.execute('INSERT INTO PostTopic (postID, topicID) values ({}, {})'.format(postID, topicID))
        for URL in attachmentURLs:
            self.cursor.execute('INSERT INTO Attachment (postID, URL) values ({}, \'{}\')'.format(postID, URL))
        print('postID: ' + str(postID))
        self.db.commit()

    def respond(self, userID, respondedByID, topicIDs, title, contentText, attachmentURLs):
        self.cursor.execute('INSERT INTO Post (createdAt, title, contentText, userID) values (\'{}\', \'{}\', \'{}\', {})'.format(str(datetime.now()), title, contentText, userID))
        postID = self.cursor.lastrowid
        for topicID in topicIDs:
            self.cursor.execute('INSERT INTO PostTopic (postID, topicID) values ({}, {})'.format(postID, topicID))
        for URL in attachmentURLs:
            self.cursor.execute('INSERT INTO Attachment (postID, URL) values ({}, \'{}\')'.format(postID, URL))
        self.cursor.execute('INSERT INTO Response (responseID,respondedByID) values ({}, {})'.format(postID, respondedByID))
        print('postID: ' + str(postID))
        self.db.commit()

    def subscribe_topic(self, userID, topicID):
        self.cursor.execute('INSERT INTO Subscriber (userID, topicID) values ({}, {})'.format(userID, topicID))
        self.db.commit()

    def follow_user(self, followerID, followedByID):
        self.cursor.execute('INSERT INTO Follower (followerID, followedByID) values  ({}, {})'.format(followerID, followedByID))
        self.db.commit()

    def join_group(self, userID, groupID):
        self.cursor.execute('INSERT INTO Member (userID, groupID) values ({}, {})'.format(userID, groupID))
        self.db.commit()

    def like(self, userID, postID, value):
        self.cursor.execute('INSERT INTO Liked (userID, postID, value) values ({}, {}, {})'.format(userID, postID, value))
        self.db.commit()

    def get_unread_posts(self, userID, maxResults):
        self.cursor.execute('SELECT * FROM Post WHERE postID NOT IN (SELECT postID FROM Presented WHERE userID={}) LIMIT {}'.format(userID, maxResults))
        return self.cursor.fetchall()

    def read(self, userID, postID):
        self.cursor.execute('INSERT INTO Presented (userID, postID) values ({}, {})'.format(userID, postID))
        self.db.commit()

    def get_likes(self, postID):
        self.cursor.execute('SELECT userID, value FROM Liked WHERE postID={}'.format(postID))
        return self.cursor.fetchall()

    def get_post(self, postID):
        self.cursor.execute('SELECT * from Post WHERE postID={}'.format(postID))
        return self.cursor.fetchall()

    def get_responses(self, postID):
        self.cursor.execute('SELECT * from Post WHERE postID IN (SELECT responseID FROM Response WHERE respondedByID={})'.format(postID))
        return self.cursor.fetchall()

    def get_followers(self, userID):
        self.cursor.execute('SELECT followerID from Follower WHERE followedByID={}'.format(userID))
        return self.cursor.fetchall()

    def get_members(self, groupID):
        self.cursor.execute('SELECT userID from Member WHERE groupID={}'.format(groupID))
        return self.cursor.fetchall()

    def get_subscribers(self, topicID):
        self.cursor.execute('SELECT userID from Subscriber WHERE topicID={}'.format(topicID))
        return self.cursor.fetchall()

    def get_attachments(self, postID):
        self.cursor.execute('SELECT URL FROM Attachment WHERE postID={}'.format(postID))
        return self.cursor.fetchall()

    def get_user(self, userID):
        self.cursor.execute('SELECT * from User WHERE userID={}'.format(userID))
        return self.cursor.fetchall()

def main():
    # Connect to db
    password = ''
    api = ''
    flag = 1
    while flag:
        try:
            f = open("password.txt", "r")
            password = f.read()
            f.close()
            f = open("socket.txt", "r")
            socket = f.read()
            f.close()
        except:
            socket = input('Enter MySQL unix_socket: ')
            password = getpass()
            f = open("password.txt", "w")
            f.write(password)
            f.close()
            f = open("socket.txt", "w")
            f.write(socket)
            f.close()
        try:
            api = API(password, socket)
            api.handleInput()
            flag = 0
        except:
            socket = input('Enter MySQL unix_socket: ')
            password = getpass()
            f = open("password.txt", "w")
            f.write(password)
            f.close()
            f = open("socket.txt", "w")
            f.write(socket)
            f.close()

main()
