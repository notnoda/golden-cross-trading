from trader.base.base_thread import BaseThread
from trader.kis.strategy1.default_dual_strategy import DefaultDualStrategy
from trader.kis.strategy1.volatility_crossover_strategy import VolatilityCrossoverStrategy

# -----------------------------------------------------------------------------
# BaseRunner
# -----------------------------------------------------------------------------
class BaseRunner(BaseThread):

    def __init__(self, volatility_strategy: VolatilityCrossoverStrategy, default_strategy: DefaultDualStrategy):
        super().__init__()
        self.volatility_strategy: VolatilityCrossoverStrategy = volatility_strategy
        self.default_strategy: DefaultDualStrategy = default_strategy

    def execute(self):
        self.volatility_strategy.execute()
        self.default_strategy.execute()

# end of class BaseRunner
