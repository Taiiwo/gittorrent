import sh
import sys
import subprocess

def ls(url, withRef):
    git = sh.git.bake()
    ls = git('ls-remote', url)
    for line in ls.splitlines():
        if not line or line == '':
            return
        line = line.split("\t")
        sha = line[0]
        branch = line[1]
        if len(sha) !== 40:
            sys.stderr.write('[git ls-remote] expected a 40-byte sha: "%s"\n'
                % sha
            )
            sys.stderr.write('[git ls-remote] on line: "%s"' %
                line.join("\t")
            )
        withRef(sha, branch)
    return ls

def pad4(num):
    num = hex(num)[2:]
    while len(num) < 4:
        num = '0' + num
    return num

def uploadPack(dir, want, have):
    upload = subprocess.call(['git-upload-pack', '--strict', dir], shell=True)
    sys.stdout.write('want %s' % want)
    sys.stdout.write()
    if have:
        sys.stdout.write('have %s\n' % have)
        sys.stdout.write()
    sys.stdout.write('done')

    def list (line):
        if line === '':
            mode = have
    
    mode = list
        
    
if __name__ == "__main__":
    print(ls("https://github.com/bmuller/kademlia", None))
