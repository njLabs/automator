from py5paisa import FivePaisaClient


class Paisa5Client:
    def __init__(self, creds: dict, client_creds: dict):
        self.client = FivePaisaClient(**client_creds, cred=creds)

    def login_(self):
        self.client.login()
        data = self.client.historical_data('N', 'C', 1660, '15m', '2023-02-02', '2023-02-27')
        print(data)


def paisa_5_client(client_creds, creds):
    client = FivePaisaClient(**client_creds, cred=creds)
    client.login()
    return client


cred = {
    "APP_NAME": "5P52119099",
    "APP_SOURCE": "5357",
    "USER_ID": "7gquHuCFNFV",
    "PASSWORD": "FiwCx2E6RNN",
    "USER_KEY": "zlZrwaeOpuVHEjAjAKyUoGraOg1xfKVw",
    "ENCRYPTION_KEY": "P4RCNE2Xu24Aa1O7mvvaqS3aky1EaKo7"
}
client_credentials = {
    "email": "mann_1730@yahoo.com",
    "passwd": "Bhola@2025",
    "dob": "19840101"
}

# client = Paisa5Client(creds=cred, client_creds=client_credentials)
client = paisa_5_client(creds=cred, client_creds=client_credentials)