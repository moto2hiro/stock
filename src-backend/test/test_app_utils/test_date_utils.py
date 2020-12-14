from datetime import date, datetime, timedelta
from dateutil import tz
from app_consts import AppConsts
from app_utils.date_utils import DateUtils
from test.test_base import TestBase


class TestDateUtils(TestBase):

  def test_to_string_should_return_date_string(self) -> None:
    # ARRANGE
    none_case: date = None
    invalid_type_case: int = 1
    date_case: date = date(2000, 1, 1)

    # ACT
    ret_none_case: str = DateUtils.to_string(none_case)
    ret_invalid_type_case: str = DateUtils.to_string(invalid_type_case)
    ret_date_case: str = DateUtils.to_string(date_case)

    # ASSERT
    self.assertEqual('', ret_none_case)
    self.assertEqual('', ret_invalid_type_case)
    self.assertEqual('2000-01-01', ret_date_case)

  def test_get_date_should_not_return_date_if_invalid_request(self) -> None:
    # ARRANGE
    none_datestr_case: str = None
    empty_datestr_case: str = ''
    whitespace_datestr_case: str = ' '
    invalid_datestr_case: str = 'foo'
    invalid_datestr_type_case: int = 1
    none_fmt_case: str = None
    empty_fmt_case: str = ''
    whitespace_fmt_case: str = ' '
    invalid_fmt_case: str = 'bar'
    invalid_fmt_type_case: int = 1

    # ACT
    ret_none_datestr_case: date = DateUtils.get_date(none_datestr_case, 'fake')
    ret_empty_datestr_case: date = DateUtils.get_date(empty_datestr_case, 'fake')
    ret_whitespace_datestr_case: date = DateUtils.get_date(whitespace_datestr_case, 'fake')
    ret_invalid_datestr_case: date = DateUtils.get_date(invalid_datestr_case, '%Y-%m-%d')
    ret_invalid_datestr_type_case: date = DateUtils.get_date(invalid_datestr_type_case, '%Y-%m-%d')
    ret_none_fmt_case: date = DateUtils.get_date('fake', none_fmt_case)
    ret_empty_fmt_case: date = DateUtils.get_date('fake', empty_fmt_case)
    ret_whitespace_fmt_case: date = DateUtils.get_date('fake', whitespace_fmt_case)
    ret_invalid_fmt_case: date = DateUtils.get_date('2001-01-01', invalid_fmt_case)
    ret_invalid_fmt_type_case: date = DateUtils.get_date('2001-01-01', invalid_fmt_type_case)

    # ASSERT
    self.assertIsNone(ret_none_datestr_case)
    self.assertIsNone(ret_empty_datestr_case)
    self.assertIsNone(ret_whitespace_datestr_case)
    self.assertIsNone(ret_invalid_datestr_case)
    self.assertIsNone(ret_invalid_datestr_type_case)
    self.assertIsNone(ret_none_fmt_case)
    self.assertIsNone(ret_empty_fmt_case)
    self.assertIsNone(ret_whitespace_fmt_case)
    self.assertIsNone(ret_invalid_fmt_case)
    self.assertIsNone(ret_invalid_fmt_type_case)

  def test_get_date_should_return_date_if_valid_request(self) -> None:
    # ARRANGE
    test_date: str = '2001-01-01'
    fmt: str = '%Y-%m-%d'

    # ACT
    ret_test_date: date = DateUtils.get_date(test_date, fmt)

    # ASSERT
    self.assertIsNotNone(ret_test_date)
    self.assertEqual(2001, ret_test_date.year)
    self.assertEqual(1, ret_test_date.month)
    self.assertEqual(1, ret_test_date.day)

  def test_get_date_from_epoch_should_return_appropriately(self) -> None:
    # ARRANGE
    date_2020_07_15_4_utc: datetime = datetime(2020, 7, 15, 4, tzinfo=tz.tzutc())
    date_2020_07_16_4_utc: datetime = datetime(2020, 7, 16, 4, tzinfo=tz.tzutc())
    date_2020_07_16_0_ny: datetime = datetime(2020, 7, 16, 0, tzinfo=tz.gettz(AppConsts.TZ_NY))
    seconds_2020_07_15_4_utc: int = 1594785600
    seconds_2020_07_16_4_utc: int = 1594872000

    # ACT
    ret_2020_07_15_4_utc: datetime = DateUtils.get_date_from_epoch(seconds_2020_07_15_4_utc)
    ret_2020_07_16_4_utc: datetime = DateUtils.get_date_from_epoch(seconds_2020_07_16_4_utc)
    ret_2020_07_16_0_ny: datetime = DateUtils.get_date_from_epoch(seconds_2020_07_16_4_utc, AppConsts.TZ_NY)

    # ASSERT
    self.assertEqual(date_2020_07_15_4_utc, ret_2020_07_15_4_utc)
    self.assertEqual(date_2020_07_16_4_utc, ret_2020_07_16_4_utc)
    self.assertEqual(date_2020_07_16_0_ny, ret_2020_07_16_0_ny)

  def test_get_diff_should_return_none_if_invalid_request(self) -> None:
    # ARRANGE
    normal_date: date = date(2001, 1, 1)
    none_first_date: date = None
    none_second_date: date = None
    invalid_type_first_date: int = 1
    invalid_type_second_date: int = 1

    # ACT
    ret_both_none_case: date = DateUtils.get_diff(none_first_date, none_second_date)
    ret_first_none_case: date = DateUtils.get_diff(none_first_date, normal_date)
    ret_second_none_case: date = DateUtils.get_diff(normal_date, none_second_date)
    ret_both_invalid_type_case: date = DateUtils.get_diff(invalid_type_first_date, invalid_type_second_date)
    ret_invalid_type_first_case: date = DateUtils.get_diff(invalid_type_first_date, normal_date)
    ret_invalid_type_second_case: date = DateUtils.get_diff(normal_date, invalid_type_second_date)

    # ASSERT
    self.assertIsNone(ret_both_none_case)
    self.assertIsNone(ret_first_none_case)
    self.assertIsNone(ret_second_none_case)
    self.assertIsNone(ret_invalid_type_first_case)
    self.assertIsNone(ret_invalid_type_second_case)

  def test_get_diff_should_return_timedelta_if_valid_request(self) -> None:
    # ARRANGE
    first_date: date = date(2001, 1, 1)
    second_date: date = date(2003, 1, 1)
    expected_timedelta: timedelta = first_date - second_date

    # ACT
    ret_actual: timedelta = DateUtils.get_diff(first_date, second_date)

    # ASSERT
    self.assertEqual(expected_timedelta, ret_actual)

  def test_get_quarter_should_return_appropriately(self) -> None:
    # ARRANGE
    less_than_1_case: int = 0
    more_than_12_case: int = 13
    invalid_type_case: str = 'foo'
    january_case: int = 1
    february_case: int = 2
    march_case: int = 3
    april_case: int = 4
    may_case: int = 5
    june_case: int = 6
    july_case: int = 7
    august_case: int = 8
    september_case: int = 9
    october_case: int = 10
    november_case: int = 11
    december_case: int = 12

    # ACT
    ret_less_than_1_case: int = DateUtils.get_quarter(less_than_1_case)
    ret_more_than_12_case: int = DateUtils.get_quarter(more_than_12_case)
    ret_invalid_type_case: int = DateUtils.get_quarter(invalid_type_case)
    ret_january_case: int = DateUtils.get_quarter(january_case)
    ret_february_case: int = DateUtils.get_quarter(february_case)
    ret_march_case: int = DateUtils.get_quarter(march_case)
    ret_april_case: int = DateUtils.get_quarter(april_case)
    ret_may_case: int = DateUtils.get_quarter(may_case)
    ret_june_case: int = DateUtils.get_quarter(june_case)
    ret_july_case: int = DateUtils.get_quarter(july_case)
    ret_august_case: int = DateUtils.get_quarter(august_case)
    ret_september_case: int = DateUtils.get_quarter(september_case)
    ret_october_case: int = DateUtils.get_quarter(october_case)
    ret_november_case: int = DateUtils.get_quarter(november_case)
    ret_december_case: int = DateUtils.get_quarter(december_case)

    # ASSERT
    self.assertIsNone(ret_less_than_1_case)
    self.assertIsNone(ret_more_than_12_case)
    self.assertIsNone(ret_invalid_type_case)
    self.assertEqual(ret_january_case, 1)
    self.assertEqual(ret_february_case, 1)
    self.assertEqual(ret_march_case, 1)
    self.assertEqual(ret_april_case, 2)
    self.assertEqual(ret_may_case, 2)
    self.assertEqual(ret_june_case, 2)
    self.assertEqual(ret_july_case, 3)
    self.assertEqual(ret_august_case, 3)
    self.assertEqual(ret_september_case, 3)
    self.assertEqual(ret_october_case, 4)
    self.assertEqual(ret_november_case, 4)
    self.assertEqual(ret_december_case, 4)

  def test_add_business_days_should_validate_input(self) -> None:
    # ARRANGE
    none_date: date = None
    invalid_type_date: str = 'foo'
    none_days: int = None
    invalid_type_days: str = 'bar'
    normal_date: date = date(2000, 1, 1)
    zero_date: int = 0

    # ACT
    ret_none_date_case: date = DateUtils.add_business_days(none_date, 1)
    ret_invalid_type_date_case: date = DateUtils.add_business_days(invalid_type_date, 1)
    ret_none_days_case: date = DateUtils.add_business_days(normal_date, none_days)
    ret_invalid_type_days_case: date = DateUtils.add_business_days(normal_date, invalid_type_days)

    # ASSERT
    self.assertIsNone(ret_none_date_case)
    self.assertIsNone(ret_invalid_type_date_case)
    self.assertEqual(normal_date, ret_none_days_case)
    self.assertEqual(normal_date, ret_invalid_type_days_case)

  def test_add_business_days_should_return_appropriately(self) -> None:
    # ARRANGE
    monday: date = date(2000, 1, 3)
    tuesday: date = date(2000, 1, 4)
    friday: date = date(2000, 1, 7)
    saturday: date = date(2000, 1, 8)
    sunday: date = date(2000, 1, 9)
    next_monday: date = date(2000, 1, 10)
    next_tuesday: date = date(2000, 1, 11)
    friday_before_christmas: date = date(2000, 12, 22)
    tuesday_after_christmas: date = date(2000, 12, 26)

    # ACT
    add_to_monday_case: date = DateUtils.add_business_days(monday, 1)
    add_to_friday_case: date = DateUtils.add_business_days(friday, 1)
    add_to_saturday_case: date = DateUtils.add_business_days(saturday, 1)
    add_to_sunday_case: date = DateUtils.add_business_days(sunday, 1)
    subtract_from_next_monday_case: date = DateUtils.add_business_days(next_monday, -1)
    subtract_from_next_tuesday_case: date = DateUtils.add_business_days(next_tuesday, -1)
    subtract_from_saturday_case: date = DateUtils.add_business_days(saturday, -1)
    subtract_from_sunday_case: date = DateUtils.add_business_days(sunday, -1)
    add_to_friday_before_christmas: date = DateUtils.add_business_days(friday_before_christmas, 1)

    # ASSERT
    self.assertEqual(tuesday, add_to_monday_case)
    self.assertEqual(next_monday, add_to_friday_case)
    self.assertEqual(next_monday, add_to_saturday_case)
    self.assertEqual(next_monday, add_to_sunday_case)
    self.assertEqual(friday, subtract_from_next_monday_case)
    self.assertEqual(next_monday, subtract_from_next_tuesday_case)
    self.assertEqual(friday, subtract_from_saturday_case)
    self.assertEqual(friday, subtract_from_sunday_case)
    self.assertEqual(tuesday_after_christmas, add_to_friday_before_christmas)
