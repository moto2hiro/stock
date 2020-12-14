from app_utils.number_utils import NumberUtils
from test.test_base import TestBase


class TestNumberUtils(TestBase):

  def test_has_bit_should_return_appropriately(self) -> None:
    # ACT
    zero_has_one: bool = NumberUtils.has_bit(0, 1)
    one_has_one: bool = NumberUtils.has_bit(1, 1)
    one_has_two: bool = NumberUtils.has_bit(1, 2)
    two_has_one: bool = NumberUtils.has_bit(2, 1)
    two_has_two: bool = NumberUtils.has_bit(2, 2)
    two_has_four: bool = NumberUtils.has_bit(2, 4)
    three_has_one: bool = NumberUtils.has_bit(3, 1)
    three_has_two: bool = NumberUtils.has_bit(3, 2)
    three_has_four: bool = NumberUtils.has_bit(3, 4)
    four_has_one: bool = NumberUtils.has_bit(4, 1)
    four_has_two: bool = NumberUtils.has_bit(4, 2)
    four_has_four: bool = NumberUtils.has_bit(4, 4)
    four_has_eight: bool = NumberUtils.has_bit(4, 8)

    # ASSERT
    self.assertFalse(zero_has_one)
    self.assertTrue(one_has_one)
    self.assertFalse(one_has_two)
    self.assertFalse(two_has_one)
    self.assertTrue(two_has_two)
    self.assertFalse(two_has_four)
    self.assertTrue(three_has_one)
    self.assertTrue(three_has_two)
    self.assertFalse(three_has_four)
    self.assertFalse(four_has_one)
    self.assertFalse(four_has_two)
    self.assertTrue(four_has_four)
    self.assertFalse(four_has_eight)

  def test_add_bit_should_return_appropriately(self) -> None:
    # ACT
    zero_add_one: bool = NumberUtils.add_bit(0, 1)
    zero_add_two: bool = NumberUtils.add_bit(0, 2)
    one_add_one: bool = NumberUtils.add_bit(1, 1)
    one_add_two: bool = NumberUtils.add_bit(1, 2)
    two_add_one: bool = NumberUtils.add_bit(2, 1)
    two_add_two: bool = NumberUtils.add_bit(2, 2)
    two_add_four: bool = NumberUtils.add_bit(2, 4)
    three_add_one: bool = NumberUtils.add_bit(3, 1)
    three_add_two: bool = NumberUtils.add_bit(3, 2)
    three_add_four: bool = NumberUtils.add_bit(3, 4)
    four_add_one: bool = NumberUtils.add_bit(4, 1)
    four_add_two: bool = NumberUtils.add_bit(4, 2)
    four_add_four: bool = NumberUtils.add_bit(4, 4)
    four_add_eight: bool = NumberUtils.add_bit(4, 8)

    # ASSERT
    self.assertEqual(1, zero_add_one)
    self.assertEqual(2, zero_add_two)
    self.assertEqual(1, one_add_one)
    self.assertEqual(3, one_add_two)
    self.assertEqual(3, two_add_one)
    self.assertEqual(2, two_add_two)
    self.assertEqual(6, two_add_four)
    self.assertEqual(3, three_add_one)
    self.assertEqual(3, three_add_two)
    self.assertEqual(7, three_add_four)
    self.assertEqual(5, four_add_one)
    self.assertEqual(6, four_add_two)
    self.assertEqual(4, four_add_four)
    self.assertEqual(12, four_add_eight)

  def test_delete_bit_should_return_appropriately(self) -> None:
    # ACT
    zero_delete_one: bool = NumberUtils.delete_bit(0, 1)
    zero_delete_two: bool = NumberUtils.delete_bit(0, 2)
    one_delete_one: bool = NumberUtils.delete_bit(1, 1)
    one_delete_two: bool = NumberUtils.delete_bit(1, 2)
    two_delete_one: bool = NumberUtils.delete_bit(2, 1)
    two_delete_two: bool = NumberUtils.delete_bit(2, 2)
    two_delete_four: bool = NumberUtils.delete_bit(2, 4)
    three_delete_one: bool = NumberUtils.delete_bit(3, 1)
    three_delete_two: bool = NumberUtils.delete_bit(3, 2)
    three_delete_four: bool = NumberUtils.delete_bit(3, 4)
    four_delete_one: bool = NumberUtils.delete_bit(4, 1)
    four_delete_two: bool = NumberUtils.delete_bit(4, 2)
    four_delete_four: bool = NumberUtils.delete_bit(4, 4)
    four_delete_eight: bool = NumberUtils.delete_bit(4, 8)

    # ASSERT
    self.assertEqual(0, zero_delete_one)
    self.assertEqual(0, zero_delete_two)
    self.assertEqual(0, one_delete_one)
    self.assertEqual(1, one_delete_two)
    self.assertEqual(2, two_delete_one)
    self.assertEqual(0, two_delete_two)
    self.assertEqual(2, two_delete_four)
    self.assertEqual(2, three_delete_one)
    self.assertEqual(1, three_delete_two)
    self.assertEqual(3, three_delete_four)
    self.assertEqual(4, four_delete_one)
    self.assertEqual(4, four_delete_two)
    self.assertEqual(0, four_delete_four)
    self.assertEqual(4, four_delete_eight)
