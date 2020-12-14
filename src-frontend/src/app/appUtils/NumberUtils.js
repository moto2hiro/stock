export default class NumberUtils {
  static toInt = (src, dflt = 0) => {
    var ret = parseInt(src);
    return !isNaN(ret) ? ret : dflt;
  };

  static toFloat = (src, dflt = 0, decimals = 2) => {
    var ret = parseFloat(src);
    return !isNaN(ret) ? NumberUtils.round(ret, decimals) : dflt;
  };

  static round = (src, decimals = 2) => {
    if (!('' + src).includes('e')) {
      return +(Math.round(src + 'e+' + decimals) + 'e-' + decimals);
    } else {
      var arr = ('' + src).split('e');
      var sig = '';
      if (+arr[1] + decimals > 0) {
        sig = '+';
      }
      return +(Math.round(+arr[0] + 'e' + sig + (+arr[1] + decimals)) + 'e-' + decimals);
    }
  };

  static hasBit = (orgNumber, bitToSearch) => {
    return (orgNumber | bitToSearch) === orgNumber;
  };

  static addBit = (orgNumber, bitToAdd) => {
    return orgNumber | bitToAdd;
  };

  static deleteBit = (orgNumber, bitToDelete) => {
    if (!NumberUtils.hasBit(orgNumber, bitToDelete)) {
      return orgNumber;
    }
    return orgNumber ^ bitToDelete;
  };
}
