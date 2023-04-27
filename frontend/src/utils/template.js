import axios from "axios";

// For clarity, we split the functions (simplifies maintenance)
export const fetchTemplates = async (username = null) => {
  if (username == null) {
    return templateAction("get");
  } else {
    return getCreatedTemplates(username);
  }
};

// Generic function for all of the above (create, update, delete)
export const templateAction = async (action, template = null) => {
  const returnValue = {
    errors: [],
    success: null,
    data: null,
  };
  let response = null;

  try {
    switch (action) {
      case "create":
        response = await axios.post(`/templates/`, {
          template: template,
        });
        break;
      case "get":
        response = await axios.get("/templates/");
        break;
      case "update":
        response = await axios.put(`/templates/`, {
          template: template,
        });
        break;
      case "delete":
        response = await axios.delete(`/templates/${template.id}/`);
        break;
      default:
        returnValue.errors = ["Invalid action"];
        return returnValue;
    }
    if (response.data.success) {
      returnValue.success = response.data.success;
    } else if (response.data.errors) {
      returnValue.errors = response.data.errors;
    } else if (response.status === 200 && response.data.length > 0) {
      returnValue.success = true;
      returnValue.data = response.data;
    } else if (response.status === 200 && response.data.length === 0) {
      returnValue.success = true;
      returnValue.data = 0;
    } else {
      returnValue.errors = ["Unknown error"];
    }
  } catch (error) {
    returnValue.errors = error.response.data;
  }
  return returnValue;
};

export const getCreatedTemplates = async (username) => {
  let returnValue = {
    errors: [],
    success: null,
    data: null,
  };
  if (!username) {
    returnValue.errors = ["Please give a username"];
    return returnValue;
  }
  try {
    const response = await axios.get(`/templates/user/${username}/`);
    if (response.data.success) {
      returnValue.success = response.data.success;
      returnValue.data = response.data.templates;
    } else {
      returnValue.errors = [response.data.error];
    }
  } catch (error) {
    returnValue.errors = error.response.data.errors;
  }
  return returnValue;
};

export const getTemplatesCount = async (username = null) => {
  let returnValue = {
    errors: [],
    success: null,
    count: 0,
  };
  if (!username) {
    returnValue.errors = ["Please give a username"];
    return returnValue;
  }
  try {
    const response = await axios.get(`/templates/count/${username}/`);
    if (response.data.success) {
      returnValue.success = response.data.success;
      returnValue.count = response.data.count;
    } else {
      returnValue.errors = [response.data.error];
    }
  } catch (error) {
    returnValue.errors = error.response.data.errors;
  }
  return returnValue;
};
