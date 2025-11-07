"""
Pytest configuration for PhiGEN tests.

This file contains common fixtures and configuration for all tests.
"""

import sys
import os
import pytest
from pathlib import Path

# Add src directory to Python path for imports
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

# Test configuration
TEST_CONFIG = {
    "test_data_dir": Path(__file__).parent / "fixtures",
    "temp_dir": Path(__file__).parent / "temp",
}

@pytest.fixture(scope="session")
def test_config():
    """Provide test configuration to tests."""
    return TEST_CONFIG

@pytest.fixture
def temp_dir():
    """Provide a temporary directory for tests."""
    import tempfile
    import shutil
    
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)

# Mock external dependencies that might not be available
@pytest.fixture(autouse=True)
def mock_external_deps(monkeypatch):
    """Mock external dependencies that might not be available in test environment."""
    # Mock PyQt6
    mock_qt = pytest.importorskip("unittest.mock", reason="Testing environment")
    monkeypatch.setitem(sys.modules, "PyQt6", mock_qt.MagicMock())
    monkeypatch.setitem(sys.modules, "PyQt6.QtWidgets", mock_qt.MagicMock())
    
    # Mock discord
    monkeypatch.setitem(sys.modules, "discord", mock_qt.MagicMock())
    
    # Mock cryptography
    monkeypatch.setitem(sys.modules, "cryptography", mock_qt.MagicMock())