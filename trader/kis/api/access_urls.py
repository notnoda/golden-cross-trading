from abc import abstractmethod

# ------------------------------------------------------------------------------
# - BaseUrls
# ------------------------------------------------------------------------------
class BaseUrls:

    @abstractmethod
    def get_api_url(self): pass

    @abstractmethod
    def get_ws_url(self): pass
# end of class BaseUrls

# ------------------------------------------------------------------------------
# - KisRealUrls
# - 실전 도메인 정보
# ------------------------------------------------------------------------------
class KisRealUrls(BaseUrls):
    def get_api_url(self): return "https://openapi.koreainvestment.com:9443"
    def get_ws_url(self): return "ws://ops.koreainvestment.com:21000"
# end of class KisRealUrls

# ------------------------------------------------------------------------------
# - KisMockUrls
# - 모의 도메인 정보
# ------------------------------------------------------------------------------
class KisMockUrls(BaseUrls):
    def get_api_url(self): return "https://openapivts.koreainvestment.com:29443"
    def get_ws_url(self): return "ws://ops.koreainvestment.com:31000"
# end of class KisMockUrls

################################################################################
# URL 정보를 반환 한다.
################################################################################
def get_urls(mode):
    return KisRealUrls() if mode == "real" else KisMockUrls()
