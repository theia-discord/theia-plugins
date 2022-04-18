import TheiaPy
from TheiaPy.replies import *
from ..dispatch import dispatcher

@dispatcher.on_command("status")
def cmd_status(mdata):
    binfo = [
        "{plugins} loaded plugins, with {commands} public commands".format(**{
            "plugins": len(dispatcher.bot_info["plugins"]),
            "commands": len(dispatcher.bot_info["commands"]),
        }),
        "on shard {this_shard} of {total_shards}".format(**dispatcher.bot_info),
    ]

    message = SendMessage().in_reply_to(mdata["message"])
    message["content"] = " ".join([
        TheiaPy.emoji("robot"), 
        "Hi! I'm Theia - <https://theia.irys.cc>",
        "\n\n{binfo}"
    ]).format(**{
        "binfo": "> \u2022 " + "\n> \u2022 ".join(binfo),
    })

    message.emit()
