class DoubleBollingerBandsStrategyRequest:

  @property
  def sma_period(self) -> int: return self._sma_period

  @sma_period.setter
  def sma_period(self, val: int) -> None: self._sma_period = val

  @property
  def std_distance(self) -> float: return self._std_distance

  @std_distance.setter
  def std_distance(self, val: float) -> None: self._std_distance = val
