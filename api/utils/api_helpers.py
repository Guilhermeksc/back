import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging

logger = logging.getLogger(__name__)

def get_api_data(url):
    """Busca dados da API com retry."""
    session = requests.Session()
    retry = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)

    logger.info(f"Consultando a API: {url}")
    response = session.get(url, headers={"accept": "application/json"}, timeout=10, verify=False)
    response.raise_for_status()
    return response.json()
