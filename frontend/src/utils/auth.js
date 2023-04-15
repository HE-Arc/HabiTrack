import axios from "axios";

// Get current user
export const getCurrentUser = async () => {
  try {
    const response = await axios.get("/users/current/");
    if (response.data) {
      return response.data.user;
    } else {
      return null;
    }
  } catch (error) {
    console.log(error);
  }
};
