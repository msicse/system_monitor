"""
Unit tests for screenshot_service module.
Tests screenshot capture functionality with mocked dependencies.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock, call
from pathlib import Path
import os
from services.screenshot_service import take_screenshot


class TestTakeScreenshot:
    """Test cases for take_screenshot function"""
    
    def test_single_monitor_success(self, tmp_path, monkeypatch):
        """Test successful screenshot capture with one monitor"""
        # Set up temporary directory for screenshots
        monkeypatch.setattr('services.screenshot_service.SCREENSHOT_DIR', str(tmp_path))
        
        # Mock mss
        with patch('services.screenshot_service.mss.mss') as mock_mss:
            # Setup mock screenshot tool
            mock_sct = MagicMock()
            mock_monitor = {'left': 0, 'top': 0, 'width': 1920, 'height': 1080}
            mock_sct.monitors = [None, mock_monitor]  # First element is all monitors combined
            
            # Mock screenshot object
            mock_screenshot = MagicMock()
            mock_screenshot.rgb = b'fake_image_data'
            mock_screenshot.size = (1920, 1080)
            mock_sct.grab.return_value = mock_screenshot
            
            mock_mss.return_value.__enter__.return_value = mock_sct
            
            # Mock the PNG save function
            with patch('services.screenshot_service.mss.tools.to_png') as mock_to_png:
                result = take_screenshot()
                
                # Assertions
                assert len(result) == 1
                assert result[0].endswith('.png')
                assert 'screenshot_' in result[0]
                
                # Verify grab was called with the monitor
                mock_sct.grab.assert_called_once_with(mock_monitor)
                
                # Verify to_png was called
                assert mock_to_png.call_count == 1
    
    def test_multiple_monitors_success(self, tmp_path, monkeypatch):
        """Test successful screenshot capture with multiple monitors"""
        monkeypatch.setattr('services.screenshot_service.SCREENSHOT_DIR', str(tmp_path))
        
        with patch('services.screenshot_service.mss.mss') as mock_mss:
            mock_sct = MagicMock()
            # Simulate 3 monitors
            mock_monitors = [
                None,  # Combined
                {'left': 0, 'top': 0, 'width': 1920, 'height': 1080},
                {'left': 1920, 'top': 0, 'width': 1920, 'height': 1080},
                {'left': 3840, 'top': 0, 'width': 1920, 'height': 1080}
            ]
            mock_sct.monitors = mock_monitors
            
            mock_screenshot = MagicMock()
            mock_screenshot.rgb = b'fake_data'
            mock_screenshot.size = (1920, 1080)
            mock_sct.grab.return_value = mock_screenshot
            
            mock_mss.return_value.__enter__.return_value = mock_sct
            
            with patch('services.screenshot_service.mss.tools.to_png'):
                result = take_screenshot()
                
                # Should capture 3 screenshots
                assert len(result) == 3
                
                # Verify all have proper naming
                for i, path in enumerate(result, start=1):
                    assert f'_{i}.png' in path
    
    def test_no_monitors_detected(self, tmp_path, monkeypatch):
        """Test behavior when no monitors are detected"""
        monkeypatch.setattr('services.screenshot_service.SCREENSHOT_DIR', str(tmp_path))
        
        with patch('services.screenshot_service.mss.mss') as mock_mss:
            mock_sct = MagicMock()
            mock_sct.monitors = [None]  # Only combined monitor, no real monitors
            mock_mss.return_value.__enter__.return_value = mock_sct
            
            result = take_screenshot()
            
            # Should return empty list
            assert result == []
    
    def test_exception_during_screenshot(self, tmp_path, monkeypatch):
        """Test exception handling during screenshot capture"""
        monkeypatch.setattr('services.screenshot_service.SCREENSHOT_DIR', str(tmp_path))
        
        with patch('services.screenshot_service.mss.mss', side_effect=Exception("MSS initialization failed")):
            result = take_screenshot()
            
            # Should return empty list on error
            assert result == []
    
    def test_directory_creation(self, tmp_path, monkeypatch):
        """Test that directory structure is created correctly"""
        monkeypatch.setattr('services.screenshot_service.SCREENSHOT_DIR', str(tmp_path))
        
        with patch('services.screenshot_service.mss.mss') as mock_mss:
            mock_sct = MagicMock()
            mock_monitor = {'left': 0, 'top': 0, 'width': 1920, 'height': 1080}
            mock_sct.monitors = [None, mock_monitor]
            
            mock_screenshot = MagicMock()
            mock_screenshot.rgb = b'data'
            mock_screenshot.size = (1920, 1080)
            mock_sct.grab.return_value = mock_screenshot
            
            mock_mss.return_value.__enter__.return_value = mock_sct
            
            with patch('services.screenshot_service.mss.tools.to_png'):
                result = take_screenshot()
                
                # Verify directory structure exists
                # Should have created: <tmp_path>/<hostname>/<YYYYMMDD>/
                created_dirs = list(tmp_path.rglob('*'))
                assert len(created_dirs) >= 2  # hostname dir and date dir
    
    def test_hostname_in_path(self, tmp_path, monkeypatch):
        """Test that hostname is included in the file path"""
        monkeypatch.setattr('services.screenshot_service.SCREENSHOT_DIR', str(tmp_path))
        
        with patch('services.screenshot_service.mss.mss') as mock_mss:
            mock_sct = MagicMock()
            mock_monitor = {'left': 0, 'top': 0, 'width': 1920, 'height': 1080}
            mock_sct.monitors = [None, mock_monitor]
            
            mock_screenshot = MagicMock()
            mock_screenshot.rgb = b'data'
            mock_screenshot.size = (1920, 1080)
            mock_sct.grab.return_value = mock_screenshot
            
            mock_mss.return_value.__enter__.return_value = mock_sct
            
            with patch('services.screenshot_service.mss.tools.to_png'):
                with patch('utils.paths_utils.socket.gethostname', return_value='TEST-PC'):
                    result = take_screenshot()
                    
                    # Verify hostname is in path
                    assert len(result) == 1
                    assert 'TEST-PC' in result[0]
    
    def test_timestamp_format_in_filename(self, tmp_path, monkeypatch):
        """Test that timestamp is correctly formatted in filename"""
        monkeypatch.setattr('services.screenshot_service.SCREENSHOT_DIR', str(tmp_path))
        
        with patch('services.screenshot_service.mss.mss') as mock_mss:
            mock_sct = MagicMock()
            mock_monitor = {'left': 0, 'top': 0, 'width': 1920, 'height': 1080}
            mock_sct.monitors = [None, mock_monitor]
            
            mock_screenshot = MagicMock()
            mock_screenshot.rgb = b'data'
            mock_screenshot.size = (1920, 1080)
            mock_sct.grab.return_value = mock_screenshot
            
            mock_mss.return_value.__enter__.return_value = mock_sct
            
            with patch('services.screenshot_service.mss.tools.to_png'):
                result = take_screenshot()
                
                # Verify filename contains timestamp pattern YYYYMMDD_HHMMSS
                filename = os.path.basename(result[0])
                assert filename.startswith('screenshot_')
                # Format: screenshot_YYYYMMDD_HHMMSS_1.png
                parts = filename.split('_')
                assert len(parts) >= 3
                assert parts[1].isdigit() and len(parts[1]) == 8  # Date part YYYYMMDD


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
