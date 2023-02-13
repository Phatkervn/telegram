
from opentele.tl import TelegramClient
from opentele.api import API
import socks

import asyncio
import string

from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.functions.contacts import DeleteContactsRequest , ImportContactsRequest
from telethon.tl.types import ChannelParticipantsSearch, ChannelParticipantBanned, PeerUser ,InputPhoneContact

from telethon.errors import *

import random

class Telegram:

    def __init__(self, pathSession: str, proxy: dict):

        loop = asyncio.get_event_loop()
        api = API.TelegramIOS.Generate(
            unique_id=pathSession)
        if proxy:
            if 'user' in proxy:
                ip = proxy['ip']
                port = proxy['port']
                user = proxy['user']
                password = proxy['password']
                self.client = TelegramClient(pathSession, api=api,
                                             proxy=dict(proxy_type=socks.SOCKS5,
                                                        addr=ip,
                                                        port=port,
                                                        username=user,
                                                        password=password), loop=loop)
            else:
                ip = proxy['ip']
                port = proxy['port']
                self.client = TelegramClient(pathSession, api=api, proxy=(
                    socks.SOCKS5, ip, port), loop=loop)
        else:
            self.client = TelegramClient(
                pathSession, api=api, loop=loop)

    async def connect(self):
        await self.client.connect()
        if not await self.client.is_user_authorized():
            # không thể kết nối tới session
            return False
        return True

    async def getMember(self, group, option: list):
        print("groupscan: ", group)
        try:
            all_participants = []
            seen = []

            for i in string.ascii_lowercase:
                print(i)
                offset = 0
                limit = 200
                while True:
                    participants = await self.client(GetParticipantsRequest(
                        channel=group,
                        filter=ChannelParticipantsSearch(i),
                        offset=offset,
                        limit=limit,
                        hash=0
                    ))
                    if not participants.users:
                        break
                    offset += len(participants.users)
                    print('offset', offset)

                    users = {user.id: user for user in participants.users}
                    for participant in participants.participants:
                        if isinstance(participant, ChannelParticipantBanned):
                            if not isinstance(participant.peer, PeerUser):
                                # May have the entire channel banned. See #3105.
                                continue
                            user_id = participant.peer.user_id
                        else:
                            user_id = participant.user_id

                        user = users[user_id]
                        if user.id in seen:
                            continue
                        seen.append(user_id)
                        user = users[user_id]
                        user.participant = participant
                        all_participants.append(user)
                    # setNotofication(
                    #     row, f'Đang quét member... total - {len(all_participants)}')
                    await asyncio.sleep(3.5)

            print('DONE SCAN')
            return all_participants
        except Exception as e:
            print(e)
            s = repr(e)
            return s

    async def addMemberID(self):
        ...

    async def addMemberContact(self, phone):
        try:
            result = await self.client(ImportContactsRequest(
                        contacts=[InputPhoneContact(
                            client_id=random.randrange(-2**63, 2**63),
                            phone=phone,
                            first_name='some',
                            last_name='here'
                        )]
                    ))
            if len(result.users) > 0:
                # print(result.stringify())
                # user_to_add = await self.client.get_input_entity(phone)
                out = await self.client(functions.contacts.DeleteContactsRequest(
                    id=[result.users[0]]
                ))
                return 200
            else :
                print("phone khong ton tai")
                return 201
        except ContactNameEmptyError:
            print("Phone không tồn tại.")
            return 201
        except FloodWaitError :
            
            return 400
        except :
            return 404