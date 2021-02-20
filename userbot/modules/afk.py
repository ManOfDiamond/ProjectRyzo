# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module which contains afk-related commands """

from asyncio import sleep
from random import choice, randint

from telethon.events import StopPropagation

from userbot import (AFKREASON, BOTLOG, BOTLOG_CHATID, CMD_HELP, COUNT_MSG,
                     ISAFK, PM_AUTO_BAN, USERS)
from userbot.events import register

# ========================= CONSTANTS ============================
AFKSTR = [
    "My master is busy right now. Please talk in a bag and when he comes back you can just give him the bag!",
    "My master is away right now. If you need anything, leave a message after the beep:\n`beeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeep`!",
    "You missed my master, next time aim better;).",
    "My master will be back in a few minutes and if he does not...,\nwait longer.",
    "My master is not here right now, so he is probably somewhere else.",
    "Roses are red,\nViolets are blue,\nLeave me a message,\nAnd my master will get back to you.",
    "Sometimes the best things in life are worth waiting for…\nMy master will be right back.",
    "My master will be right back,\nbut if he is not right back,\nHe'll be back later.",
    "If you haven't figured it out already,\nMy master is ded right now.",
    "Hello, welcome to my away message, how may I ignore you today?",
    "My master is away over 7 seas and 7 countries,\n7 waters and 7 continents,\n7 mountains and 7 hills,\n7 plains and 7 mounds,\n7 pools and 7 lakes,\n7 springs and 7 meadows,\n7 cities and 7 neighborhoods,\n7 blocks and 7 houses...\n\nWhere not even your messages can reach me!",
    "My master is away from the keyboard at the moment, but if you'll scream loud enough at your screen, he might just hear you.",
    "My master went that way\n---->",
    "My master this way\n<----",
    "Please leave a message and make my master feel even more important than he already is.",
    "My master is not here so stop writing to him,\nor else you will find yourself with a screen full of your own messages.",
    "If my master was here,\nhe'd tell you where he is.\n\nBut he is not,\nso ask him when he returns...",
    "My master is away!\nI don't know when he'll be back!\nHopefully a few minutes from now!",
    "My master is not available right now so please leave your name, number, and address and he will stalk you later.",
    "Sorry, my master is not here right now.\nFeel free to talk to me, his userbot, as long as you like.\nhe'll get back to you later.",
    "I bet you were expecting an away message!",
    "Life is so short, there are so many things to do...\nmy kind master is away doing one of them..",
    "My master is not here right now...\nbut if he was...\n\nwouldn't that be awesome?",
]
# =================================================================


@register(incoming=True, disable_edited=True)
async def mention_afk(mention):
    """ This function takes care of notifying the people who mention you that you are AFK."""
    global COUNT_MSG
    global USERS
    global ISAFK
    if mention.message.mentioned and ISAFK:
        is_bot = False
        if (sender := await mention.get_sender()):
            is_bot = sender.bot
        if not is_bot and mention.sender_id not in USERS:
            if AFKREASON:
                await mention.reply("I'm AFK right now." f"\nBecause `{AFKREASON}`")
            else:
                await mention.reply(str(choice(AFKSTR)))
            USERS.update({mention.sender_id: 1})
        else:
            if not is_bot and sender:
                if USERS[mention.sender_id] % randint(2, 4) == 0:
                    if AFKREASON:
                        await mention.reply(
                            f"I'm still AFK.\
                                \nReason: `{AFKREASON}`"
                        )
                    else:
                        await mention.reply(str(choice(AFKSTR)))
                USERS[mention.sender_id] = USERS[mention.sender_id] + 1
        COUNT_MSG = COUNT_MSG + 1


@register(incoming=True, disable_errors=True)
async def afk_on_pm(sender):
    """ Function which informs people that you are AFK in PM """
    global ISAFK
    global USERS
    global COUNT_MSG
    if (
        sender.is_private
        and sender.sender_id != 777000
        and not (await sender.get_sender()).bot
    ):
        if PM_AUTO_BAN:
            try:
                from userbot.modules.sql_helper.pm_permit_sql import \
                    is_approved

                apprv = is_approved(sender.sender_id)
            except AttributeError:
                apprv = True
        else:
            apprv = True
        if apprv and ISAFK:
            if sender.sender_id not in USERS:
                if AFKREASON:
                    await sender.reply(
                        f"I'm AFK right now.\
                    \nReason: `{AFKREASON}`"
                    )
                else:
                    await sender.reply(str(choice(AFKSTR)))
                USERS.update({sender.sender_id: 1})
            else:
                if USERS[sender.sender_id] % randint(2, 4) == 0:
                    if AFKREASON:
                        await sender.reply(
                            f"I'm still AFK.\
                        \nReason: `{AFKREASON}`"
                        )
                    else:
                        await sender.reply(str(choice(AFKSTR)))
                USERS[sender.sender_id] = USERS[sender.sender_id] + 1
            COUNT_MSG = COUNT_MSG + 1


@register(outgoing=True, pattern=r"^\.afk(?: |$)(.*)", disable_errors=True)
async def set_afk(afk_e):
    """ For .afk command, allows you to inform people that you are afk when they message you """
    afk_e.text
    string = afk_e.pattern_match.group(1)
    global ISAFK
    global AFKREASON
    if string:
        AFKREASON = string
        await afk_e.edit("Going AFK!" f"\nReason: `{string}`")
    else:
        await afk_e.edit("Going AFK!")
    if BOTLOG:
        await afk_e.client.send_message(BOTLOG_CHATID, "#AFK\nYou went AFK!")
    ISAFK = True
    raise StopPropagation


@register(outgoing=True)
async def type_afk_is_not_true(notafk):
    """ This sets your status as not afk automatically when you write something while being afk """
    global ISAFK
    global COUNT_MSG
    global USERS
    global AFKREASON
    if ISAFK:
        ISAFK = False
        msg = await notafk.respond("I'm no longer AFK.")
        await sleep(2)
        await msg.delete()
        if BOTLOG:
            await notafk.client.send_message(
                BOTLOG_CHATID,
                "You've recieved "
                + str(COUNT_MSG)
                + " messages from "
                + str(len(USERS))
                + " chats while you were away",
            )
            for i in USERS:
                name = await notafk.client.get_entity(i)
                name0 = str(name.first_name)
                await notafk.client.send_message(
                    BOTLOG_CHATID,
                    "["
                    + name0
                    + "](tg://user?id="
                    + str(i)
                    + ")"
                    + " sent you "
                    + "`"
                    + str(USERS[i])
                    + " messages`",
                )
        COUNT_MSG = 0
        USERS = {}
        AFKREASON = None


CMD_HELP.update(
    {
        "afk": ">`.afk [Optional Reason]`"
        "\nUsage: Sets you as afk.\nReplies to anyone who tags/PM's "
        "you telling them that you are AFK(reason)."
        "\n\nSwitches off AFK when you type back anything, anywhere."
    }
)

