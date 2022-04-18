import random

import TheiaPy
from TheiaPy.replies import *
from ..dispatch import dispatcher

@dispatcher.on_command("commands")
def cmd_commands(mdata):
    message = SendMessage().in_reply_to(mdata["message"])
    message["content"] = "\n".join([
        (
            "Available commands: " 
            + ", ".join(["`" + dispatcher.bot_info["prefixes"][0] + a[0] + "`" for a in dispatcher.bot_info["commands"]])
        ),
        "",
        (
            "Add the `-help` flag to a command for details - for example, try `"
            + dispatcher.bot_info["prefixes"][0] 
            + random.choice(dispatcher.bot_info["commands"])[0]
            + " -help`."
        ),
        (
            "For more information about Theia, see the website: <https://theia.irys.cc>"
        ),
    ])

    message.emit()
