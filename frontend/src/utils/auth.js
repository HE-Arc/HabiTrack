import axios from "axios";
import { Cookies } from "quasar";

// Get current user
export const getCurrentUsername = async () => {
  try {
    const response = await axios.get("whoami/");
    if (response.data.username != null) {
      Cookies.set("username", response.data.username, {
        expires: 1 / 48,
      }); // expires in 30 minutes
      return response.data.username;
    } else {
      Cookies.remove("username");
      return null;
    }
  } catch (error) {
    console.log(error);
  }
};

export const register = async (username, password, confirm) => {
  const returnValue = {
    errors: [],
    success: null,
  };
  if (!username || !password || !confirm) {
    returnValue.errors = ["Please enter a username and password"];
    return returnValue;
  }
  try {
    const response = await axios.post("register/", {
      username: username,
      password: password,
      confirm: confirm,
    });
    if (response.data.success) {
      returnValue.success = response.data.success;
      // Add a cookie to the browser to keep the user logged in
      Cookies.set("username", username, {
        expires: 1 / 48,
      }); // expires in 30 minutes
    } else {
      returnValue.errors = [response.data.error];
    }
  } catch (error) {
    returnValue.errors = error.response.data.errors;
  }
  return returnValue;
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
      username: username,
      password: password,
    });
    if (response.data.success) {
      returnValue.success = response.data.success;
      // Add a cookie to the browser to keep the user logged in
      Cookies.set("username", username, {
        expires: 1 / 48,
      }); // expires in 30 minutes
    } else {
      returnValue.errors = [response.data.error];
    }
  } catch (error) {
    returnValue.errors = error.response.data.errors;
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

export const changePassword = async (
  username,
  password,
  new_password,
  confirm
) => {
  const returnValue = {
    errors: [],
    success: null,
  };
  if (!username || !password || !new_password || !confirm) {
    returnValue.errors = ["Please enter a new password"];
    return returnValue;
  }
  try {
    const response = await axios.post("change-password/", {
      username: username,
      password: password,
      new: new_password,
      confirm: confirm,
    });
    if (response.data.success) {
      returnValue.success = response.data.success;
    } else {
      returnValue.errors = [response.data.error];
    }
  } catch (error) {
    returnValue.errors = error.response.data.errors;
  }
  return returnValue;
};

export const deleteAccount = async (username) => {
  const returnValue = {
    errors: [],
    success: null,
  };
  if (!username) {
    returnValue.errors = ["Please provide a username"];
    return returnValue;
  }
  try {
    const response = await axios.delete(`users/${username}/`);
    if (response.data.success) {
      returnValue.success = response.data.success;
      // clear the username cookie
      Cookies.remove("username");
    } else {
      returnValue.errors = [response.data.error];
    }
  } catch (error) {
    returnValue.errors = error.response.data.errors;
  }
  return returnValue;
};
