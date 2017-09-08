#!/usr/bin/env python

from __future__ import with_statement

import os
import sys
import errno
import subprocess
import atexit
import uuid
import shutil
import tempfile
import io
import random

from fuse import FUSE, FuseOSError, Operations, fuse_get_context

class sregi_fuse(Operations):
    def __init__(self, root, sregdir):
        self.root = root
        self.sregdir = sregdir

        out = subprocess.check_output(["crystallize-getconf", "WorkDirectory"], shell=False)
        self.tempdir = out[:-1] + "/.sregi_fuse.tmp/" + str(uuid.uuid4())
        if not os.path.exists(self.tempdir):
            os.makedirs(self.tempdir)

    # Helpers
    # =======

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

    def _sreg_copy_read(self, source, destination):
        inputfile = io.open(source, 'r')
        # print("copy read source: "+source)
        outputfile = io.open(destination, 'w')
        # print("copy read outfile: "+outputfile.name)
        subprocess.call(["sreg_read_stream", "--sreg-dir", self.sregdir], stdin=inputfile, stdout=outputfile)

    def _sreg_copy_write(self, source, destination):
        inputfile = io.open(source, 'r')
        print("copy write source: "+source)
        # print("copy write outfile: "+destination)
        subprocess.call(["sreg_store_stream", "--sreg-dir", self.sregdir, "--output-file", destination], stdin=inputfile)

    # Filesystem methods
    # ==================

    def access(self, path, mode):
        full_path = self._full_path(path)
        if not os.access(full_path, mode):
            raise FuseOSError(errno.EACCES)

    def chmod(self, path, mode):
        full_path = self._full_path(path)
        return os.chmod(full_path, mode)

    def chown(self, path, uid, gid):
        full_path = self._full_path(path)
        return os.chown(full_path, uid, gid)

    def getattr(self, path, fh=None):
        full_path = self._full_path(path)
        st = os.lstat(full_path)
        statDict = dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                     'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))
        # for i in statDict:
        #     print i, statDict[i]
        expandedSize = subprocess.check_output(["sregi_get_length_from_pointer", "--sreg-dir", self.sregdir, full_path])
        print "getattr run on "+full_path+" and found length "+str(expandedSize)
        # Replace st_size value
        statDict.update({'st_size': int(expandedSize)})
        # for i in statDict:
        #     print i, statDict[i]
        return statDict

    def readdir(self, path, fh):
        full_path = self._full_path(path)

        dirents = ['.', '..']
        if os.path.isdir(full_path):
            dirents.extend(os.listdir(full_path))
        for r in dirents:
            yield r

    def readlink(self, path):
        pathname = os.readlink(self._full_path(path))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    def mknod(self, path, mode, dev):
        return os.mknod(self._full_path(path), mode, dev)

    def rmdir(self, path):
        full_path = self._full_path(path)
        return os.rmdir(full_path)

    def mkdir(self, path, mode):
        directory = os.mkdir(self._full_path(path), mode)
        keepfile = directory + '/.keep'
        subprocess.call(["touch", keepfile], shell=False)
        return directory

    def statfs(self, path):
        full_path = self._full_path(path)
        stv = os.statvfs(full_path)
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
            'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax'))

    def unlink(self, path):
        return os.unlink(self._full_path(path))

    def symlink(self, name, target):
        return os.symlink(name, self._full_path(target))

    def rename(self, old, new):
        return os.rename(self._full_path(old), self._full_path(new))

    def link(self, target, name):
        return os.link(self._full_path(target), self._full_path(name))

    def utimens(self, path, times=None):
        return os.utime(self._full_path(path), times)

    # File methods
    # ============

    def open(self, path, flags):
        full_path = self._full_path(path)
        temppath = self.tempdir + "/" + full_path
        if not os.path.exists(os.path.dirname(temppath)):
            os.makedirs(os.path.dirname(temppath))
        self._sreg_copy_read(full_path, temppath)
        print("copy read target for open: "+temppath)
        return os.open(temppath, flags)

    def create(self, path, mode, fi=None):
        uid, gid, pid = fuse_get_context()
        full_path = self._full_path(path)
        temppath = self.tempdir + "/" + full_path
        if not os.path.exists(os.path.dirname(temppath)):
            os.makedirs(os.path.dirname(temppath))
        if os.path.isfile(full_path):
            self._sreg_copy_read(full_path, temppath)
        else:
            subprocess.call(["touch", temppath], shell=False)
            self._sreg_copy_write(temppath, full_path)
        fd = os.open(temppath, os.O_WRONLY | os.O_CREAT, mode)
        os.chown(temppath,uid,gid) #chown to context uid & gid
        return fd

    def read(self, path, length, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

    def write(self, path, buf, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.write(fh, buf)

    def truncate(self, path, length, fh=None):
        full_path = self._full_path(path)
        temppath = self.tempdir + "/" + full_path
        if not os.path.exists(os.path.dirname(temppath)):
            os.makedirs(os.path.dirname(temppath))
        self._sreg_copy_read(full_path, temppath)
        with open(temppath, 'r+') as f:
            f.truncate(length)
        self._sreg_copy_write(temppath, full_path)

    def flush(self, path, fh):
        temp = os.fsync(fh)
        full_path = self._full_path(path)
        print("flush name: "+full_path)
        temppath = self.tempdir + "/" + full_path
        self._sreg_copy_write(temppath, full_path)
        return temp

    def release(self, path, fh):
        print("release name: "+path)
        self.flush(path, fh)
        temp = os.close(fh)
        if random.randint(-1,32768) < 250:
            subprocess.call(['sregi_fuse_cache_gc', self.tempdir])
        return temp

    def fsync(self, path, fdatasync, fh):
        return self.flush(path, fh)

# Mountpoint may not be a subdirectory of root, apparently. When running from the command line, specify the arguments in the opposite order (root then mountpoint).
def main(mountpoint, root, sregdir):
    srf = sregi_fuse(root, sregdir)
    tempdir = srf.tempdir
    FUSE(srf, mountpoint, nothreads=True, foreground=True, **{'allow_other': True})
    def exit_handler():
        # Clean up tempdir
        if not os.path.exists(tempdir):
            os.makedirs(tempdir)
        shutil.rmtree(tempdir)

    atexit.register(exit_handler)

if __name__ == '__main__':
    main(sys.argv[2], sys.argv[1], sys.argv[3])
