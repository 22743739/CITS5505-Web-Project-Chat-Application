window.validator = {
  required: function (val) {
    return !(typeof val === 'undefined' || val === null || val === '');
  },
  isEmail: function (val) {
    var reg = /^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/;
    return reg.test(val);
  },
  isEqual: function (a, b) {
    return a === b;
  },
  isNumber: function (val) {
    return /^\d+$/.test(val);
  },
  isMin: function (val, minLen = 5) {
    return val && val.length < minLen;
  },
};

function validatorRegisterForm(values) {
  var errorMsgs = [];

  // validation
  if (!validator.required(values.name)) {
    errorMsgs.push({
      field: 'name',
      label: 'Please provide field name',
    });
  } else {
    if (validator.isMin(values.name, 5)) {
      errorMsgs.push({
        field: 'name',
        label: 'The minimum length of a name is 5',
      });
    }
  }
  if (!validator.required(values.email)) {
    errorMsgs.push({
      field: 'email',
      label: 'Please provide field email',
    });
  } else {
    if (!validator.isEmail(values.email)) {
      errorMsgs.push({
        field: 'email',
        label: 'Please provide the correct email format',
      });
    }
  }

  if (!validator.required(values.mobileNumber)) {
    errorMsgs.push({
      field: 'mobileNumber',
      label: 'Please provide field mobileNumber',
    });
  } else {
    if (!validator.isNumber(values.mobileNumber)) {
      errorMsgs.push({
        field: 'mobileNumber',
        label: 'Please provide the correct mobileNumber format',
      });
    }
  }

  if (!validator.required(values.password)) {
    errorMsgs.push({
      field: 'password',
      label: 'Please provide field password',
    });
  } else {
    if (validator.isMin(values.password, 5)) {
      errorMsgs.push({
        field: 'password',
        label: 'The minimum length of a password is 5',
      });
    }
  }

  if (!validator.required(values.password2)) {
    errorMsgs.push({
      field: 'password2',
      label: 'Please provide field confirm password',
    });
  } else {
    if (!validator.isEqual(values.password, values.password2)) {
      errorMsgs.push({
        field: 'password2',
        label: 'The two passwords are inconsistent',
      });
    }
  }

  return errorMsgs;
}
