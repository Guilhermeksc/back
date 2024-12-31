import logging

logger = logging.getLogger(__name__)

def parse_decimal(value):
    """Converte valores no formato brasileiro para o formato do PostgreSQL."""
    if value:
        try:
            return float(value.replace('.', '').replace(',', '.'))
        except ValueError:
            logger.warning("Erro ao converter valor: %s", value)
    return None