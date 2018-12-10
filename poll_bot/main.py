from jivago.jivago_application import JivagoApplication

import poll_bot.app

application = JivagoApplication(poll_bot.app)

if __name__ == '__main__':
    application.run_dev()
