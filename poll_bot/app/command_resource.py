import re
import urllib

from jivago.lang.stream import Stream
from jivago.wsgi.annotations import Resource
from jivago.wsgi.methods import POST


@Resource("/command")
class CommandResource(object):

    @POST
    def post(self, body: dict) -> dict:
        unquoted_query = urllib.parse.unquote(body['text']).replace("+", " ")
        tokens = Stream(re.findall('"([^"]*)"', unquoted_query)).filter(lambda x: x != '+').toList()

        # args = unquoted_query.split("+")
        question = tokens[0]
        responses = tokens[1::]
        button_attachments = Stream(responses).map(
            lambda x: {"callback_id": "vote_callback", "name": "poll", "text": x, "type": "button",
                       "value": x}).toList()

        text = question

        for option in responses:
            text += f"\n- {option} ->  "

        response = {"response_type": "in_channel",
                    "attachments": [{"fallback": "poll button", "text": text, "callback_id": "vote_callback",
                                     "actions": button_attachments}]}
        
        return response
