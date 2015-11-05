import sys
import subprocess

def ls(url, withRef, callback):# tested
    ls = subprocess.check_output(['git', 'ls-remote', url])
    ret = []
    for line in ls.splitlines():
        if not line or line == '':
            return
        line = line.split()
        sha = line[0]
        branch = line[1]
        ret.append([sha, branch])
        if len(sha) != 40:
            sys.stderr.write('[git ls-remote] expected a 40-byte sha: "%s"\n'
                % sha
            )
            sys.stderr.write('[git ls-remote] on line: "%s"' %
                line.join("\t")
            )
        withRef(sha, branch)
    callback(ret)
    return ret

def pad4(num):
    num = hex(num)[2:]
    while len(num) < 4:
        num = '0' + num
    return num

def uploadPack(dir, want, have):
    upload = subprocess.check_output(['git-upload-pack', '--strict', dir])
    sys.stdout.write('want %s' % want)
    sys.stdout.write()
    if have:
        sys.stdout.write('have %s\n' % have)
        sys.stdout.write()
    sys.stdout.write('done')

    def list (line):
        if line == '':
            mode = have
    
    mode = list
        
    
if __name__ == "__main__":
    print(ls("https://github.com/bmuller/kademlia", print))
