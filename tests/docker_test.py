import unittest
import subprocess

class DockerTest(unittest.TestCase):
    def docker_test(self):
        result = subprocess.run(["docker", "build", "--check", "."])
        self.assertEqual(result.returncode,0)
