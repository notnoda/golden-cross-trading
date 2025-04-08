
from trader.kis.api.access_config import AccessConfig

def create_config():
    config = {
        "mode": "mock",
        "app_key": "PSSLqkONtQdnoFs0QPCBYo6LyE0bMagd6MBX",
        "app_secret": "3yS0p3PGbKatUAiCjHXDAjpKkIO7K7nx+01DY6bD4wwX60jK1vsAmR9LIbcmNNvTx0TN+i/qLKPvqT1beJaor8McrPm9oJvKQetaT8nB0Nv7dz6sYCWK9NU7oDqwfKLUekqhhRyVPTawqD/Ik/fU8w/y3d/u1B4G813dsi2dkBs7kSkH1VA=",
        "account_no": "50124841",
        "product_no": "01",
        "token_path": "C:/Projects/PythonProject/_resources/config/token_info.yaml"
    }

    config1 = AccessConfig(config)
    config2 = AccessConfig(config)
    print(config1.access_token())
    print(AccessConfig().access_token())

if __name__ == "__main__":
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    create_config()
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
