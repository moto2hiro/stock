import NumberUtils from './NumberUtils';
import PropUtils from './PropUtils';
import TypeUtils from './TypeUtils';

export default class FormUtils {
  static onBlurField = (event, callBack) => {
    var fieldName = event?.target?.name;
    var fieldValue = event?.target?.value;
    var fieldType = event?.target?.type;
    var fieldStep = event?.target?.step;
    if (fieldValue && TypeUtils.isString(fieldValue)) {
      fieldValue = fieldValue.trim();
    }
    if (fieldType === 'number') {
      if (fieldStep === '1' || fieldStep === 1) {
        fieldValue = NumberUtils.toInt(fieldValue);
      } else {
        fieldValue = NumberUtils.toFloat(fieldValue);
      }
    }

    callBack(event, fieldName, fieldValue);
  };

  static validate = (request, ruleObj) => {
    if (!request || !ruleObj) {
      return { isInvalid: false, formData: {} };
    }
    var formData = {};
    for (var field in request) {
      if (!ruleObj.hasOwnProperty(field)) {
        continue;
      }
      var fieldRuleObj = ruleObj[field];
      for (var rule in fieldRuleObj) {
        formData[field] = !formData[field] ? {} : formData[field];
        var fieldValue = PropUtils.getValue(request, field);
        if (TypeUtils.isObject(fieldValue)) {
          formData[field] = FormUtils.validate(fieldValue, fieldRuleObj);
        } else if (rule === 'required' && (fieldValue === null || fieldValue === '')) {
          formData[field].isInvalid = true;
          formData[field].message = 'This field is required.';
        } else if (rule === 'min' && fieldValue < fieldRuleObj[rule]) {
          formData[field].isInvalid = true;
          formData[field].message = `This field must be at least ${fieldRuleObj[rule]}.`;
        } else if (rule === 'max' && fieldValue > fieldRuleObj[rule]) {
          formData[field].isInvalid = true;
          formData[field].message = `This field must be at most ${fieldRuleObj[rule]}.`;
        } else if (rule === 'lessThan' && fieldValue >= request[fieldRuleObj[rule]]) {
          formData[field].isInvalid = true;
          formData[field].message = `This field must be less than ${fieldRuleObj[rule]} field.`;
        } else if (rule === 'greaterThan' && fieldValue <= request[fieldRuleObj[rule]]) {
          formData[field].isInvalid = true;
          formData[field].message = `This field must be greater than ${fieldRuleObj[rule]} field.`;
        } else if (rule === 'notEqual' && fieldValue == request[fieldRuleObj[rule]]) {
          // double equal sign (==) is on purpose.
          formData[field].isInvalid = true;
          formData[field].message = `This field must not be equal to ${fieldRuleObj[rule]} field.`;
        }
      }
    }

    var isInvalid = false;
    for (var key in formData) {
      if (formData[key].isInvalid) {
        isInvalid = true;
        break;
      }
    }
    return { isInvalid: isInvalid, formData: formData };
  };

  static focusInvalidInput = () => {
    var invalidFields = document.querySelectorAll('input[aria-invalid="true"]');
    if (invalidFields && invalidFields.length) {
      invalidFields[0].focus();
    }
  };

  static focusFirstInput = () => {
    var inputFields = document.querySelectorAll('input');
    if (inputFields && inputFields.length) {
      inputFields[0].focus();
    }
  };
}
