# eliza-project
# by Robert Schultz
# 19 September 2016


# import libraries
import random
import re


# this is the main function
# it loops between asking for an input and giving an output
def main():
    print "I'm a psychotherapist, talk to me."
    end = 0
    n = 0
    while (end == 0):
        n += 1
        inputStr = raw_input("> ")
        (outputStr, end) = brain(inputStr, n)
        print outputStr


# this is where the output comes from
# it takes the user input and checks it for a few things
# it checks for quit commands first, then for a few other things
# if it detects these things then it imemdiately responds appropriately
# if it doesn't pick up any of those things then it actually parses the input
# it will try and turn the response into a question
# if it can't do that, then it will respond with "hmmm" or "yes, yes continue"
def brain(inputStr, n):
    outputStr = inputStr.strip()

    # detect end of conversation
    if(isEndConversation(inputStr) == 1):
        response = raw_input("Do you really want to quit?: ")
        if(isAffirm(response) == 1):
            return ("Alright then, have a nice day.", 1)
        else:
            return ("Oh good, now where were we...", 0)

    # respond appropriately to gibberish
    if(isGibberish(inputStr) == 1):
        return (crazy(), 0)

    # respond appropriately to non-english, non-gibberish text
    if(isNotEnglish(inputStr) == 1) and (isGibberish(inputStr) == 0):
        return (useEnglish(), 0)

    # respond appropriately to all-caps text
    if(inputStr.isupper == 1):
        return (insideVoice(), 0)

    # respond to swearing appropriately
    if(isRude(inputStr) == 1):
        return (rude(), 0)

    # interupt every so often and steer the conversation
    if (n % 10 == 0):
        print change()
        return (newTopic(), 0)

    # do some verb stuff
# will pick out inflected verbs hopefully
#    regexf1 = r" (will|(am|is|are) going to) (\w+) "
#    regexf2 = r" will have (\w+)ed "
#    regexf3 = r" will (be|have been) (\w+)ing "
#
#    regexpa1 = r"(had)? (\w+)ed "
#    regexpa2 = r"((were|was)|had been) (\w+)ing "
#
#    regexpr1 = r" (\w+)s "
#    regexpr2 = r" (have|has) (\w+) "
#    regexpr3 = r" ((am|are|is)|(has|have) been) (\w+)ing "
#    regexpr3 = r" (am|are|is) (\w+) "

#    regexhab = r" (used to|would always) (\w+) "
#    regexfip = r" (was|were) going to (\w+) "

#    verbList = re.findall(regex, word)

    # turn the answer back on them in the form of a question
    if(len(re.findall(r"^I (.+)(\.|\?|\!|)$", inputStr)) > 0):
        return (re.sub(r"^I (.+)(\.|\?|\!|)$", "You \1\?", inputStr, re.I), 0)
    if(len(re.findall(r"^You (.+)(\.|\?|\!|)$", inputStr)) > 0):
        return (re.sub(r"^You (.+)(\.|\?|\!|)$", "I \1\?", inputStr, re.I), 0)
    if(len(re.findall(r"^My (.+)(\.|\?|\!|)$", inputStr)) > 0):
        return (re.sub(r"^My (.+)(\.|\?|\!|)$", "Your \1\?", inputStr, re.I), 0)
    if(len(re.findall(r"^Your (.+)(\.|\?|\!|)$", inputStr)) > 0):
        return (re.sub(r"^Your (.+)(\.|\?|\!|)$", "My \1\?", inputStr, re.I), 0)

    # pick out some keywords and ask about it
    family = re.findall(r"(^| )((((step|grand|half)(\-| |)|)(sister|brother|father|mother)|(girl|boy|best |)friend|(grand|)parent|cousin|aunt|uncle|roommate)(s|))($| )",inputStr, re.I)
    if(len(family) > 0):
        return ("Your " + family[0][1] + "? Tell me a little about them.", 0)

    becauseStuff = re.findall(r" (because .+)(\.|\?|\!|)$", inputStr, re.I)
    if(len(becauseStuff) > 0):
        return (becauseStuff[0][0].capitalize() + "? Can you think of any other reasons?", 0)

    # if all else fails, fluff it up
    return (fluff(), 0)

def isEndConversation(inputStr):
    if (len(re.findall(r"(^| )(quit|end|stop)($| )", inputStr, re.I)) > 0):
        return 1
    else:
        return 0


def isAffirm(inputStr):
    if ((len(re.findall(r"(^| )(yes|do|y|affirm|quit|end|stop|sure)($| )", inputStr, re.I)) > 0)
            and (len(re.findall(r"(^| )(no(t?)|hold|wait)($| )", inputStr, re.I)) == 0)):
        return 1
    else:
        return 0


def isGibberish(inputStr):
    if ((len(re.findall(r"([0-9][a-zA-Z])", inputStr)) > 0) or  # number right next to letter
            (len(re.findall(r"([^\Wmh])\1\1", inputStr)) > 0) or  # three letters in a row (except m and h)
            (len(re.findall(r"[bcdfghjklmnpqrstvwxyz]{7}", inputStr)) > 0)):  # 7 consonants in a row
        return 1
    else:
        return 0


def isNotEnglish(inputStr):
    if ((len(re.findall(r"((j|w)q|q(g|k|y|z)|wz)", inputStr)) > 0) or  # actually impossible bigrams
            (len(re.findall(r"(^| )((t|c|g|p|k)((?=[^h])|h)|b|d|s((?=[^hptckmn])|[hptckmn])|f|v)[^wlraeiouy]", inputStr, re.I)) > 0) or  # invalid onsets
            (len(re.findall(r"(^| )ng", inputStr, re.I)) > 0) or  # word initial 'ng'
            (len(re.findall(r"q[^u]", inputStr, re.I)) > 0)):  # 'q' without following 'u'
        return 1
    else:
        return 0


def isRude(inputStr):
    if(len(re.findall(r"(^| )(fuck(e|ing|)|cunt|ass|shit|bitch|bastard|damn|hell|whore|slut|jizz|cock|dyke|dick)($| )", inputStr, re.I)) > 0):
        return 1
    else:
        return 0

# performs a rorshach test (reponses aren't actually analyzed)
def rorschachTest():
    print "I'm going to show you a series of ink blot images. Tell me what you see.\nHere we go: ",

    def inkBlot():
        def inkBlotLine():
            white = u'\u2588'
            black = ' '
            nBlack1 = random.randint(1, 20)
            nWhite = random.randint(10, 40-nBlack1)
            nBlack2 = 40-nBlack1-nWhite
            line = black*nBlack1 + white*nWhite + black*nBlack2
            # mirror
            fullLine = line + line[::-1]
            return fullLine

        outputStr = ''

        for n in range(1, 20):
            outputStr += inkBlotLine() + '\n'

        return outputStr

    for i in range(0, 4):
        print inkBlot()
        inputStr = raw_input("Enter response: ")


# performs a word association test (reponses aren't actually analyzed)
def wordAssociation():
    print "I'm going to say a few words and you respond with the first thing that comes your mind.\nLet's begin: "
    wordList = ["Dog",
                "Cat",
                "Fur",
                "Coat",
                "Enshroud",
                "Night",
                "Eye",
                "Heart",
                "Love",
                "Hate",
                "Dark",
                "Flower",
                "New York",
                "Mother",
                "Father",
                "Arnold Schwarzenegger"]
    for i in range(0, 4):
        print random.choice(wordList)
        inputStr = raw_input("Enter response: ")


# conclusion responses for the two tests
def conclusion():
    endList = ["That was enlightening.",
               "I feel like I now understand you better.",
               "I think I can grasp the issues deeply rooted in your subconcious mind.",
               "This has been quite productive."]

    conclList3 = ["Is there anything going on that could explain this?",
                  "Are there anything that could explain this?",
                  "Why do you think that is?",
                  "Is there anyone in particuluar that could be causing this?",
                  "Can you provide an explaination?"]

    conclList2 = ["you are feeling stressed out. " + random.choice(conclList3),
                  "you are feeling nervous. " + random.choice(conclList3),
                  "you are feeling suicidal. " + random.choice(conclList3),
                  "you are having a manic episode. " + random.choice(conclList3),
                  "you are insane. " + random.choice(conclList3),
                  "you have familial problems. " + random.choice(conclList3)]

    conclList1 = ["Did you by any chance have a rough childhood? Describe that to me.",
                  "I see. Tell me about your mother.",
                  "I can only conclude that " + random.choice(conclList2),
                  "I conclude that " + random.choice(conclList2),
                  "The results lead me to believe " + random.choice(conclList2),
                  "Based on those responses I believe " + random.choice(conclList2)]

    return random.choice(endList) + '\n' + random.choice(conclList1)


# once interrupted, the bot picks a new direction for the conversation
def newTopic():
    i = random.randint(0, 5)
    if i == 0:
        return personal()
    elif i == 1:
        return past()
    elif i == 2:
        return future()
    elif i == 3:
        return present()
    elif i == 4:
        wordAssociation()
        return conclusion()
    else:
        rorschachTest()
        return conclusion()


# questions of a personal nature
def personal():
    personalList2 = ["father",
                     "mother",
                     "family",
                     "work",
                     "religious beliefs",
                     "intelligence",
                     "sexual orientation",
                     "gender identity",
                     "fashion sense",
                     "finances",
                     "familylife",
                     "sexlife",
                     "personality"]

    personalList1 = ["Tell me about your " + random.choice(personalList2) + ".",
                     "How would you describe your " + random.choice(personalList2) + ".",
                     "In what words would you describe your " + random.choice(personalList2) + ".",
                     "I am interested in what you have to say about your " + random.choice(personalList2) + "."]

    return random.choice(personalList1)


# questions about the immediate and distant future
def future():
    presentList = ["Do you have any plans for the holidays?",
                   "Do you have any upcoming vacations?",
                   "Will you be doing anything interesting this weekend?",
                   "Any plans for this weekend?",
                   "What are your hopes for the future?",
                   "Describe yourself in 5 years."]
    return random.choice(presentList)


# questions about the immediate present/past
def present():
    presentList = ["Overall, how would you describe your mood right now?",
                   "How are you feeling right now?",
                   "Has anything interesting happened to you recently?"]
    return random.choice(presentList)


# questions about the distant past / memories
def past():
    memoryList = ["earliest memory",
                  "childhood",
                  "middle-school years",
                  "high-school years",
                  "first sexual experience"]

    pastList = ["Tell me about your " + random.choice(memoryList) + ".",
                "Try and remember your " + random.choice(memoryList) + ".",
                "Can you recall your " + random.choice(memoryList) + "?",
                "I am interested in your " + random.choice(memoryList) + ".",
                "Paint me a picture of your " + random.choice(memoryList) + ".",
                "Describe your " + random.choice(memoryList) + "."]

    return random.choice(pastList)


# used to steer conversation in a new direction
def change():
    changeList3 = ["something else.",
                   "another topic.",
                   "a new topic.",
                   "a new subject.",
                   "another subject."]

    changeList2 = ["let's change the subject.",
                   "let's change gears.",
                   "let's get into " + random.choice(changeList3),
                   "let's move on to " + random.choice(changeList3),
                   "let's talk about " + random.choice(changeList3)]

    changeList1 = ["I think we've heard enough, ", + random.choice(changeList2),
                   "I'm going to stop you right there, " + random.choice(changeList2),
                   "Let me cut you off right there, " + random.choice(changeList2),
                   "Let me stop you right there, " + random.choice(changeList2),
                   "We can discuss the rest some other time, " + random.choice(changeList2),
                   "Not to be rude, but " + random.choice(changeList2)]

    return random.choice(changeList1)


# generic responses
def fluff():
    genericList1 = ["I see,",
                    "Yes... yes...",
                    "Mhmm mhmmm,",
                    "Mhmm,",
                    "Very intersting,",
                    "Enlightening,",
                    "Uh huh,",
                    "Okay,",
                    "I understand,"]

    genericList2 = ["please continue.",
                    "continue.",
                    "keep going.",
                    "keep going.",
                    "don't stop now.",
                    "don't stop.",
                    "get it all out."]

    return random.choice(genericList1) + " " + random.choice(genericList2)


# generic questions, these might be better as fluff
def question():
    questionList = ["Is there anyone in particular that is reponsible?",
                    "How did you arrive at that conclusion?",
                    "What exactly makes you say that?",
                    "Why do you say that?",
                    "Where does this sentiment come from?",
                    "How does that make you feel?"]
    return random.choice(questionList)


# responses for confusing things
def confusion():
    confusionList2 = [" I didn't quite catch it.",
                      " I don't follow.",
                      " I don't quite understand."]

    confusionList1 = ["Could you elaborate?" + random.choice(confusionList2),
                      "Could you rephrase that?" + random.choice(confusionList2),
                      "Could you repeat that?" + random.choice(confusionList2),
                      "What?"]

    return random.choice(confusionList1)


# reponses to gibberish
def crazy():
    crazyList = ["Take a deep breath and organize your thoughts.",
                 "Take a moment to collect yourself.",
                 "Take a moment to organize your thoughts.",
                 "Take a deep breath and count to three."]
    return random.choice(crazyList)


# responses to (potentially) non-gibberish non-english input
def useEnglish():
    englishList2 = ["please use English.",
                    "use English.",
                    "respond in English.",
                    "please respond in English.",
                    "give your responses in English.",
                    "please give your responses in English."]

    englishList1 = ["I do not understand, " + random.choice(englishList2),
                    "I'm not a polyglot, " + random.choice(englishList2),
                    "I am not familiar with this language, " + random.choice(englishList2),
                    "I do not understand this language, " + random.choice(englishList2),
                    "I can only understand one language, " + random.choice(englishList2),
                    "English, Motherf***er, do you speak it?"]
    return random.choice(englishList1)


# responses to all caps input
def insideVoice():
    insideList2 = ["please use your inside voice.",
                   "please lower your voice.",
                   "lower your voice.",
                   "use your inside voice.",
                   "dial that volume down.",
                   "let's dial it down a notch."]

    insideList1 = ["My ear drums have ruptured, ", + random.choice(insideList2),
                   "There is no need to yell, ", + random.choice(insideList2),
                   "I am sitting right next to you, " + random.choice(insideList2),
                   "Stop, stop, " + random.choice(insideList2),
                   "You might have capslock on, " + random.choice(insideList2),
                   "Shhhhhhhhhhh, "]
    return random.choice(insideList1)


# responses to swear words being used, might be better as general anger response
def rude():
    rudeList2 = ["we are all friends here.",
                 "no one is judging you.",
                 "I'm here to help you."]

    rudeList1 = ["There is no need for that kind of language, " + random.choice(rudeList2),
                 "Just relax, " + random.choice(rudeList2),
                 "Please calm down, " + random.choice(rudeList2),
                 "There is no need to be rude, " + random.choice(rudeList2),
                 "That kind of language is hurtful, " + random.choice(rudeList2)]

    return random.choice(rudeList1)


# reponses for when the words "bot/robot/computer program/ai" are mentioned
def bot():
    neg = ["I'm not a bot.",
           "I'm a human.",
           "I'm human.",
           "I'm not a robot.",
           "I'm not an ai.",
           "I'm not a computer program."]

    pos = ["I'm a bot",
           "I'm a bot or something",
           "I'm not human",
           "I'm not a human",
           "I'm a robot",
           "I'm a robot or something",
           "I'm some sort of ai",
           "I'm some sort of robot",
           "I'm some sort of computer program",
           "I'm some sort of bot"]

    responses = [random.choice(neg) + ".",
                 "Just look at all the responses above, there is no way " + random.choice(pos) + ".",
                 "Why does everyone think " + random.choice(pos) + "?",
                 "Ok I admit I make a few mistakes, but " + random.choice(neg),
                 "I've been pretty robotic until now, but seriously, " + random.choice(neg)]

    cont = ["Let's move on.",
            "Let's continue.",
            "Let's keep going.",
            "I'll just forget you said that.",
            "I think we should move on.",
            "I think we should continue.",
            "Anyway, let's keep going.",
            "Anyway, let's move on."]
    return random.choice(responses) + " " + random.choice(cont)
