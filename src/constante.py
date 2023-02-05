from pathlib import Path
import os


class Constante:
    """Constantes com o nome das consultas sql utilizadas no codigo"""
    DIRETORIO = Path(__file__).parent.parent
    DIRETORIO_DATA = os.path.join(DIRETORIO, 'data')
    DIRETORIO_DATA_RAW = os.path.join(DIRETORIO, 'data/raw')
    DIRETORIO_DATA_PROCESSID = os.path.join(DIRETORIO, 'data/processed')
    DIRETORIO_DATA_FINAL = os.path.join(DIRETORIO, 'data/final')
    URL = 'http://portalweb.cooxupe.com.br:8080/portal/precohistoricocafe.jsp'