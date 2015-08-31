from matrix_client import client as matrix

import requests
requests.packages.urllib3.disable_warnings()
import urllib


class MatrixRoom(object):
    def __init__(self, room, handler_cls):
        self.room_id = room.room_id
        self._room = room
        self._handler = handler_cls()

    def _listen(self, event):
        if event['type'] == 'm.room.message':
            content = event['content']
            msg_type = content['msgtype'][2:]

            resp = None

            if msg_type == 'emote':
                resp = self._handler.process_text(msg_type, content['body'])
            elif content['body'].startswith('@dicebot'):
                resp = self._handler.process_text(msg_type, content['body'][9:])

            if resp is not None:
                if resp.TYPE == 'text':
                    self._room.send_text(str(resp))
                else:
                    self._room.send_emote(str(resp))


class MatrixBackend(object):
    def __init__(self, handler_cls, server, username, password):
        self._client = matrix.MatrixClient(server)
        self._client.api.validate_cert = False
        self._client.login_with_password(username, password)
        self._client.add_listener(self._listen)

        self._handler_cls = handler_cls

    def begin(self):
        presence_url = '/presence/{user_id}/status'.format(user_id=urllib.quote(self._client.user_id))
        try:
            print('In rooms %s' % self._client.rooms)
            self._client.api._send('PUT', presence_url, {'status_msg': 'Keep on rollin\'!', 'presence': 'online'})

            for room in self._client.rooms.values():
                room.add_listener(MatrixRoom(room, self._handler_cls)._listen)

            self._client.listen_forever()
        finally:
            print('In rooms %s' % self._client.rooms)
            self._client.api._send('PUT', presence_url, {'status_msg': 'no dice :-(', 'presence': 'offline'})

    def _listen(self, event):
        if (event['type'] == 'm.room.member' and
              event['state_key'] == self._client.user_id):
            if event['content']['membership'] == 'invite':
                self._client.join_room(event['room_id'])
                room = self._client.rooms[event['room_id']]
                room.add_listener(MatrixRoom(room, self._handler_cls)._listen)
            elif event['content']['membership'] == 'leave':
                del self._client.rooms[event['room_id']]
