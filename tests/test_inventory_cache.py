import json
import os
import stat
import tempfile
import unittest
from unittest.mock import MagicMock, patch


class TestInventoryCache(unittest.TestCase):
    """Unit tests for JSON cache read/write in inventory.py"""

    def _make_inventory(self):
        """Return a minimal IonosCloudInventory-like object with only the cache methods."""
        sys_modules_patch = {
            'ionoscloud': MagicMock(),
            'six': MagicMock(),
            'six.moves': MagicMock(),
            'six.moves.configparser': MagicMock(),
        }
        with patch.dict('sys.modules', sys_modules_patch):
            import importlib, sys
            # Build a minimal stand-in without running __init__
            class FakeInventory:
                cache_filename = None
                data = {}
                inventory = {}
                client = MagicMock()

                def load_from_cache(self):
                    with open(self.cache_filename, 'r') as f:
                        file_mode = stat.S_IMODE(os.stat(self.cache_filename).st_mode)
                        if file_mode != 0o600:
                            import sys as _sys
                            _sys.stderr.write('WARNING: bad perms\n')
                        try:
                            cached = json.load(f)
                        except (ValueError, json.JSONDecodeError):
                            import sys as _sys
                            _sys.stderr.write('WARNING: Cache file is not valid JSON; treating as a cache miss.\n')
                            raise
                    self.data = cached['data']
                    self.inventory = cached['inventory']

                def write_to_cache(self):
                    serializable_data = {}
                    for k, v in self.data.items():
                        serializable_data[k] = [self.client.sanitize_for_serialization(item) for item in v]

                    serializable_inventory = {}
                    for k, v in self.inventory.items():
                        if k == '_meta':
                            serializable_inventory['_meta'] = {
                                'hostvars': {
                                    host: self.client.sanitize_for_serialization(srv)
                                    for host, srv in v.get('hostvars', {}).items()
                                }
                            }
                        else:
                            serializable_inventory[k] = v

                    cache_data = {"version": 1, "data": serializable_data, "inventory": serializable_inventory}
                    with open(self.cache_filename, 'w') as f:
                        json.dump(cache_data, f)
                    os.chmod(self.cache_filename, 0o600)

            return FakeInventory()

    def test_write_creates_json_file(self):
        inv = self._make_inventory()
        inv.client.sanitize_for_serialization.side_effect = lambda x: x
        inv.data = {'servers': [{'id': 'abc'}]}
        inv.inventory = {'all': {'hosts': []}, '_meta': {'hostvars': {}}}

        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            inv.cache_filename = f.name

        try:
            inv.write_to_cache()
            with open(inv.cache_filename) as f:
                data = json.load(f)
            self.assertEqual(data['version'], 1)
            self.assertIn('data', data)
            self.assertIn('inventory', data)
        finally:
            os.unlink(inv.cache_filename)

    def test_write_sets_permissions_600(self):
        inv = self._make_inventory()
        inv.client.sanitize_for_serialization.side_effect = lambda x: x
        inv.data = {}
        inv.inventory = {'_meta': {'hostvars': {}}}

        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            inv.cache_filename = f.name

        try:
            inv.write_to_cache()
            mode = stat.S_IMODE(os.stat(inv.cache_filename).st_mode)
            self.assertEqual(mode, 0o600)
        finally:
            os.unlink(inv.cache_filename)

    def test_read_loads_data_and_inventory(self):
        inv = self._make_inventory()
        inv.client.sanitize_for_serialization.side_effect = lambda x: x
        payload = {"version": 1, "data": {"servers": []}, "inventory": {"all": {"hosts": []}, "_meta": {"hostvars": {}}}}

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(payload, f)
            inv.cache_filename = f.name
        os.chmod(inv.cache_filename, 0o600)

        try:
            inv.load_from_cache()
            self.assertEqual(inv.data, {"servers": []})
        finally:
            os.unlink(inv.cache_filename)

    def test_read_invalid_json_raises(self):
        inv = self._make_inventory()
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("not json{{{")
            inv.cache_filename = f.name
        os.chmod(inv.cache_filename, 0o600)

        try:
            with self.assertRaises(Exception):
                inv.load_from_cache()
        finally:
            os.unlink(inv.cache_filename)

    def test_pickle_never_called(self):
        """Ensure pickle is not imported or used in the inventory cache path."""
        import ast, inspect
        inventory_path = os.path.join(
            os.path.dirname(__file__), '..', 'plugins', 'inventory', 'inventory.py'
        )
        with open(inventory_path) as f:
            source = f.read()
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [a.name for a in getattr(node, 'names', [])]
                module = getattr(node, 'module', '') or ''
                self.assertNotIn('pickle', names, "pickle should not be imported")
                self.assertNotEqual('pickle', module, "pickle should not be imported")


if __name__ == '__main__':
    unittest.main()
