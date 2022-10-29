import version
if version.local() < version.remote():
    print("needs update")
else:
    print("is fine")
