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
            val = unquote(val).replace("+", " ")

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

        for xt in xts:
            m = re.match("^urn:btih:(.{40})", xt)
            if m:
                result["infoHash"] = m.groups(0)  # might need conversion
            else:
                m = re.match("^urn:btih:(.{32})", xt)
                if m:
                    decoded_string = b32decode(m.groups(0))
                    result["infoHash"] = b16encode(decoded_string)

    if "dn" in result:
        result["name"] = result["dn"]


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

    if "as" in result and isinstance(result["as"], (str, list)):
            result["urlList"].extend(result["as"])

    if "ws" in result and isinstance(result["ws"], (str, list)):
            result["urlList"].extend(result["ws"])

    return result


def magnet_uri_encode(obj):
    mutated_obj = obj

    if "infoHash" in obj:
        mutated_obj["xt"] = "urn:btih:" + obj["infoHash"]
    if "name" in obj:
        mutated_obj["dn"] = obj["name"]
    if "keywords" in obj:
        mutated_obj["kt"] = obj["keywords"]
    if "announce" in obj:
        mutated_obj["tr"] = obj["announce"]
    if "urlList" in obj:
        mutated_obj["ws"] = obj["urlList"]
        if "as" in obj:
            del(mutated_obj["as"])

    result = "magnet:?"

    i = 0
    for key in mutated_obj.keys():
        if len(key) != 2:
            continue

        values = mutated_obj[key] if isinstance(mutated_obj[key], (list, tuple)) else [mutated_obj[key]]

        j = 0
        for val in values:
            if (i > 0 or j > 0) and (key != "kt" or j == 0):
                result += "&"

            if key == "dn":
                val = quote(val).replace("%20", "+")

            if key in ["tr", "xs", "as", "ws"]:
                val = quote(val)

            if key == "kt":
                val = quote(val)

            if key == "kt" and j > 0:
                result += "+" + val
            else:
                result += key + "=" + val
            j += 1
        i += 1

    return result



