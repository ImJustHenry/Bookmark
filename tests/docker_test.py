import unittest
import subprocess
import os

class DockerTest(unittest.TestCase):
    def test_docker_build(self):
        """Test that Docker image can be built successfully"""
        # Get the project root directory (parent of tests directory)
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        
        # Build Docker image with a test tag
        result = subprocess.run(
            ["docker", "build", "-t", "bookmark-app:test", "."],
            cwd=project_root,
            capture_output=True,
            text=True
        )
        
        # Check that build succeeded
        self.assertEqual(
            result.returncode, 
            0, 
            f"Docker build failed. Error: {result.stderr}"
        )

