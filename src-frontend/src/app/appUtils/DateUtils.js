export default class DateUtils {
  static isoToDate = (src) => {
    if (!src) {
      return null;
    }
    var parts = src.split('-');
    return parts.length >= 3 ? new Date(parts[0], parts[1] - 1, parts[2]) : null;
  };

  static toYYYY_MM_DD = (src) => {
    if (!src) return '';
    var mm = src.getMonth() + 1; // getMonth() is zero-based
    var dd = src.getDate();
    return [src.getFullYear(), (mm > 9 ? '' : '0') + mm, (dd > 9 ? '' : '0') + dd].join('-');
  };

  static getDiffInDays = (first, second) => {
    if (!first || !second) {
      return 0;
    }
    return Math.round((second - first) / (1000 * 60 * 60 * 24));
  };
}
