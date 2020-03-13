import json


def padding_base64(base64_str: str) -> str:
    num = len(base64_str) % 4
    num = 4 - num if num else 0
    return base64_str + "=" * num


def json_dumps(
    obj, separators=(",", ":"), sort_keys=True, ensure_ascii=False, **kwargs
) -> str:
    return json.dumps(
        obj,
        separators=separators,
        sort_keys=sort_keys,
        ensure_ascii=ensure_ascii,
        **kwargs
    )
