import trader.utils.logging_utils as logger

from trader.kis.api.access_config import AccessConfig

################################################################################
# 테스트 환경 정보
################################################################################
def get_test_config(is_real: bool):
    config = get_real_data() if is_real else get_mock_data()
    config["product_no"]   = "01"
    config["stock_long"]   = "SOXL"
    config["stock_short"]  = "SOXS"
    config["socket_long"]  = "RAMSSOXL"
    config["socket_short"] = "RAMSSOXS"
    config["tick_macd"]    = "466"
    config["tick_long"]    = "68"
    config["tick_short"]   = "34"
    config["exchange"]     = "AMEX"
    config["order_qty"]    = "1"

    AccessConfig(config)
    logger.console_logger(config["log_path"])
    return config

################################################################################
# 실전 테스트 정보
################################################################################
def get_real_data():
    return {
        "mode"      : "real",
        "app_key"   : "PSWMSkis4i7AuuVORXJEy3lBz1K3M9WPO9kQ",
        "app_secret": "GU3mRHLNCprNtX3pzPVMXI9FKs+/jh84jbaYLQddVIMeJPm1Kc9cIaxEu+C7Q6dLxHGYxLYwroyOujv/BOng5KJKmnRAIRsDyCgzRlspKAcwqS4h+htbE/CYnzuMnPLd+M0nwv+/LnD+dkD6vD0wbKDyAspvhtI8yFfhUNH81KDzK8VE+nk=",
        "token_path": "C:/project-workspace/PythonProject/_resources/config/token_real.yaml",
        "log_path"  : "C:/project-workspace/PythonProject/_resources/logs/solx",
        "account_no": "64859119",
    }

################################################################################
# 모의 테스트 정보
################################################################################
def get_mock_data():
    return {
        "mode"      : "mock",
        "app_key"   : "PSSLqkONtQdnoFs0QPCBYo6LyE0bMagd6MBX",
        "app_secret": "3yS0p3PGbKatUAiCjHXDAjpKkIO7K7nx+01DY6bD4wwX60jK1vsAmR9LIbcmNNvTx0TN+i/qLKPvqT1beJaor8McrPm9oJvKQetaT8nB0Nv7dz6sYCWK9NU7oDqwfKLUekqhhRyVPTawqD/Ik/fU8w/y3d/u1B4G813dsi2dkBs7kSkH1VA=",
        "token_path": "C:/project-workspace/PythonProject/_resources/config/token_mock.yaml",
        "log_path"  : "C:/project-workspace/PythonProject/_resources/logs/solx-mock",
        "account_no": "50124841",
    }