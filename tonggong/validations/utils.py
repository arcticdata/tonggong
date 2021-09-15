import ipaddress
import re

from .errors import EmailError


def _validate_ipv4_address(value):
    try:
        ipaddress.IPv4Address(value)
    except ValueError:
        raise EmailError("invalid IPv4 address.")
    else:
        # Leading zeros are forbidden to avoid ambiguity with the octal
        # notation. This restriction is included in Python 3.9.5+.
        # TODO: Remove when dropping support for PY39.
        if any(octet != "0" and octet[0] == "0" for octet in value.split(".")):
            raise EmailError("invalid IPv4 address.")


def _is_valid_ipv6_address(ip_str):
    """
    Return whether or not the `ip_str` string is a valid IPv6 address.
    """
    try:
        ipaddress.IPv6Address(ip_str)
    except ValueError:
        return False
    return True


def _validate_ipv6_address(value):
    if not _is_valid_ipv6_address(value):
        raise EmailError("invalid IPv6 address.")


def _validate_ipv46_address(value):
    try:
        _validate_ipv4_address(value)
    except Exception:
        try:
            _validate_ipv6_address(value)
        except Exception:
            raise EmailError("invalid IPv4 or IPv6 address.")


class EmailValidate(object):
    message = "Enter a valid email address."
    code = "invalid"
    user_regex = re.compile(
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*\Z"  # dot-atom
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"\Z)',  # quoted-string
        re.IGNORECASE,
    )
    domain_regex = re.compile(
        # max length for domain name labels is 63 characters per RFC 1034
        r"((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+)(?:[A-Z0-9-]{2,63}(?<!-))\Z",
        re.IGNORECASE,
    )
    literal_regex = re.compile(
        # literal form, ipv4 or ipv6 address (SMTP 4.1.3)
        r"\[([A-f0-9:.]+)\]\Z",
        re.IGNORECASE,
    )
    domain_allowlist = ["localhost"]

    def __init__(self, message=None, code=None, allowlist=None, *, whitelist=None):
        if whitelist is not None:
            allowlist = whitelist
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        if allowlist is not None:
            self.domain_allowlist = allowlist

    def __call__(self, value):
        if not value or "@" not in value:
            raise EmailError(self.message)

        user_part, domain_part = value.rsplit("@", 1)

        if not self.user_regex.match(user_part):
            raise EmailError(self.message)

        if domain_part not in self.domain_allowlist and not self.validate_domain_part(domain_part):
            # Try for possible IDN domain-part
            try:
                domain_part = domain_part.encode("idna").decode("ascii")
            except UnicodeError:
                pass
            else:
                if self.validate_domain_part(domain_part):
                    return
            raise EmailError(self.message)

    def __eq__(self, other):
        return (
            isinstance(other, EmailValidate)
            and (self.domain_allowlist == other.domain_allowlist)
            and (self.message == other.message)
            and (self.code == other.code)
        )

    def validate_domain_part(self, domain_part):
        if self.domain_regex.match(domain_part):
            return True

        literal_match = self.literal_regex.match(domain_part)
        if literal_match:
            ip_address = literal_match[1]
            try:
                _validate_ipv46_address(ip_address)
                return True
            except Exception:
                pass
        return False
