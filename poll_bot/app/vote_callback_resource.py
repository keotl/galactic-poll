import json
import urllib

from jivago.lang.stream import Stream
from jivago.wsgi.annotations import Resource, Path
from jivago.wsgi.methods import POST


@Resource("/vote-callback")
class VoteCallbackResource(object):

    @POST
    def vote_callback(self, body: dict) -> dict:
        payload = json.loads(urllib.parse.unquote(body["payload"]))
        multi = payload['callback_id'] == 'vote_callback_multi'
        original_message = payload['original_message']

        message_body = urllib.parse.unquote(original_message['text']).replace("+", " ").split("\n")
        if message_body == ['']:
            message_body = urllib.parse.unquote(original_message["attachments"][0]['text']).replace("+", " ").split(
                "\n")

        new_message = [message_body[0]]

        user_action = payload['actions'][0]['value'].replace('+', ' ')
        user_id = '<@' + payload['user']['id'] + '>'

        votes = {}
        for line in message_body[1::]:
            header, respondents = line.split(" -&gt; ")
            if "`" in header:
                header, _, _ = header.split("`")
                header = header.strip(" ")
            if header not in votes:
                votes[header] = []
            Stream(respondents.split(",")).forEach(lambda name: votes[header].append(name))

        if not multi:
            match = Stream(votes.items()).firstMatch(lambda option, voters: user_id in voters)
            if match:
                votes[match[0]].remove(user_id)

        if f"- {user_action}" not in votes:
            votes[f"- {user_action}"] = []
        if user_id not in votes[f"- {user_action}"]:
            votes[f"- {user_action}"].append(user_id)
        elif user_id in votes[f"- {user_action}"]:
            votes[f"- {user_action}"].remove(user_id)

        for line in message_body[1::]:
            header, respondents = line.split(" -&gt; ")
            if "`" in header:
                header, _, _ = header.split("`")
                header = header.strip(" ")
            if header not in votes:
                votes[header] = []
            respondents = ",".join(Stream(votes[header]).filter(lambda x: x not in ('', ' ')).toList())
            number_of_votes = Stream(votes[header]).filter(lambda x: x not in ('', ' ')).count()
            new_message.append(f"{header} `{number_of_votes}` -> {respondents}")

        original_message["attachments"][0]['text'] = "\n".join(new_message)
        for x in original_message['attachments']:
            x['actions'] = Stream(x['actions']).map(
                lambda action: {
                    "id": action['id'],
                    "name": action['name'],
                    "text": action['text'].replace('+', " "),
                    "type": action['type'],
                    'value': action['value'].replace('+', " "),
                    "style": action['style']
                }).toList()

        return original_message
