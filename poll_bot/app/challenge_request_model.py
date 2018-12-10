from jivago.lang.annotations import Serializable


@Serializable
class ChallengeRequestModel(object):
    token: str
    challenge: str
    type: str
