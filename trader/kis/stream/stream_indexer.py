from abc import abstractmethod

# -----------------------------------------------------------------------------
# - BaseStreamIndexer
# -----------------------------------------------------------------------------
class BaseStreamIndexer:

    @abstractmethod
    def get_tr_id(self) -> str: pass

    @abstractmethod
    def get_length(self) -> int: pass

    @abstractmethod
    def get_time(self) -> int: pass

    @abstractmethod
    def get_price(self) -> int: pass
# end of class BaseStreamIndexer

# -----------------------------------------------------------------------------
# - OverseasPriceIndexer
# - 해외 주식 실시간 지연 체결가[실시간-007]
# -----------------------------------------------------------------------------
class OverseasPriceIndexer(BaseStreamIndexer):
    def get_tr_id(self) -> str: return "HDFSCNT0"
    def get_length(self) -> int: return 26
    def get_time(self) -> int: return 5
    def get_price(self) -> int: return 11
# end of class OverseasPriceIndexer

# -----------------------------------------------------------------------------
# - DomesticPriceIndexer
# - 국내 주식 실시간 체결가 (KRX) [실시간-003]
# -----------------------------------------------------------------------------
class DomesticPriceIndexer(BaseStreamIndexer):
    def get_tr_id(self) -> str: return "H0STCNT0"
    def get_length(self) -> int: return 46
    def get_time(self) -> int: return 1
    def get_price(self) -> int: return 2
# end of class DomesticPriceIndexer

################################################################################
# Stream Indexer 를 생성 한다.
################################################################################
def get_stream_indexer(tr_id: str):
    if tr_id == "HDFSCNT0": return OverseasPriceIndexer()
    elif tr_id == "H0STCNT0": return DomesticPriceIndexer()
    else: return OverseasPriceIndexer()
