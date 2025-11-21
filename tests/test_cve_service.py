"""
Unit tests for cve_service module.
Tests CVE fetching and searching functionality with mocked API calls.
"""
import pytest
from unittest.mock import patch, MagicMock
import json
import requests
from requests.exceptions import Timeout, RequestException
from services.cve_service import get_cve_by_id, get_cve_list, search_cves_by_vendor


class TestGetCveById:
    """Test cases for get_cve_by_id function"""
    
    @patch('services.cve_service.requests.get')
    def test_get_cve_success(self, mock_get):
        """Test successful CVE fetch"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': 'CVE-2021-44228',
            'summary': 'Apache Log4j2 2.0-beta9 through 2.15.0 JNDI features...',
            'cvss': 10.0
        }
        mock_get.return_value = mock_response
        
        result = get_cve_by_id('CVE-2021-44228')
        
        assert result is not None
        assert result['id'] == 'CVE-2021-44228'
        assert 'summary' in result
        mock_get.assert_called_once_with(
            'https://cve.circl.lu/api/cve/CVE-2021-44228',
            timeout=10
        )
    
    def test_get_cve_invalid_format(self):
        """Test with invalid CVE ID format"""
        with pytest.raises(ValueError, match="Invalid CVE ID format"):
            get_cve_by_id('INVALID-FORMAT')
        
        with pytest.raises(ValueError):
            get_cve_by_id('CVE-ABC-123')
        
        with pytest.raises(ValueError):
            get_cve_by_id('2021-44228')
    
    def test_get_cve_valid_formats(self):
        """Test various valid CVE ID formats"""
        valid_ids = [
            'CVE-2021-44228',
            'CVE-2020-0001',
            'CVE-1999-0001',
            'CVE-2023-12345678'  # CVE with more than 4 digits after year
        ]
        
        with patch('services.cve_service.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {'id': 'test'}
            mock_get.return_value = mock_response
            
            for cve_id in valid_ids:
                result = get_cve_by_id(cve_id)
                assert result is not None
    
    @patch('services.cve_service.requests.get')
    def test_get_cve_not_found(self, mock_get):
        """Test CVE not found (404)"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        result = get_cve_by_id('CVE-2099-99999')
        
        assert result is None
    
    @patch('services.cve_service.requests.get')
    def test_get_cve_server_error(self, mock_get):
        """Test server error response"""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response
        
        result = get_cve_by_id('CVE-2021-44228')
        
        assert result is None
    
    @patch('services.cve_service.requests.get')
    def test_get_cve_timeout(self, mock_get):
        """Test timeout handling"""
        mock_get.side_effect = Timeout("Connection timeout")
        
        result = get_cve_by_id('CVE-2021-44228')
        
        assert result is None
    
    @patch('services.cve_service.requests.get')
    def test_get_cve_json_decode_error(self, mock_get):
        """Test invalid JSON response"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_get.return_value = mock_response
        
        result = get_cve_by_id('CVE-2021-44228')
        
        assert result is None
    
    @patch('services.cve_service.requests.get')
    def test_get_cve_network_error(self, mock_get):
        """Test network error handling"""
        mock_get.side_effect = RequestException("Network error")
        
        result = get_cve_by_id('CVE-2021-44228')
        
        assert result is None
    
    @patch('services.cve_service.requests.get')
    def test_get_cve_custom_timeout(self, mock_get):
        """Test with custom timeout parameter"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'id': 'CVE-2021-44228'}
        mock_get.return_value = mock_response
        
        result = get_cve_by_id('CVE-2021-44228', timeout=30)
        
        assert result is not None
        mock_get.assert_called_once_with(
            'https://cve.circl.lu/api/cve/CVE-2021-44228',
            timeout=30
        )


class TestGetCveList:
    """Test cases for get_cve_list function"""
    
    @patch('services.cve_service.get_cve_by_id')
    def test_get_cve_list_all_success(self, mock_get_cve):
        """Test fetching multiple CVEs successfully"""
        mock_get_cve.side_effect = [
            {'id': 'CVE-2021-44228', 'summary': 'Log4j'},
            {'id': 'CVE-2021-45046', 'summary': 'Log4j 2'},
            {'id': 'CVE-2021-45105', 'summary': 'Log4j 3'}
        ]
        
        cve_ids = ['CVE-2021-44228', 'CVE-2021-45046', 'CVE-2021-45105']
        result = get_cve_list(cve_ids)
        
        assert len(result) == 3
        assert result[0]['id'] == 'CVE-2021-44228'
        assert mock_get_cve.call_count == 3
    
    @patch('services.cve_service.get_cve_by_id')
    def test_get_cve_list_partial_success(self, mock_get_cve):
        """Test with some CVEs failing"""
        mock_get_cve.side_effect = [
            {'id': 'CVE-2021-44228', 'summary': 'Log4j'},
            None,  # This one fails
            {'id': 'CVE-2021-45105', 'summary': 'Log4j 3'}
        ]
        
        cve_ids = ['CVE-2021-44228', 'CVE-2099-99999', 'CVE-2021-45105']
        result = get_cve_list(cve_ids)
        
        assert len(result) == 2
        assert result[0]['id'] == 'CVE-2021-44228'
        assert result[1]['id'] == 'CVE-2021-45105'
    
    @patch('services.cve_service.get_cve_by_id')
    def test_get_cve_list_empty_input(self, mock_get_cve):
        """Test with empty CVE list"""
        result = get_cve_list([])
        
        assert result == []
        mock_get_cve.assert_not_called()
    
    @patch('services.cve_service.get_cve_by_id')
    def test_get_cve_list_invalid_id_skipped(self, mock_get_cve):
        """Test that invalid CVE IDs are skipped"""
        mock_get_cve.side_effect = [
            ValueError("Invalid format"),
            {'id': 'CVE-2021-45046', 'summary': 'Valid CVE'}
        ]
        
        cve_ids = ['INVALID', 'CVE-2021-45046']
        result = get_cve_list(cve_ids)
        
        assert len(result) == 1
        assert result[0]['id'] == 'CVE-2021-45046'
    
    @patch('services.cve_service.get_cve_by_id')
    def test_get_cve_list_custom_timeout(self, mock_get_cve):
        """Test custom timeout is passed to get_cve_by_id"""
        mock_get_cve.return_value = {'id': 'CVE-2021-44228'}
        
        result = get_cve_list(['CVE-2021-44228'], timeout=20)
        
        mock_get_cve.assert_called_once_with('CVE-2021-44228', timeout=20)


class TestSearchCvesByVendor:
    """Test cases for search_cves_by_vendor function"""
    
    @patch('services.cve_service.requests.get')
    def test_search_vendor_success(self, mock_get):
        """Test successful vendor search"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {'id': 'CVE-2021-0001', 'summary': 'Apache vulnerability 1'},
            {'id': 'CVE-2021-0002', 'summary': 'Apache vulnerability 2'},
            {'id': 'CVE-2021-0003', 'summary': 'Apache vulnerability 3'}
        ]
        mock_get.return_value = mock_response
        
        result = search_cves_by_vendor('apache')
        
        assert len(result) == 3
        assert result[0]['id'] == 'CVE-2021-0001'
        mock_get.assert_called_once_with(
            'https://cve.circl.lu/api/search/apache',
            timeout=10
        )
    
    @patch('services.cve_service.requests.get')
    def test_search_vendor_max_results(self, mock_get):
        """Test max_results parameter"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        # Return 100 results
        mock_response.json.return_value = [
            {'id': f'CVE-2021-{i:04d}', 'summary': f'Vuln {i}'}
            for i in range(100)
        ]
        mock_get.return_value = mock_response
        
        result = search_cves_by_vendor('apache', max_results=5)
        
        # Should only return 5 results
        assert len(result) == 5
        assert result[0]['id'] == 'CVE-2021-0000'
        assert result[4]['id'] == 'CVE-2021-0004'
    
    @patch('services.cve_service.requests.get')
    def test_search_vendor_no_results(self, mock_get):
        """Test vendor with no CVEs"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response
        
        result = search_cves_by_vendor('nonexistent-vendor')
        
        assert result == []
    
    @patch('services.cve_service.requests.get')
    def test_search_vendor_error_response(self, mock_get):
        """Test error response from API"""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response
        
        result = search_cves_by_vendor('apache')
        
        assert result == []
    
    @patch('services.cve_service.requests.get')
    def test_search_vendor_timeout(self, mock_get):
        """Test timeout during search"""
        mock_get.side_effect = Timeout("Connection timeout")
        
        result = search_cves_by_vendor('apache')
        
        assert result == []
    
    @patch('services.cve_service.requests.get')
    def test_search_vendor_json_error(self, mock_get):
        """Test invalid JSON response"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_get.return_value = mock_response
        
        result = search_cves_by_vendor('apache')
        
        assert result == []
    
    @patch('services.cve_service.requests.get')
    def test_search_vendor_network_error(self, mock_get):
        """Test network error during search"""
        mock_get.side_effect = RequestException("Network error")
        
        result = search_cves_by_vendor('apache')
        
        assert result == []
    
    @patch('services.cve_service.requests.get')
    def test_search_vendor_custom_timeout(self, mock_get):
        """Test custom timeout parameter"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response
        
        result = search_cves_by_vendor('apache', timeout=30)
        
        mock_get.assert_called_once_with(
            'https://cve.circl.lu/api/search/apache',
            timeout=30
        )
    
    @patch('services.cve_service.requests.get')
    def test_search_vendor_non_list_response(self, mock_get):
        """Test when API returns non-list response"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'error': 'Invalid request'}
        mock_get.return_value = mock_response
        
        result = search_cves_by_vendor('apache')
        
        # Should handle gracefully and return empty list
        assert result == []


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
