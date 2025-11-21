"""
Unit tests for installed_software_service module.
Tests software listing and file saving functionality.
"""
import pytest
import json
from unittest.mock import patch, MagicMock
from pathlib import Path
import tempfile
import os
from services.installed_software_service import (
    list_installed_software,
    save_software_list_to_file,
    check_blacklisted_software
)


class TestListInstalledSoftware:
    """Test cases for list_installed_software function"""

    @patch('services.installed_software_service.winreg')
    def test_list_installed_software_registry_error(self, mock_winreg):
        """Test handling of registry access errors"""
        mock_winreg.OpenKey.side_effect = FileNotFoundError()

        result = list_installed_software()

        assert result == []

    def test_list_installed_software_returns_list(self):
        """Test that function returns a list"""
        result = list_installed_software()
        assert isinstance(result, list)

    def test_list_installed_software_structure(self):
        """Test that software entries have expected structure"""
        result = list_installed_software()

        if result:  # Only test if we have software installed
            for software in result:
                assert 'DisplayName' in software
                assert 'DisplayVersion' in software
                assert 'Publisher' in software
                assert 'InstallDate' in software
                assert 'InstallLocation' in software
                assert 'UninstallString' in software


class TestSaveSoftwareListToFile:
    """Test cases for save_software_list_to_file function"""

    def test_save_software_list_success(self, tmp_path, monkeypatch):
        """Test successful file saving"""
        monkeypatch.setattr('services.installed_software_service.DATA_DIR', str(tmp_path))

        software_list = [
            {'DisplayName': 'Test Software', 'DisplayVersion': '1.0'},
            {'DisplayName': 'Another Software', 'DisplayVersion': '2.0'}
        ]

        result = save_software_list_to_file(software_list)

        assert result is not None
        assert 'software.json' in result  # Now saves as software.json (latest)

        # Verify file was created
        file_path = Path(result)
        assert file_path.exists()

        # Verify content
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            assert len(data) == 2
            assert data[0]['DisplayName'] == 'Test Software'

        # Verify dated version was also created
        reports_dir = file_path.parent
        dated_files = list(reports_dir.glob('software_*.json'))
        assert len(dated_files) >= 1  # Should have at least one dated file

    def test_save_software_list_empty(self, tmp_path, monkeypatch):
        """Test saving empty software list"""
        monkeypatch.setattr('services.installed_software_service.DATA_DIR', str(tmp_path))

        result = save_software_list_to_file([])

        assert result is None

    def test_save_software_list_custom_filename(self, tmp_path, monkeypatch):
        """Test saving with custom filename"""
        monkeypatch.setattr('services.installed_software_service.DATA_DIR', str(tmp_path))

        software_list = [{'DisplayName': 'Test Software'}]
        result = save_software_list_to_file(software_list, 'custom_software.json')

        assert result is not None
        assert 'custom_software.json' in result

        file_path = Path(result)
        assert file_path.exists()
        assert file_path.name == 'custom_software.json'
        # Should be in reports directory
        assert file_path.parent.name == 'reports'

    def test_save_software_list_directory_creation(self, tmp_path, monkeypatch):
        """Test that directory structure is created"""
        # Set DATA_DIR to a base directory
        monkeypatch.setattr('services.installed_software_service.DATA_DIR', str(tmp_path))

        software_list = [{'DisplayName': 'Test Software'}]
        result = save_software_list_to_file(software_list)

        assert result is not None

        # Verify directory structure was created (hostname/reports/)
        file_path = Path(result)
        assert file_path.parent.name == 'reports'  # reports directory
        assert file_path.parent.parent.name.startswith(tmp_path.name) or file_path.parent.parent.parent == tmp_path  # hostname directory


class TestCheckBlacklistedSoftware:
    """Test cases for check_blacklisted_software function"""

    def test_check_blacklisted_software_match(self):
        """Test finding blacklisted software"""
        software_list = [
            {'DisplayName': 'Apache Tomcat 9.0', 'DisplayVersion': '9.0.0'},
            {'DisplayName': 'Regular Software', 'DisplayVersion': '1.0'}
        ]

        cve_list = [
            {'product': 'Apache Tomcat', 'id': 'CVE-2021-1234'},
            {'product': 'Other Product', 'id': 'CVE-2021-5678'}
        ]

        result = check_blacklisted_software(software_list, cve_list)

        assert len(result) == 1
        assert result[0]['software']['DisplayName'] == 'Apache Tomcat 9.0'
        assert result[0]['cve']['id'] == 'CVE-2021-1234'

    def test_check_blacklisted_software_no_match(self):
        """Test when no blacklisted software is found"""
        software_list = [
            {'DisplayName': 'Regular Software', 'DisplayVersion': '1.0'}
        ]

        cve_list = [
            {'product': 'Apache Tomcat', 'id': 'CVE-2021-1234'}
        ]

        result = check_blacklisted_software(software_list, cve_list)

        assert result == []

    def test_check_blacklisted_software_empty_inputs(self):
        """Test with empty inputs"""
        result = check_blacklisted_software([], [])
        assert result == []

        result = check_blacklisted_software([{'DisplayName': 'Software'}], [])
        assert result == []

        result = check_blacklisted_software([], [{'product': 'Product'}])
        assert result == []


if __name__ == '__main__':
    pytest.main([__file__, '-v'])