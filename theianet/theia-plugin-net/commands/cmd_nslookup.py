from TheiaPy.replies import *
from ..dispatch import dispatcher

RECORD_TYPES = ["A", "AAAA", "CNAME", "MX", "NS", "TXT", "PTR"]

@dispatcher.on_command("nslookup")
def cmd_nslookup(mdata):
    try:
        import dns
        import dns.resolver
    except ImportError:
        message = SendMessage().in_reply_to(mdata["message"])
        message["content"] = "\U0000274c `dns` could not be imported."
        return message.emit()

    record_type = (["A"] + [fl[1:] for fl in mdata["cmd"]["start_flags"] if fl[1:] in RECORD_TYPES])[-1]
    nameserver = (["9.9.9.9"] + [fl[1:] for fl in mdata["cmd"]["arguments"] if fl.startswith("&")])[-1]
    host = mdata["cmd"]["arguments"][0]

    try:
        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = [nameserver]

        answer = resolver.resolve(host, rdtype=record_type, raise_on_no_answer=True)
        status = [
            f"`{host}` ({record_type} records, nameserver: `{nameserver}`)",
            "```",
            answer.rrset.to_text(),
            "```",
        ]

    except dns.resolver.LifetimeTimeout:
        status = [f"\U0001f6d1 Timeout while resolving (nameserver: `{nameserver}`)"]

    except dns.resolver.NoNameservers:
        status = [f"\U0001f6d1 Could not reach nameserver: `{nameserver}`"]

    except dns.resolver.NXDOMAIN:
        status = [f"\U0001f6d1 `{host}` is NXDOMAIN"]

    except dns.resolver.NoAnswer:
        status = [f"\U0001f6d1 `{host}` has no {record_type} records"]

    message = SendMessage().in_reply_to(mdata["message"])
    message["content"] = "\n".join(status)
    message.emit()
