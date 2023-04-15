import axios from "axios";
import { ref } from "vue";

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
