def register_commands():
    from .dispatch import dispatcher
    from .commands import cmd_commands
    from .commands import cmd_status
    from .commands import cmd_invite
