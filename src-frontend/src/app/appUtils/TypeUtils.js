export default class TypeUtils {
  static isString = (src) => {
    return typeof src === 'string' || src instanceof String;
  };

  static isObject = (src) => {
    return typeof src === 'object' && src !== null;
  };
}
