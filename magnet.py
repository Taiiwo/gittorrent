from urllib.parse import quote, unquote
from base64 import b32decode, b32encode, b16decode, b16encode
import re


def magnet_uri_decode(uri):
    result = {}
    try:
        data = uri.split("magnet:?")[1]
        params = data.split("&")
    except IndexError:
        params = []

    for param in params:
        keyval = param.split("=")

        if len(keyval) != 2:
            continue

        key = keyval[0]
        val = keyval[1]

        if key == "dn":
            val = re.sub("\+", " ", unquote(val))

        if key in ["tr", "xs", "as", "ws"]:
            val = unquote(val)

        if key == "kt":
            val = unquote(val).split("+")

        if key in result:
            if isinstance(result[key], list):
                result[key].append(val)
            else:
                old = result[key]
                result[key] = [old, val]
        else:
            result[key] = val

    m = None
    if "xt" in result:
        xts = result["xt"] if isinstance(result["xt"], list) else [result["xt"]]

        for xt in result["xts"]:
            m = re.match("^urn:bith:(.{40})", xt)
            if m:
                print("m:", m)
                result["infoHash"] = m[1]  # might need conversion
            else:
                m = re.match("^urn:bith:(.{32})", xt)
                if m:
                    decoded_string = b32decode(m[1])
                    result["infoHash"] = b16encode(decoded_string)

    if "dn" in result:
        result["name"] = "dn"

    if "kt" in result:
        result["keywords"] = result["kt"]

    if "tr" in result:
        if isinstance(result["tr"], str):
            result["announce"] = [result["tr"]]
        elif isinstance(result["tr"], list):
            result["announce"] = result["tr"]
        else:
            result["announce"] = []

    # uniq(result["announce"])

    result["urlList"] = []

    if result["as"] and isinstance(result["as"], (str, list)):
            result["urlList"].extend(result["as"])

    if result["ws"] and isinstance(result["ws"], (str, list)):
            result["urlList"].extend(result["ws"])

    return result



