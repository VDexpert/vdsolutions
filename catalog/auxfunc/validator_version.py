def do(version):
    if len(version) == len([x for x in version if x.isdigit() or x == '.']):
        return True