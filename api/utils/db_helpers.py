from django.db import connection

def get_table_list():
    """Obtém todas as tabelas disponíveis que começam com 'controle_'."""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT tablename 
            FROM pg_tables 
            WHERE schemaname = 'public' AND tablename LIKE 'controle_%'
        """)
        return [row[0] for row in cursor.fetchall()]