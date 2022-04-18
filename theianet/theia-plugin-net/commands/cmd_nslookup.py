import TheiaPy
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
        message["content"] = " ".join([TheiaPy.emoji("error"), "`dns` could not be imported."])
        return message.emit()

    host = mdata["cmd"]["arguments"][0]
    record_type = (
        [RECORD_TYPES[0]]
        + [fl[1:] for fl in mdata["cmd"]["start_flags"] if fl[1:] in RECORD_TYPES]
    )[-1]
    nameserver = (
        [dispatcher.config_get("default-nameserver", "9.9.9.9")] 
        + [fl[1:] for fl in mdata["cmd"]["arguments"] if fl.startswith("&")]
    )[-1]

    try:
        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = [nameserver]

        answer = resolver.resolve(host, rdtype=record_type, raise_on_no_answer=True)
        status = [
            TheiaPy.emoji("success") + f" `{host}` ({record_type} records, nameserver: `{nameserver}`)",
            "```",
            answer.rrset.to_text(),
            "```",
        ]

    except dns.resolver.LifetimeTimeout:
        status = [TheiaPy.emoji("warning") + f" Timeout while resolving (nameserver: `{nameserver}`)"]

    except dns.resolver.NoNameservers:
        status = [TheiaPy.emoji("warning") + f" Could not reach nameserver: `{nameserver}`"]

    except dns.resolver.NXDOMAIN:
        status = [TheiaPy.emoji("warning") + f" `{host}` is NXDOMAIN"]

    except dns.resolver.NoAnswer:
        status = [TheiaPy.emoji("warning") + f" `{host}` has no {record_type} records"]

    message = SendMessage().in_reply_to(mdata["message"])
    message["content"] = "\n".join(status)
    message.emit()
