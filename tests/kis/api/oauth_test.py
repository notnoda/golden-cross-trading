import trader.kis.api.oauth as oauth
import tests.const.test_data_values as conf

if __name__ == "__main__":
    is_real: bool = True # 실전: True, 모의: False
    config = conf.get_test_config(is_real)

    approval_key = oauth.get_approval_key()
    print(approval_key)
