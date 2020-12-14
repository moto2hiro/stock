export default class PropUtils {
  static setValue = (srcObj, fieldName, fieldValue) => {
    if (!srcObj || !fieldName) {
      return null;
    }

    // Get Child Obj
    var childObjs = fieldName.split('.');
    var obj = srcObj;
    for (var i = 0; i < childObjs.length - 1; i++) {
      var childObj = childObjs[i];
      if (!obj[childObj]) {
        obj[childObj] = {};
      }
      obj = obj[childObj];
    }

    // Set Value
    obj[childObjs[childObjs.length - 1]] = fieldValue;

    return srcObj;
  };

  static getValue = (srcObj, fieldName) => {
    if (!srcObj || !fieldName) {
      return null;
    }

    var ret = srcObj;
    var childObjs = fieldName.split('.');
    fieldName = fieldName.replace(/\[(\w+)\]/g, '.$1'); // convert indexes to properties
    fieldName = fieldName.replace(/^\./, ''); // strip a leading dot
    for (var i = 0, n = childObjs.length; i < n; ++i) {
      var childObj = childObjs[i];
      if (childObj in ret) {
        ret = ret[childObj];
      } else {
        return;
      }
    }
    return ret;
  };
}
