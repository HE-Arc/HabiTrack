import axios from "axios";

// For clarity, we split the functions (simplifies maintenance)
export const fetchEntries = async (username = null) => {
  if (username == null) {
    return entryAction("get");
  } else {
    return getCreatedEntries(username);
  }
};

// Generic function for all of the above (create, update, delete)
export const entryAction = async (action, entry) => {
  const returnValue = {
    errors: [],
    success: null,
    data: null,
  };
  let response = null;

  try {
    switch (action) {
      case "create":
        response = await axios.post("/entries/", {
          entry: entry,
        });
        break;
      case "get":
        response = await axios.get("/entries/");
        break;
      case "update":
        response = await axios.put("/entries/", {
          entry: entry,
        });
        break;
      case "delete":
        response = await axios.delete(`/entries/${entry.id}/`);
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

export const getCreatedEntries = async (username) => {
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
    const response = await axios.get(`/entries/user/${username}/`);
    if (response.data.success) {
      returnValue.success = response.data.success;
      returnValue.data = response.data.entries;
    } else {
      returnValue.errors = [response.data.error];
    }
  } catch (error) {
    returnValue.errors = error.response.data.errors;
  }
  return returnValue;
};

export const getEntriesCount = async (username = null) => {
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
    const response = await axios.get(`/entries/count/${username}/`);
    if (response.data.success) {
      returnValue.success = response.data.success;
      returnValue.data = response.data.count;
    } else {
      returnValue.errors = [response.data.error];
    }
  } catch (error) {
    returnValue.errors = error.response.data.errors;
  }
  return returnValue;
};

export const getTemplateEntries = async (templateId = null) => {
  let returnValue = {
    errors: [],
    success: null,
    data: null,
  };
  if (!templateId) {
    returnValue.errors = ["Please give a template id"];
    return returnValue;
  }
  try {
    const response = await axios.get(`/entries/template/${templateId}/`);
    if (response.data.success) {
      returnValue.success = response.data.success;
      returnValue.data = response.data.entries;
    } else {
      returnValue.errors = [response.data.error];
    }
  } catch (error) {
    returnValue.errors = error.response.data.errors;
  }
  return returnValue;
};
