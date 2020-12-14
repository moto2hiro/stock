class InvertedHeadAndShouldersRequest:

  @property
  def exponential_smoothing_alpha(self) -> float: return self._exponential_smoothing_alpha

  @exponential_smoothing_alpha.setter
  def exponential_smoothing_alpha(self, val: float) -> None: self._exponential_smoothing_alpha = val

  @property
  def exponential_smoothing_max_min_diff(self) -> float: return self._exponential_smoothing_max_min_diff

  @exponential_smoothing_max_min_diff.setter
  def exponential_smoothing_max_min_diff(self, val: float) -> None: self._exponential_smoothing_max_min_diff = val

  @property
  def shoulder_diff(self) -> float: return self._shoulder_diff

  @shoulder_diff.setter
  def shoulder_diff(self, val: float) -> None: self._shoulder_diff = val

  @property
  def neck_diff(self) -> float: return self._neck_diff

  @neck_diff.setter
  def neck_diff(self, val: float) -> None: self._neck_diff = val
