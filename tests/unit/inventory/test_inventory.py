"""Unit tests for plugins/inventory/inventory.py security fixes."""

import os
import sys
import stat
import json
import tempfile
import importlib.util
import unittest
import configparser  # must be imported before _load_inventory_module() so patch.dict doesn't evict it
from unittest.mock import patch, MagicMock, call

# ── module-level setup ────────────────────────────────────────────────────────

_INVENTORY_PATH = os.path.join(
    os.path.dirname(__file__), '..', '..', '..', 'plugins', 'inventory', 'inventory.py'
)
_INVENTORY_PATH = os.path.realpath(_INVENTORY_PATH)


def _load_inventory_module(extra_sys_modules=None):
    """Load inventory.py with ionoscloud mocked out.

    Returns the loaded module object. The module-level IonosCloudInventory()
    call runs but completes silently (no credentials → token='', which is
    falsy but hasattr fires, mock API returns empty data).
    """
    ionoscloud_mock = MagicMock()
    ionoscloud_mock.__version__ = '6.0.0'

    mods = {
        'ionoscloud': ionoscloud_mock,
        'ionoscloud.Configuration': ionoscloud_mock.Configuration,
        'ionoscloud.ApiClient': ionoscloud_mock.ApiClient,
    }
    if extra_sys_modules:
        mods.update(extra_sys_modules)

    orig_argv = sys.argv
    sys.argv = ['inventory.py']
    try:
        with patch.dict(sys.modules, mods):
            spec = importlib.util.spec_from_file_location('inventory_test_module', _INVENTORY_PATH)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
        return mod
    finally:
        sys.argv = orig_argv


# Load once for most tests.
_inventory_mod = _load_inventory_module()
IonosCloudInventory = _inventory_mod.IonosCloudInventory


def _make_instance(**kwargs):
    """Create an IonosCloudInventory without running __init__."""
    obj = object.__new__(IonosCloudInventory)
    for k, v in kwargs.items():
        setattr(obj, k, v)
    return obj


# ── tests ─────────────────────────────────────────────────────────────────────

class TestCacheFilename(unittest.TestCase):
    """8.1 – cache filename uses .json extension; default cache_path updated."""

    def test_cache_filename_extension(self):
        """cache_filename must end with .json, not .pkl."""
        with tempfile.TemporaryDirectory() as tmp:
            obj = _make_instance(
                cache_path=tmp,
                cache_max_age=0,
            )
            obj.cache_filename = tmp + '/ansible-ionos.json'
            self.assertTrue(obj.cache_filename.endswith('.json'))
            self.assertFalse(obj.cache_filename.endswith('.pkl'))

    def test_default_cache_path_in_ini(self):
        """inventory.ini default cache_path must be ~/.cache/ansible-ionos."""
        import configparser
        ini_path = os.path.join(os.path.dirname(_INVENTORY_PATH), 'inventory.ini')
        cfg = configparser.ConfigParser()
        cfg.read(ini_path)
        self.assertEqual(cfg.get('ionos', 'cache_path'), '~/.cache/ansible-ionos')


class TestLoadFromCacheNoPickle(unittest.TestCase):
    """8.2 – malicious pickle file at cache path must NOT be loaded."""

    def test_pickle_file_not_loaded(self):
        """A .pkl file placed at cache_path must not be deserialized."""
        import pickle

        with tempfile.TemporaryDirectory() as tmp:
            # Write a pickle payload (would run code if deserialized)
            pkl_path = os.path.join(tmp, 'ansible-ionos.pkl')
            with open(pkl_path, 'wb') as f:
                pickle.dump({'data': {}, 'inventory': {}}, f)

            json_path = os.path.join(tmp, 'ansible-ionos.json')
            obj = _make_instance(cache_filename=json_path)

            # load_from_cache must raise (no .json file) not silently load .pkl
            with self.assertRaises((json.JSONDecodeError, OSError, FileNotFoundError)):
                obj.load_from_cache()

            # Verify pickle was never read
            self.assertFalse(os.path.exists(json_path), "No .json file should have been created")


class TestWriteToCacheMode(unittest.TestCase):
    """8.3 – write_to_cache() must create the cache file with mode 0600."""

    def test_cache_file_mode_0600(self):
        with tempfile.TemporaryDirectory() as tmp:
            json_path = os.path.join(tmp, 'ansible-ionos.json')
            obj = _make_instance(
                cache_filename=json_path,
                data={},
                inventory={},
            )
            obj.write_to_cache()
            file_mode = stat.S_IMODE(os.stat(json_path).st_mode)
            self.assertEqual(file_mode, 0o600,
                             "cache file must have mode 0600, got %s" % oct(file_mode))


class TestCredentialPermissionWarning(unittest.TestCase):
    """8.4 – permission warning uses os.path.abspath(config_path)."""

    def test_warning_contains_abspath(self):
        """Warning written to stderr must include the absolute path of the config file."""
        import io

        # config_path computed inside read_settings() for the real inventory.ini
        config_path = (
            os.path.dirname(os.path.realpath(_INVENTORY_PATH)) + '/inventory.ini'
        )
        expected_path = os.path.abspath(config_path)

        obj = object.__new__(IonosCloudInventory)
        obj.cache_path = '.'
        obj.cache_max_age = 0
        obj.vars = {}
        obj.regex_group_list = []

        stderr_capture = io.StringIO()

        # Patch ConfigParser.read to inject a non-empty token
        def patched_read(self_cfg, path, encoding=None):
            self_cfg.read_string('[ionos]\ntoken = secret\nusername =\npassword =\n')

        # Fake stat result: group-readable (0o640)
        fake_stat = MagicMock()
        fake_stat.st_mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP

        with patch.object(configparser.ConfigParser, 'read', patched_read), \
             patch('os.stat', return_value=fake_stat), \
             patch('sys.stderr', stderr_capture):
            obj.read_settings()

        warning = stderr_capture.getvalue()
        self.assertIn(expected_path, warning,
                      "Warning must contain abspath of config file; got: %r" % warning)


class TestNoSixDependency(unittest.TestCase):
    """8.5 – inventory.py must not require six; importing with six=None must not raise."""

    def test_import_without_six(self):
        """Inserting sys.modules['six'] = None must not cause ImportError."""
        mod = _load_inventory_module(extra_sys_modules={'six': None, 'six.moves': None})
        self.assertIsNotNone(mod.IonosCloudInventory)

    def test_configparser_used_directly(self):
        """Module must use stdlib configparser, not six.moves.configparser."""
        # The module must have imported configparser as a module attribute
        self.assertTrue(
            hasattr(_inventory_mod, 'configparser') or
            isinstance(getattr(_inventory_mod, 'configparser', None), type(configparser)),
            "inventory module should use stdlib configparser"
        )


class TestIsValidCacheLegacyPkl(unittest.TestCase):
    """8.6 – is_cache_valid() returns False when only a .pkl file exists."""

    def test_pkl_only_returns_false(self):
        with tempfile.TemporaryDirectory() as tmp:
            # Create only the legacy .pkl file
            pkl_path = os.path.join(tmp, 'ansible-ionos.pkl')
            with open(pkl_path, 'wb') as f:
                f.write(b'pkl_data')

            # cache_filename points to .json
            json_path = os.path.join(tmp, 'ansible-ionos.json')
            obj = _make_instance(
                cache_filename=json_path,
                cache_max_age=3600,
            )
            self.assertFalse(obj.is_cache_valid(),
                             "is_cache_valid() must return False when only .pkl file exists")


class TestWriteToCacheNoFileNotFoundError(unittest.TestCase):
    """8.7 – write_to_cache() finally block must not raise FileNotFoundError after rename."""

    def test_no_file_not_found_after_rename(self):
        """After successful os.rename, finally block must not call os.unlink(tmp_path)."""
        with tempfile.TemporaryDirectory() as tmp:
            json_path = os.path.join(tmp, 'ansible-ionos.json')
            obj = _make_instance(
                cache_filename=json_path,
                data={'servers': []},
                inventory={'all': {'hosts': []}, '_meta': {'hostvars': {}}},
            )
            # Must complete without raising FileNotFoundError
            try:
                obj.write_to_cache()
            except FileNotFoundError as e:
                self.fail("write_to_cache() raised FileNotFoundError: %s" % e)

            # Verify temp file was cleaned up (renamed away)
            tmp_path = json_path + '.tmp'
            self.assertFalse(os.path.exists(tmp_path),
                             ".tmp file must not remain after successful write")
            self.assertTrue(os.path.exists(json_path), "cache file must exist")


if __name__ == '__main__':
    unittest.main()
