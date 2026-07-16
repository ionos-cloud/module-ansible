import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch


def _validate_file_path(module, path, param_name):
    if path is None:
        return
    canonical = os.path.realpath(path)
    if not os.path.isfile(canonical):
        module.fail_json(msg="invalid file path for parameter '%s'" % param_name)


class TestCertificatePathValidation(unittest.TestCase):

    def _module(self):
        m = MagicMock()
        m.fail_json.side_effect = SystemExit(1)
        return m

    def test_valid_path_passes(self):
        module = self._module()
        with tempfile.NamedTemporaryFile(delete=False) as f:
            path = f.name
        try:
            _validate_file_path(module, path, 'certificate_file')
            module.fail_json.assert_not_called()
        finally:
            os.unlink(path)

    def test_traversal_path_fails(self):
        module = self._module()
        with self.assertRaises(SystemExit):
            _validate_file_path(module, '../../etc/passwd', 'certificate_file')
        module.fail_json.assert_called_once()
        self.assertIn('invalid file path', module.fail_json.call_args[1]['msg'])

    def test_missing_file_fails(self):
        module = self._module()
        with self.assertRaises(SystemExit):
            _validate_file_path(module, '/nonexistent/path/cert.pem', 'certificate_file')
        module.fail_json.assert_called_once()

    def test_symlink_resolved_canonical(self):
        module = self._module()
        with tempfile.NamedTemporaryFile(delete=False) as f:
            real_path = f.name
        link_path = real_path + '.link'
        os.symlink(real_path, link_path)
        try:
            _validate_file_path(module, link_path, 'certificate_file')
            module.fail_json.assert_not_called()
        finally:
            os.unlink(link_path)
            os.unlink(real_path)

    def test_none_path_skipped(self):
        module = self._module()
        _validate_file_path(module, None, 'certificate_chain_file')
        module.fail_json.assert_not_called()


class TestALBCertificatePathValidation(unittest.TestCase):
    """Tests for application_load_balancer_forwardingrule path validation."""

    def _module(self):
        m = MagicMock()
        m.fail_json.side_effect = SystemExit(1)
        return m

    def _validate_cert_file_path(self, module, path, key):
        if path is None:
            return
        canonical = os.path.realpath(path)
        if not os.path.isfile(canonical):
            module.fail_json(msg="invalid file path for certificate parameter '%s'" % key)

    def _make_cert_input(self, cert_file=None, key_file=None, chain_file=None):
        return {
            'certificate_file': cert_file,
            'private_key_file': key_file,
            'certificate_chain_file': chain_file,
            'certificate_name': 'test',
        }

    def test_valid_paths_pass(self):
        module = self._module()
        with tempfile.NamedTemporaryFile(delete=False) as cert, \
             tempfile.NamedTemporaryFile(delete=False) as key, \
             tempfile.NamedTemporaryFile(delete=False) as chain:
            try:
                inp = self._make_cert_input(cert.name, key.name, chain.name)
                self._validate_cert_file_path(module, inp['certificate_file'], 'certificate_file')
                self._validate_cert_file_path(module, inp['private_key_file'], 'private_key_file')
                self._validate_cert_file_path(module, inp['certificate_chain_file'], 'certificate_chain_file')
                module.fail_json.assert_not_called()
            finally:
                os.unlink(cert.name)
                os.unlink(key.name)
                os.unlink(chain.name)

    def test_traversal_certificate_file_fails(self):
        module = self._module()
        with self.assertRaises(SystemExit):
            self._validate_cert_file_path(module, '../../etc/passwd', 'certificate_file')
        module.fail_json.assert_called_once()

    def test_traversal_private_key_file_to_nonexistent_fails(self):
        module = self._module()
        with self.assertRaises(SystemExit):
            self._validate_cert_file_path(module, '/nonexistent/../../private.key', 'private_key_file')
        module.fail_json.assert_called_once()

    def test_traversal_chain_file_fails(self):
        module = self._module()
        with self.assertRaises(SystemExit):
            self._validate_cert_file_path(module, '../../etc/hosts', 'certificate_chain_file')
        module.fail_json.assert_called_once()


class TestK8sConfigPathValidation(unittest.TestCase):
    """Tests for k8s_config.py write-path validation."""

    def _module(self):
        m = MagicMock()
        m.fail_json.side_effect = SystemExit(1)
        return m

    def _validate_config_path(self, module, config_file):
        import stat as _stat
        canonical = os.path.realpath(config_file)
        parent_dir = os.path.dirname(canonical)
        if not os.path.isdir(parent_dir):
            module.fail_json(msg="invalid file path for parameter 'config_file': parent directory does not exist")
        parent_st = os.stat(parent_dir)
        if parent_st.st_mode & _stat.S_IWOTH:
            module.warn("config_file parent directory '%s' is world-writable" % parent_dir)

    def test_valid_path_passes(self):
        module = self._module()
        with tempfile.TemporaryDirectory() as d:
            config_file = os.path.join(d, 'kubeconfig.yaml')
            self._validate_config_path(module, config_file)
            module.fail_json.assert_not_called()

    def test_missing_parent_dir_fails(self):
        module = self._module()
        with self.assertRaises(SystemExit):
            self._validate_config_path(module, '/nonexistent/dir/kubeconfig.yaml')
        module.fail_json.assert_called_once()
        self.assertIn('parent directory does not exist', module.fail_json.call_args[1]['msg'])

    def test_traversal_to_nonexistent_parent_fails(self):
        module = self._module()
        with self.assertRaises(SystemExit):
            self._validate_config_path(module, '/nonexistent_root/sub/kubeconfig.yaml')
        module.fail_json.assert_called_once()

    def test_symlink_resolved_canonical_parent(self):
        module = self._module()
        with tempfile.TemporaryDirectory() as d:
            config_file = os.path.join(d, 'config.yaml')
            self._validate_config_path(module, config_file)
            module.fail_json.assert_not_called()


if __name__ == '__main__':
    unittest.main()
