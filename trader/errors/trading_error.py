# ------------------------------------------------------------------------------
# - TradingError
# ------------------------------------------------------------------------------
class TradingError(Exception):
    def __init__(self, message):
        super().__init__(message)
# end of class TradingError

# ------------------------------------------------------------------------------
# - TradingOrderBuyError
# ------------------------------------------------------------------------------
class TradingOrderBuyError(Exception):
    def __init__(self, message):
        super().__init__(message)
# end of class TradingOrderBuyError

# ------------------------------------------------------------------------------
# - TradingOrderSellError
# ------------------------------------------------------------------------------
class TradingOrderSellError(Exception):
    def __init__(self, message):
        super().__init__(message)
# end of class TradingOrderSellError

# ------------------------------------------------------------------------------
# - TradingOrderCloseError
# ------------------------------------------------------------------------------
class TradingOrderCloseError(Exception):
    def __init__(self):
        super().__init__("매매 시간이 지났습니다.")
# end of class TradingOrderCloseError
