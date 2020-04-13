SET FOREIGN_KEY_CHECKS=0;

DROP DATABASE IF EXISTS social;
CREATE DATABASE social;
USE social;

drop table if exists User;
CREATE TABLE User (
    userID INT NOT NULL AUTO_INCREMENT,
    firstName VARCHAR(100),
    lastName VARCHAR(100),
    birthYear INT,
    birthMonth INT,
    birthDay INT,
    gender VARCHAR(7),
    email VARCHAR(50),
    profileImageURL VARCHAR(100),
    CONSTRAINT PRIMARY KEY (userID)
);

drop table if exists UserGroup;
CREATE TABLE UserGroup (
    groupID INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100),
    description VARCHAR(100),
    CONSTRAINT PRIMARY KEY (groupID)
);

drop table if exists Topic;
CREATE TABLE Topic (
    topicID INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(100),
    CONSTRAINT PRIMARY KEY (topicID)
);

drop table if exists Post;
CREATE TABLE Post (
    postID INT NOT NULL AUTO_INCREMENT,
    createdAt TIMESTAMP,
    title VARCHAR(100),
    contentText VARCHAR(140),
    CONSTRAINT PRIMARY KEY (postID)
);

drop table if exists Attachment;
Create Table Attachment (
    postID INT,
    URL VARCHAR(100),
    CONSTRAINT PRIMARY KEY (postID, URL)
);

drop table if exists Member;
CREATE TABLE Member (
    groupID INT,
    userID INT,
    CONSTRAINT PRIMARY KEY (groupID, userID)
);

drop table if exists Follower;
CREATE TABLE Follower (
    followerID INT,
    followedByID INT,
    CONSTRAINT PRIMARY KEY (followerID, followedByID)
);

drop table if exists Subscriber;
CREATE TABLE Subscriber (
    userID INT,
    topicID INT,
    CONSTRAINT PRIMARY KEY (userID, topicID)
);

drop table if exists Presented;
CREATE TABLE Presented (
    userID INT,
    postID INT,
    CONSTRAINT PRIMARY KEY (userID, postID)
);

drop table if exists Liked;
CREATE TABLE Liked (
    userID INT,
    postID INT,
    value INT,
    CONSTRAINT PRIMARY KEY (userID, postID)
);

drop table if exists Liked;
CREATE TABLE Liked (
    userID INT,
    postID INT,
    value INT,
    CONSTRAINT PRIMARY KEY (userID, postID)
);

drop table if exists Response;
CREATE TABLE Response (
    responseID INT,
    respondedByID INT,
    CONSTRAINT PRIMARY KEY (responseID, respondedByID)
);

drop table if exists PostTopic;
CREATE TABLE PostTopic (
    postID INT,
    topicID INT,
    CONSTRAINT PRIMARY KEY (postID, topicID)
);

ALTER TABLE Member ADD FOREIGN KEY fk0 (groupID) REFERENCES UserGroup(groupID);
ALTER TABLE Member ADD FOREIGN KEY fk1 (userID) REFERENCES User(userID);

ALTER TABLE Follower ADD FOREIGN KEY fk2 (followerID) REFERENCES User(userID);
ALTER TABLE Follower ADD FOREIGN KEY fk3 (followedByID) REFERENCES User(userID);

ALTER TABLE Subscriber ADD FOREIGN KEY fk4 (userID) REFERENCES User(userID);
ALTER TABLE Subscriber ADD FOREIGN KEY fk5 (topicID) REFERENCES Topic(topicID);

ALTER TABLE Presented ADD FOREIGN KEY fk6 (userID) REFERENCES User(userID);
ALTER TABLE Presented ADD FOREIGN KEY fk7 (postID) REFERENCES Post(postID);

ALTER TABLE Liked ADD FOREIGN KEY fk8 (userID) REFERENCES User(userID);
ALTER TABLE Liked ADD FOREIGN KEY fk9 (postID) REFERENCES Post(postID);

ALTER TABLE Response ADD FOREIGN KEY fk10 (responseID) REFERENCES Post(postID);
ALTER TABLE Response ADD FOREIGN KEY fk11 (respondedByID) REFERENCES Post(postID);

ALTER TABLE Attachment ADD FOREIGN KEY fk12 (postID) REFERENCES Post(postID);

ALTER TABLE Post ADD COLUMN userID INT;
ALTER TABLE Post ADD FOREIGN KEY fk13 (userID) REFERENCES User(userID);

ALTER TABLE PostTopic ADD FOREIGN KEY fk14 (postID) REFERENCES Post(postID);
ALTER TABLE PostTopic ADD FOREIGN KEY fk15 (topicID) REFERENCES Topic(topicID);

SET time_zone='+00:00';
