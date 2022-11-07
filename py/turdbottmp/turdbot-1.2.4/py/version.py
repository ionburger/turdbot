import subprocess

def remote():
    try:
        process = subprocess.Popen(["lastversion", "ionburger/turdbot"],stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return (process.communicate()[0])
    except:
        return 0
def local():
    return open("VERSION","r").read()