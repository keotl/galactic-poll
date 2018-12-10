import json
import urllib

from jivago.wsgi.annotations import Resource
from jivago.wsgi.methods import POST


@Resource("/vote-callback")
class VoteCallbackResource(object):

    @POST
    def vote_callback(self, body: dict) -> dict:
        payload = json.loads(urllib.parse.unquote(body["payload"]))

        original_message = payload['original_message']

        number_of_votes = int(original_message['text'].split("+")[0]) if original_message['text'] != '' else 0


        original_message['text'] = f"{number_of_votes + 1} {'person' if number_of_votes == 0 else 'people'} voted."

        return original_message
