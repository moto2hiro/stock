import pandas as pd
from pandas.core.frame import DataFrame
from test.test_base import TestBase
from services.strategies.demo_strategy_service import DemoStrategyService


class TestDemoStrategyService(TestBase):

  def __init__(self, *args, **kwargs):
    super(TestDemoStrategyService, self).__init__(*args, **kwargs)

  def test_do_preparations_should_add_custom_property_column(self) -> None:
    # ARRANGE
    prices: DataFrame = pd.DataFrame(data=[0, 1, 2])
    service: DemoStrategyService() = DemoStrategyService(None, None, prices)

    # ACT
    service._do_preparations()

    # ASSERT
    self.assertIsNotNone(service._prices)
    self.assertIsNotNone(service._prices.columns)
    self.assertTrue('custom_property' in service._prices.columns)
    self.assertEqual(0, service._prices['custom_property'][0])
