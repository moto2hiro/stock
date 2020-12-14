from test.test_base import TestBase
from services.import_service import ImportService
from services.stock_service import StockService


class TestImportService(TestBase):

  def __init__(self, *args, **kwargs):
    super(TestImportService, self).__init__(*args, **kwargs)
    self.__import_service: ImportService = ImportService()
    self.__stock_service: StockService = StockService()

  def test_import_company_profiles(self) -> None:
    pass
    # self.__import_service.import_company_profiles()
