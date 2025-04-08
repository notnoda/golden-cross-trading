from collections import namedtuple
from datetime import datetime, timedelta

################################################################################
# Json Data 를 Object 로 변환 한다.
################################################################################
def get_json_to_object(json_data):
    _tc_ = namedtuple('res', json_data.keys())
    return _tc_(**json_data)
