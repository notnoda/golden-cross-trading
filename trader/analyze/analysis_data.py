# -----------------------------------------------------------------------------
# AnalysisData 객체 생성
# 분석 정보를 저정 한다.
# -----------------------------------------------------------------------------
class AnalysisData:

    def __init__(self,
                 open_val: float, high_val: float, low_val: float, close_val: float,
                 macd_val: float = 0, macd_signal: float = 0, macd_histo: float = 0,
                 rsi_long: float = 0, rsi_short: float = 0,
                 psar_long: float = 0, psar_short: float = 0):

        # 주식 시세 정보
        self.open_val = open_val
        self.high_val = high_val
        self.low_val = low_val
        self.close_val = close_val

        # MACD 정보
        self.macd_val = macd_val
        self.macd_signal = macd_signal
        self.macd_histo = macd_histo
        self.macd_diff = macd_diff

        # RSI 정보
        self.rsi_long = rsi_long
        self.rsi_short = rsi_short

        # PSAR 정보
        self.psar_long = psar_long
        self.psar_short = psar_short


    def close_val(self): return self.close_val
    def macd_val(self): return self.macd_val
    def macd_signal(self): return self.macd_signal
    def macd_histogram(self): return self.macd_histogram

    def macd(self): return self.macd_val - self.macd_signal
    def rsi(self): return self.rsi_short - self.rsi_long
    def sar(self): return self.psar_long - self.psar_short

    def is_rsi_over(self, line): return self.rsi_long > line and self.rsi_short > line
    def is_rsi_under(self, line): return self.rsi_long < line and self.rsi_short < line

    def to_str(self) -> str:
        return f"[{self.macd_val}] [{self.macd_signal}] [{self.rsi_long}] [{self.rsi_short}] [{self.psar_long}] [{self.psar_short}]"

# end of class AnalysisData
