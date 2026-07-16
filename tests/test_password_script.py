import os
import stat
import tempfile
import unittest


def read_password_file(password_file):
    """Inline copy of the updated read_password_file for isolated testing."""
    import subprocess

    def is_executable(path):
        return ((stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH) & os.stat(path)[stat.ST_MODE])

    this_path = os.path.realpath(os.path.expanduser(password_file))
    if not os.path.exists(this_path):
        raise Exception("The password file %s was not found" % this_path)

    if is_executable(this_path):
        canonical_path = os.path.realpath(this_path)
        if not os.path.isfile(canonical_path):
            raise Exception("Password script path is not a regular file: %s" % canonical_path)
        if not os.access(canonical_path, os.X_OK):
            raise Exception("Password script is not executable: %s" % canonical_path)
        try:
            p = subprocess.Popen([canonical_path], stdout=subprocess.PIPE)
        except OSError as e:
            raise Exception("Problem running password script %s (%s)." % (canonical_path, e))
        stdout, stderr = p.communicate()
        try:
            password = stdout.decode('utf-8').strip()
        except UnicodeDecodeError:
            raise Exception("Password script output is not valid UTF-8: %s" % canonical_path)
    else:
        try:
            f = open(this_path, "rb")
            password = f.read().strip()
            f.close()
        except (OSError, IOError) as e:
            raise Exception("Could not read password file %s: %s" % (this_path, e))

    return password


class TestPasswordScript(unittest.TestCase):

    def test_valid_script_returns_password(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False) as f:
            f.write('#!/bin/sh\necho "mypassword"\n')
            script_path = f.name
        os.chmod(script_path, 0o755)
        try:
            result = read_password_file(script_path)
            self.assertEqual(result, 'mypassword')
        finally:
            os.unlink(script_path)

    def test_directory_path_raises(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(Exception) as ctx:
                read_password_file(d)
            self.assertIn('not a regular file', str(ctx.exception))

    def test_non_executable_file_read_as_plain_text(self):
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            f.write(b'secretpass')
            plain_path = f.name
        os.chmod(plain_path, 0o644)
        try:
            result = read_password_file(plain_path)
            self.assertEqual(result, b'secretpass')
        finally:
            os.unlink(plain_path)

    def test_non_utf8_output_raises(self):
        # Use a Python script to output raw non-UTF-8 bytes reliably
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('#!/usr/bin/env python3\nimport sys\nsys.stdout.buffer.write(b"\\x80\\x81")\n')
            script_path = f.name
        os.chmod(script_path, 0o755)
        try:
            with self.assertRaises(Exception) as ctx:
                read_password_file(script_path)
            self.assertIn('UTF-8', str(ctx.exception))
        finally:
            os.unlink(script_path)


if __name__ == '__main__':
    unittest.main()
