class DoubleTopsStrategyRequest:

  @property
  def exponential_smoothing_alpha(self) -> float: return self._exponential_smoothing_alpha

  @exponential_smoothing_alpha.setter
  def exponential_smoothing_alpha(self, val: float) -> None: self._exponential_smoothing_alpha = val

  @property
  def exponential_smoothing_max_min_diff(self) -> float: return self._exponential_smoothing_max_min_diff

  @exponential_smoothing_max_min_diff.setter
  def exponential_smoothing_max_min_diff(self, val: float) -> None: self._exponential_smoothing_max_min_diff = val

  @property
  def double_tops_diff(self) -> float: return self._double_tops_diff

  @double_tops_diff.setter
  def double_tops_diff(self, val: float) -> None: self._double_tops_diff = val
