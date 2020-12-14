class AbzStrategyRequest:

  @property
  def abz_er_period(self) -> int: return self._abz_er_period

  @abz_er_period.setter
  def abz_er_period(self, val: int) -> None: self._abz_er_period = val

  @property
  def abz_std_distance(self) -> float: return self._abz_std_distance

  @abz_std_distance.setter
  def abz_std_distance(self, val: float) -> None: self._abz_std_distance = val

  @property
  def abz_constant_k(self) -> float: return self._abz_constant_k

  @abz_constant_k.setter
  def abz_constant_k(self, val: float) -> None: self._abz_constant_k = val
