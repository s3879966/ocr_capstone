import configparser
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient


def client():
    config = configparser.ConfigParser()

    config.read('client.ini')
    key = config.get('Capstoner_AutoGrader', 'key')
    endpoint = config.get('Capstoner_AutoGrader', 'endpoint')
    client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    return client


if __name__ == "__main__":
    client = client()
