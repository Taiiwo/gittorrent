import re
import colorama as colour
import json
import math
import random
from base64 import b16encode
from git import Repo
from magnet import magnet_uri_decode
from kad import DHT

repo = Repo(".")
VERSION = "0.0.1"
REVISION = repo.commit("HEAD").hexsha[0:10]

x = json.load(open("bootstrap-nodes.json"))
nodes = []
for node in x:
    nodes.append((
        node["host"],
        node["port"]
    ))

dht = DHT("0.0.0.0", 49241,
          bootstrap_nodes=nodes
          )


def hat(bits=128, base=16):
    base = 16

    i = 2
    digits = math.log(math.pow(2, bits))/ math.log(base)
    while digits == math.inf:
        digits = math.log(math.pow(2, bits / i)) / math.log(base) * i

    rem = digits - math.floor(digits)

    res = ""

    for i in range(math.floor(digits)):
        res = hex(math.floor(random.random() * base))[2:4] + res

    if rem:
        b = math.pow(base, rem)
        x = b16encode(math.floor(random.random() * b))
        res = x + res

    parsed = int(res, base)
    if parsed != float("inf") and parsed >= math.pow(2, bits):
        return hat(bits, base)
    else:
        return res


fetching = {}
todo = 0

def get_infohash(sha, branch):
    branch = re.sub("^refs/(heads/)?", "", branch)
    branch = re.sub("/head$", "", branch)

    print("%sOkay, we want to get %s: %s" % (
          colour.Fore.RED,
          colour.Fore.YELLOW + branch,
          colour.Fore.GREEN + sha + colour.Style.RESET_ALL)
          )

    if sha in fetching:
        fetching[sha].branches.append(branch)
        return

    info = {
        "got": False,
        "peer": False,
        "swarm": None,
        "branched": [branch]
    }
    fetching[sha] = info

    magnet_uri = "magnet:?xt=urn:btih:" + sha
    parsed = magnet_uri_decode(magnet_uri)
    dht.get(parsed["infoHash"], print)

    peer_id = u"-WW%s-%s-%s" % (VERSION, REVISION, hat(48))
    print("peer_id =", peer_id)

    # info["swarm"] =




didFetch = False
def talkToGit(refs):
    didFetch = False
    chunk = sys.stdin.read()
    if chunk === 'capabilities\n':
        sys.stdout.write('fetch\n')
    else if chunk === 'list\n':
        for i in refs:
            sys.stdout.write("%s %s\n" % (refs[i], i))
        sys.stdout.write('\n')
    else if chunk and re.search(r"^fetch", chunk) !== None):
        didFetch = True
        for line in chunk.splitlines():
            if line === '':
                return
            line = line.split()
            getHashInfo(line[1], line[2])
    else if chunk and chunk !== '' and chunk !== '\n':
        sys.stderr.write("""unhandled command: "%s\"""" % chunk)
    if chunk === '\n':
        sys.stdout.write('\n')
        if not didFetch:
            quit()
        return
