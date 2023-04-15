import axios from "axios";
import { Cookies } from "quasar";

// Get current user
export const getCurrentUsername = async () => {
  if (Cookies.has("username")) {
    return Cookies.get("username");
  }
};

export const login = async (username, password) => {
  const returnValue = {
    errors: [],
    success: null,
  };
  if (!username || !password) {
    returnValue.errors = ["Please enter a username and password"];
    return returnValue;
  }
  try {
    const response = await axios.post("login/", {
      username: username.value,
      password: password.value,
    });
    if (response.data.success) {
      returnValue.success = response.data.success;
      // Add a cookie to the browser to keep the user logged in
      Cookies.set("username", username.value, {
        expires: 1 / 48,
      }); // expires in 30 minutes
    } else {
      returnValue.errors = [response.data.error];
    }
  } catch (error) {
    returnValue.errors = error.response.data;
  }
  return returnValue;
};

export const logout = async () => {
  try {
    const response = await axios.post("logout/", null, {});
    if (response.data.success) {
      // clear the username cookie
      Cookies.remove("username");
      return { success: response.data.success };
    }
    return { errors: [response.data.error] };
  } catch (error) {
    return { errors: error.response.data };
  }
};