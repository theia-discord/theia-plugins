import TheiaPy
from TheiaPy.replies import *
from ..dispatch import dispatcher

@dispatcher.on_command("invite")
def cmd_invite(mdata):
    message = SendMessage().in_reply_to(mdata["message"])

    if dispatcher.bot_info["invite_url"] is not None:
        message["content"] = " ".join([
            TheiaPy.emoji("robot"),
            "Use this link to invite me to your server:",
            dispatcher.bot_info["invite_url"]
        ])

    else:
        message["content"] = " ".join([
            TheiaPy.emoji("warning"),
            "Sorry, I couldn't get an invite link!",
        ])

    message.emit()
