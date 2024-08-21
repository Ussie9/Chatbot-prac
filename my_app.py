#!/usr/bin/env python3

import spacy
from spacy.matcher.matcher import Matcher
import python-telegram-bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
import random

nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)

my_doc = open("machine.txt", encoding="utf8")
text = my_doc.read()
my_doc = nlp(text)


async def state0_handler(update, context):
    doc = nlp(update.message.text)
    reply = ''

    pattern1 = [{"TEXT" : "what"},{"LEMMA" : "machine"} , {"POS" : "learn"}]
    matcher.add("ML_DEFINITION_PATTERN" , [pattern1])
    matched_what = matcher(doc)

    pattern2 = [{"TEXT" : "how"} , {"LEMMA" : "machine"} , {"POS" : "learn"}]
    matcher.add("ML_FUNCTION_PATTERN" , [pattern2])
    matched_how = matcher(doc)

    pattern3 = [{"TEXT" : "deep", "OP":"?"} ,{"TEXT" : "neural"},{"TEXT" : "machine"}, {"POS" : "learn"}]
    matcher.add("ML_NEURAL_DIFF_PATTERN" , [pattern3])
    matched_diff = matcher(doc)

    if matched_what != 0:
        print(my_doc[0])
    elif matched_how != 0:
        print(my_doc[3])
    elif matched_diff != 0:
        print(my_doc[16])
    else :
        await update.message.reply_text(random.choice([
            "I didn't get the question, could you repeat it" ,
            "Unfortunately I currently don't have enough information on that" ,
        ]))
    if reply:
        await update.message.reply_text(reply)
        # most likely, a different state needs to be returned
    return 'STATE0'


async def start(update, context):
    await update.message.reply_text("Good day, how may I assist you")
    return


async def cancel(update, context):
    await update.message.reply_text("Goodbye")
    return ConversationHandler.END


async def help(update, context):
    return await update.message.reply_text("Try these most common questions:\n"
                                           "what is machine learning\n"
                                           "how to implement machine learning\n"
                                           "differences between machine learning and neural networks")


def main():
    application = Application.builder().token('TOKEN').build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler(['start'], start)],
        states={
            'STATE0': [MessageHandler(filters.TEXT & ~filters.COMMAND, state0_handler)],
        },
        fallbacks=[CommandHandler(['cancel'], cancel),
                   CommandHandler('help', help)]
    )
    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
