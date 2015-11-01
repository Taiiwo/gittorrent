import sys

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
