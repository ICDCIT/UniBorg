#COMBOT ANTI SPAM SYSTEM IS USED
#created for @uniborg (unfinished)

import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
#COMBOT ANTI SPAM SYSTEM IS USED
#created for @uniborg (unfinished)
from telethon.tl.types import ChatBannedRights
from telethon.tl.functions.channels import EditBannedRequest
from telethon import events
from uniborg.util import admin_cmd
import sys

@borg.on(events.ChatAction())
async def _(cas):
    chat = await cas.get_chat()
    if (chat.admin_rights or chat.creator):
        if cas.user_joined or cas.user_added: 
            user = await cas.get_user()
            id = user.id
            mid = "{}".format(chat.title)
            mention = "[{}](tg://user?id={})".format(user.first_name, user.id) 
            from requests import get
            r = get(f'https://combot.org/api/cas/check?user_id={id}') 
            r_dict = r.json() 
            if r_dict['ok']:
                try: 
                    more = r_dict['result']
                    # rights = ChatBannedRights(
                    #     until_date=None,
                    #     view_messages=True,
                    #     send_messages=True
                    # )

                    
                    # await borg.send_message('me',entity)
                    # get_entity = await event.get_participants(chat)
                    # await borg.send_message('me',get_entity)
                    # await borg(EditBannedRequest(cas.chat_id, id, rights))
                    entity = await borg.get_entity(chat)
                    await borg.edit_permissions(int('-100' + str(entity.id)), user.id, view_messages=False)
                    await borg.send_message(Config.PRIVATE_GROUP_BOT_API_ID, "**antispam log** \n**Who**: {} \n**Where**: {} \n**How**: [here](https://combot.org/api/cas/check?user_id={}) \n**Action**: Banned \n**More**: ```{}```".format(mention, mid, id, more),link_preview=False)
                except (Exception) as exc:
                    await borg.send_message(Config.PRIVATE_GROUP_BOT_API_ID, str(exc))
                    exc_type, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    print(exc)
    else:
        return ""
