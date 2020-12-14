from datetime import date, datetime, timedelta
from dateutil import tz
from app_consts import AppConsts
from app_utils.string_utils import StringUtils
from app_utils.log_utils import LogUtils
from pandas.core.indexes.datetimes import DatetimeIndex
from pandas.tseries.holiday import \
    AbstractHolidayCalendar, Holiday, nearest_workday, USMartinLutherKingJr, \
    USPresidentsDay, GoodFriday, USMemorialDay, USLaborDay, USThanksgivingDay


class DateUtils:

  @staticmethod
  def to_string(src_date: date) -> str:
    if not src_date or not isinstance(src_date, (date, datetime)):
      return ''
    return src_date.isoformat()

  @staticmethod
  def get_date(datestr: str, fmt: str) -> date:
    if not isinstance(datestr, str) \
            or not isinstance(fmt, str) \
            or StringUtils.isNullOrWhitespace(datestr) \
            or StringUtils.isNullOrWhitespace(fmt):
      return None
    try:
      return datetime.strptime(datestr, fmt)
    except Exception as ex:
      LogUtils.warning('Invalid date inputs={0} {1}'.format(datestr, fmt))
      return None

  @staticmethod
  def get_date_from_epoch(utc_seconds: int, to_zone: str = '') -> datetime:
    if utc_seconds < 0:
      return None
    ret: datetime = datetime.utcfromtimestamp(utc_seconds)
    ret = ret.replace(tzinfo=tz.tzutc())
    if to_zone:
      ret = ret.astimezone(tz.gettz(to_zone))
    return ret

  @staticmethod
  def get_diff(first_date: date, second_date: date) -> timedelta:
    if not first_date \
            or not second_date \
            or not isinstance(first_date, (date, datetime)) \
            or not isinstance(second_date, (date, datetime)):
      return None
    return first_date - second_date

  @staticmethod
  def get_quarter(month: int) -> int:
    if not isinstance(month, int) or month < 1 or month > 12:
      return None
    return (month - 1)//3 + 1

  @staticmethod
  def add_business_days(start_date: date, days: int) -> date:
    if not start_date or not isinstance(start_date, (date, datetime)):
      return None
    if not days or not isinstance(days, int) or days == 0:
      return start_date
    is_add: bool = days > 0
    days = abs(days)
    current_date: date = start_date
    while days > 0:
      current_date = current_date + timedelta(days=1) if is_add else current_date - timedelta(days=1)
      stock_holidays: DatetimeIndex = USTradingCalendar().holidays(
          start=date(current_date.year - 1, 1, 1),
          end=date(current_date.year + 1, 1, 1))
      # 5 = Saturday, 6 = Sunday
      if current_date.weekday() >= AppConsts.WEEKDAY_IDX_SAT \
              or current_date in stock_holidays \
              or DateUtils.to_string(current_date) in AppConsts.SPECIAL_NON_TRADING_DAYS:
        continue
      days = days - 1
    return current_date


class USTradingCalendar(AbstractHolidayCalendar):
  """
  This may not be constant.
  This is the Stock Exchange Holidays (not the US Bank Holidays)
  """
  rules = [
      Holiday('NewYearsDay', month=1, day=1, observance=nearest_workday),
      USMartinLutherKingJr,
      USPresidentsDay,
      GoodFriday,
      USMemorialDay,
      Holiday('USIndependenceDay', month=7, day=4, observance=nearest_workday),
      USLaborDay,
      USThanksgivingDay,
      Holiday('Christmas', month=12, day=25, observance=nearest_workday)
  ]
