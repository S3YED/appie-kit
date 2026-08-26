import pathlib
import subprocess
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'tools/managed-software-update.sh'
INSTALL = ROOT / 'install.sh'


class ManagedUpdateProvisioningTest(unittest.TestCase):
    def test_updater_is_valid(self):
        self.assertTrue(SCRIPT.is_file())
        subprocess.run(['bash', '-n', str(SCRIPT)], check=True)
        text = SCRIPT.read_text()
        self.assertIn('hermes update --yes', text)
        self.assertNotIn('hermes update --yes --backup', text)
        self.assertIn('claude update', text)
        self.assertIn('apt-get', text)
        self.assertIn('brew', text)

    def test_installer_places_and_schedules_updater(self):
        text = INSTALL.read_text()
        self.assertIn('managed-software-update.sh', text)
        self.assertIn('$TARGET/scripts', text)
        self.assertIn('0 2 * * *', text)
        self.assertIn('crontab', text)


if __name__ == '__main__':
    unittest.main()
