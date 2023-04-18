import axios from "axios";
import { ref } from "vue";

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
  try {
    const response = ref(null);
    switch (action) {
      case "create":
        response.value = await axios.put(`/templates/`, template);
        break;
      case "get":
        response.value = await axios.get("/templates/");
        console.log(response.value.data);
        break;
      case "update":
        response.value = await axios.put(
          `/templates/${template.id}/`,
          template
        );
        break;
      case "delete":
        response.value = await axios.delete(`/templates/${template.id}/`);
        break;
    }
    if (response.value.data.success) {
      return response.value.data;
    } else {
      return response.value.data.error;
    }
  } catch (error) {
    console.log("[ERROR] " + action + error);
  }
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
