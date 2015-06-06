# Name: usernameMentions (/u/usernameMentions)
# Author: Saroekin (/u/Saroekin)
# Version: Python 2.7.6

#Files or importations that are used elsewhere in program.
import os
import praw
import time
import traceback
import requests
import sqlite3

#User's username and password.
Username = <Username>
Password = <Password>

#What reddit sees from the bot's requests.
user_agent = <User Agent>
r = praw.Reddit(user_agent = user_agent)
print("\n\nLogging in . . . \n\n")
r.login(Username, Password)

#Various variables.
usernameDepictor = "/u/"
privateMessageLink = "http://www.reddit.com/message/compose/?to=Saroekin&subject=/u/usernameMentions."
wikiPage = "http://www.reddit.com/r/Saroekin_redditBots/wiki/-/u/usernamementions"
sourceCode = "http://github.com/Saroekin/usernameMentions"

#Templates for messages and comments (and variables).
Message_Username_Mention_Title_Template = """
**Your username was mentioned in the title of this [submisson](%s).**

*Subreddit:*

>/r/%s

*Author of submission:*

>%s

---
[[Contact Developer]({privateMessageLink})] | [[Wiki Page]({wikiPage})] | [[Source Code]({sourceCode})]

""".format(privateMessageLink = privateMessageLink, wikiPage = wikiPage, sourceCode = sourceCode)

Message_Username_Mention_Text_Template = """
**Your username was mentioned in the subtext of this [submisson](%s).**

*Subreddit:*

>/r/%s

*Author of submission:*

>%s

---
[[Contact Developer]({privateMessageLink})] | [[Wiki Page]({wikiPage})] | [[Source Code]({sourceCode})]

""".format(privateMessageLink = privateMessageLink, wikiPage = wikiPage, sourceCode = sourceCode)

Message_Username_Mention_TitleText_Template = """
**Your username was mentioned in the title and subtext of this [submisson](%s).**

*Subreddit:*

>/r/%s

*Author of submission:*

>%s

---
[[Contact Developer]({privateMessageLink})] | [[Wiki Page]({wikiPage})] | [[Source Code]({sourceCode})]

""".format(privateMessageLink = privateMessageLink, wikiPage = wikiPage, sourceCode = sourceCode)

messageSendTitle = Message_Username_Mention_Title_Template

messageSendText = Message_Username_Mention_Text_Template

messageSendTitleText = Message_Username_Mention_TitleText_Template

#Main definiton for cycling through username request.
def mentionedUsers_all():
    subreddit = r.get_subreddit("Saroekin_redditBots")
    streamedSubmissions = praw.helpers.submission_stream(r, subreddit)
    for submission in streamedSubmissions:
        if submission.is_self == True:
            submissionTitle = str(submission.title)
            try:
                submissionText = str(submission.selftext)
            except UnicodeEncodeError:
                pass
            if usernameDepictor not in submissionTitle or usernameDepictornot in submissionText:
                continue
        else:
            submissionTitle = str(submission.title)
            if usernameDepictor not in submissionTitle:
                continue
        try:
            submissionAuthor = submission.author
            submissionAuthor.get_overview()
        except AttributeError:
            submissionAuthor = "[deleted]"
            pass
        if submissionAuthor != "[deleted]":
            submissionAuthor = usernameDepictor + str(submissionAuthor)
        submissionSubreddit = submission.subreddit
        submissionTitleList = submissionTitle.split()
        submissionTextList = submissionText.split()
        messagedAuthors = []
        multipleMentions = []
        mentionedTitleAuthors = []
        mentionedTextAuthors = []
        submissionPermalink = submission.permalink
        if usernameDepictor in submissionTitle and submissionText:
            for word in submissionTitleList:
                if usernameDepictor in str(word):
                    userMentionedName = str(word.replace(usernameDepictor, ""))
                    if ("/u/" + userMentionedName) == submissionAuthor:
                        continue
                    try:
                        r.get_content(("http://www.reddit.com/u/" + userMentionedName))
                    except requests.exceptions.HTTPError as e:
                        if e.response.status_code == 404:
                            continue                   
                    mentionedTitleAuthors.append(userMentionedName)
            for word in submissionTextList:
                if usernameDepictor in str(word):
                    userMentionedName = str(word.replace(usernameDepictor, ""))
                    if ("/u/" + userMentionedName) == submissionAuthor:
                        continue
                    try:
                        r.get_content(("http://www.reddit.com/u/" + userMentionedName))
                    except requests.exceptions.HTTPError as e:
                        if e.response.status_code == 404:
                            continue   
                    if userMentionedName in mentionedTitleAuthors:
                        multipleMentions.append(userMentionedName)
                        mentionedTitleAuthors.remove(userMentionedName)
                    else:
                        mentionedTextAuthors.append(userMentionedName)
            for author in multipleMentions:
                r.send_message(author, "username mention", (messageSendTitleText % (submissionPermalink, submissionSubreddit, submissionAuthor)))
            for author in mentionedTitleAuthors:
                r.send_message(author, "username mention", (messageSendTitle % (submissionPermalink, submissionSubreddit, submissionAuthor)))
            for author in mentionedTextAuthors:
                r.send_message(author, "username mention", (messageSendText % (submissionPermalink, submissionSubreddit, submissionAuthor)))
        elif usernameDepictor in submissionTitle:
            for word in submissionTitleList:
                if usernameDepictor in str(word):
                    userMentionedName = str(word.replace(usernameDepictor, ""))
                    if ("/u/" + userMentionedName) == submissionAuthor:
                        continue
                    if userMentionedName not in messagedAuthors:
                        try:
                            r.get_content(("http://www.reddit.com/u/" + userMentionedName))
                        except requests.exceptions.HTTPError as e:
                            if e.response.status_code == 404:
                                continue     
                        r.send_message(userMentionedName, "username mention", (messageSendTitle % (submissionPermalink, submissionSubreddit, submissionAuthor)))
                        messagedAuthors.append(userMentionedName)
        elif usernameDepictor in submissionText:
            for word in submissionTextList:
                if usernameDepictor in str(word):
                    userMentionedName = str(word.replace(usernameDepictor, ""))
                    if ("/u/" + userMentionedName) == submissionAuthor:
                        continue
                    if userMentionedName not in messagedAuthors:
                        try:
                            r.get_content(("http://www.reddit.com/u/" + userMentionedName))
                        except requests.exceptions.HTTPError as e:
                            if e.response.status_code == 404:
                                continue
                        r.send_message(userMentionedName, "username mention", (messageSendText % (submissionPermalink, submissionSubreddit, submissionAuthor)))
                        messagedAuthors.append(userMentionedName)

#def mentionedUsers_allEdited():
    #subreddit = r.get_subreddit("editedPosts")
    #submissions = subreddit.get_new(limit=100)
    #In progress.

#Describes the running process of the bot.
print("\n\nRunning . . . \n\n")
while True:
    mentionedUsers_all()
