import requests
import json
import logging
from typing import List, Dict, Optional
import re
from requests.exceptions import RequestException, Timeout

from config.settings import CVE_API_BASE_URL, CVE_REQUEST_TIMEOUT, CVE_MAX_RESULTS

logger = logging.getLogger(__name__)

# CVE ID validation pattern
CVE_PATTERN = re.compile(r'^CVE-\d{4}-\d{4,}$')


def get_cve_by_id(cve_id: str, timeout: int = CVE_REQUEST_TIMEOUT) -> Optional[Dict]:
    """
    Fetch CVE details by CVE ID from CVE API.
    
    Args:
        cve_id: CVE identifier (e.g., 'CVE-2021-44228')
        timeout: Request timeout in seconds (default: from settings)
    
    Returns:
        Dict containing CVE details, or None if not found/error
    
    Raises:
        ValueError: If CVE ID format is invalid
    
    Example:
        >>> cve = get_cve_by_id('CVE-2021-44228')
        >>> print(cve['summary'])
    """
    # Validate CVE ID format
    if not CVE_PATTERN.match(cve_id):
        raise ValueError(f"Invalid CVE ID format: {cve_id}. Expected format: CVE-YYYY-NNNNN")
    
    url = f"{CVE_API_BASE_URL}/cve/{cve_id}"
    logger.info(f"Fetching CVE data for {cve_id} from {url}")
    
    try:
        response = requests.get(url, timeout=timeout)
        
        if response.status_code == 200:
            cve_data = response.json()
            logger.info(f"Successfully fetched CVE {cve_id}")
            return cve_data
        elif response.status_code == 404:
            logger.warning(f"CVE not found: {cve_id}")
            return None
        else:
            logger.error(f"Error fetching CVE {cve_id}: HTTP {response.status_code}")
            return None
            
    except Timeout:
        logger.error(f"Timeout fetching CVE {cve_id} after {timeout}s")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON response for CVE {cve_id}: {e}")
        return None
    except RequestException as e:
        logger.error(f"Network error fetching CVE {cve_id}: {e}")
        return None


def get_cve_list(cve_ids: List[str], timeout: int = CVE_REQUEST_TIMEOUT) -> List[Dict]:
    """
    Fetch multiple CVEs by their IDs.
    
    Args:
        cve_ids: List of CVE identifiers
        timeout: Request timeout in seconds per CVE (default: from settings)
    
    Returns:
        List of CVE data dictionaries (excludes failed fetches)
    
    Example:
        >>> cves = get_cve_list(['CVE-2021-44228', 'CVE-2021-45046'])
        >>> print(f"Fetched {len(cves)} CVEs")
    """
    cve_list = []
    
    for cve_id in cve_ids:
        try:
            cve_data = get_cve_by_id(cve_id, timeout=timeout)
            if cve_data:
                cve_list.append(cve_data)
        except ValueError as e:
            logger.warning(f"Skipping invalid CVE ID: {e}")
            continue
    
    logger.info(f"Successfully fetched {len(cve_list)}/{len(cve_ids)} CVEs")
    return cve_list


def search_cves_by_vendor(vendor: str, max_results: int = CVE_MAX_RESULTS, timeout: int = CVE_REQUEST_TIMEOUT) -> List[Dict]:
    """
    Search for CVEs by vendor name.
    
    Args:
        vendor: Vendor/product name (e.g., 'apache', 'microsoft')
        max_results: Maximum number of results to return (default: from settings)
        timeout: Request timeout in seconds (default: from settings)
    
    Returns:
        List of CVE data dictionaries
    
    Example:
        >>> cves = search_cves_by_vendor('apache', max_results=5)
    """
    url = f"{CVE_API_BASE_URL}/search/{vendor}"
    logger.info(f"Searching CVEs for vendor: {vendor} at {url}")
    
    try:
        response = requests.get(url, timeout=timeout)
        
        if response.status_code == 200:
            results = response.json()
            # Limit results
            limited_results = results[:max_results] if isinstance(results, list) else []
            logger.info(f"Found {len(limited_results)} CVEs for {vendor}")
            return limited_results
        else:
            logger.error(f"Error searching CVEs for {vendor}: HTTP {response.status_code}")
            return []
            
    except Timeout:
        logger.error(f"Timeout searching CVEs for {vendor} after {timeout}s")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON response searching for {vendor}: {e}")
        return []
    except RequestException as e:
        logger.error(f"Network error searching CVEs for {vendor}: {e}")
        return []