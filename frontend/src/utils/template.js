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
export const templateAction = async (
  action,
  template = null,
  username = null
) => {
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
    } else {
      returnValue.errors = ["Unknown error"];
    }
  } catch (error) {
    returnValue.errors = error.response.data;
  }
  return returnValue;
};

export const getCreatedTemplates = async (username) => {
  try {
    const response = await axios.get(`/templates/user/${username}/`);
    if (response.data.success) {
      return response.data.templates;
    } else {
      return null;
    }
  } catch (error) {
    console.log(error);
  }
};

export const getTemplatesCount = async (username = null) => {
  if (username) {
    try {
      const response = await axios.get(`/templates/count/${username}/`);
      if (response.data.success) {
        return response.data.count;
      } else {
        return "Error getting template count";
      }
    } catch (error) {
      console.log("[ERROR] getTemplatesCount " + error);
    }
  }
};

export const getEntries = async (username) => {
  // if (username) {
  //! TODO - Implement this
  username;
  return [];
};

export const getEntriesCount = async (username = null) => {
  // if (username) {
  //   try {
  //     const response = await axios.get(`/entries/count/${username}/`);
  //     if (response.data.success) {
  //       return response.data.count;
  //     } else {
  //       return "Error getting entry count";
  //     }
  //   } catch (error) {
  //     console.log("[ERROR] getEntriesCount " + error);
  //   }
  // }
  //! TODO - Implement this
  username;
  return 0;
};
