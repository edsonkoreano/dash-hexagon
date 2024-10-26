import pyodbc
import pandas as pd
from datetime import datetime
import logging

class interface_db:
    """
    Classe para iteragir com qualquer tipo de banco de dados. 
    Atenção na string de conexão que pode variar caso a caso
    """
    
    def __init__(self, server: str, database: str, username: str, password: str):
        """
        Initialize the database connector with connection parameters.
        
        Args:
            server (str): The server name
            database (str): The database name
            username (str): The username
            password (str): The password
        """
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.conn = None
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
    def _build_connection_string(self) -> str:
        """
        Cria a string para conectar com banco de dados.
        A depender do banco essa estrutura precisa ser mudada
        
        Returns:
            str: string de conexão
        """
        return (
            "Driver={ODBC Driver 18 for SQL Server};"
            f"Server=tcp:{self.server},1433;"
            f"Database={self.database};"
            f"Uid={self.username};"
            f"Pwd={self.password};"
            "Encrypt=yes;"
            "TrustServerCertificate=no;"
            "Connection Timeout=30;"
        )
    
    def connect(self) -> None:
        """
        Conecta com a db
        """
        try:
            if not self.conn or self.conn.closed:
                self.conn = pyodbc.connect(self._build_connection_string())
                self.logger.info("Conexao feita com o sucesso")
        except pyodbc.Error as e:
            self.logger.error(f"Erro de conexao: {str(e)}")
            raise
    
    def disconnect(self) -> None:
        """
        Fecha conexão se existir.
        """
        if self.conn and not self.conn.closed:
            self.conn.close()
            self.logger.info("conexao fechada")
    
    def execute_query(self, query: str) -> pd.DataFrame:
        """
        Executa uma  query SQL e retorna resultado como pandas DataFrame.
        
        Args:
            query (str): Comando SQL a ser executado           
        Returns:
            pd.DataFrame: Resultado como DF
        """
        try:
            self.connect()
            df = pd.read_sql_query(query, self.conn)

            self.logger.info(f"Query executed successfully: {query[:100]}...")
            return df
        except Exception as e:
            self.logger.error(f"Error executing query: {str(e)}")
            raise
        finally:
            self.disconnect()
    
