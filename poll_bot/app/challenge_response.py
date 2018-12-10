from jivago.wsgi.annotations import Resource
from jivago.wsgi.methods import POST

from poll_bot.app.challenge_request_model import ChallengeRequestModel


@Resource("/")
class ChallengeResponse(object):

    @POST
    def challenge(self, body: ChallengeRequestModel) -> str:
        return body.challenge
