import urllib

from jivago.lang.stream import Stream
from jivago.wsgi.annotations import Resource
from jivago.wsgi.methods import POST


@Resource("/command")
class CommandResource(object):

    @POST
    def post(self, body: dict) -> dict:
        print(body)
        args = urllib.parse.unquote(body['text']).split(" ")
        question = args[0]
        responses = args[1::]
        button_attachments = Stream(responses).map(
            lambda x: {"callback_id": "vote_callback", "name": "poll", "text": x, "type": "button",
                       "value": x}).toList()
        response = {"response_type": "in_channel",
                    "attachments": [{"fallback": "poll button", "text": question, "callback_id": "vote_callback",
                                     "actions": button_attachments}]}
        print(response)
        return response
