class SmaCrossoverStrategyRequest:

  @property
  def sma_period_fast(self) -> int: return self._sma_period_fast

  @sma_period_fast.setter
  def sma_period_fast(self, val: int) -> None: self._sma_period_fast = val

  @property
  def sma_period_slow(self) -> int: return self._sma_period_slow

  @sma_period_slow.setter
  def sma_period_slow(self, val: int) -> None: self._sma_period_slow = val
