import axios from "axios";

export const fetchSubscriptions = async (username) => {
  try {
    const response = await axios.get(`/subscriptions/user/${username}`);
    if (response.data.success) {
      return response.data.subscriptions;
    } else {
      console.log("Failed!");
      return null;
    }
  } catch (error) {
    console.log(error);
  }
};

// Check if user is subscribed to a template
export const isUserSubscribed = async (username, template_id) => {
  let returnValue = {
    errors: [],
    success: null,
    subscribed: false,
  };
  if (!username || !template_id) {
    returnValue.errors = [
      "Please give a username and template_id",
      "Values given: " + username + " " + template_id + " ",
    ];
    return returnValue;
  }

  try {
    const response = await axios.get(
      `/subscriptions/${username}/subscribed/${template_id}/`
    );
    if (response.data.success) {
      returnValue.success = response.data.success;
      returnValue.subscribed = response.data.subscribed;
    } else {
      returnValue.errors = [response.data.error];
    }
  } catch (error) {
    returnValue.errors = error.response.data.errors;
  }
  return returnValue;
};

// Subscribe user to a template
export const subOrUnsubScribe = async (route, username, template_id) => {
  let returnValue = {
    errors: [],
    success: null,
  };
  if (!username || !template_id) {
    returnValue.errors = ["Please give a username and template_id"];
    return returnValue;
  }

  try {
    const response = await axios.post(
      "subscriptions/" + route + "/" + username + "/" + template_id + "/"
    );
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

// Get subscription count
export const getSubscriptionsCount = async (username = null) => {
  if (username) {
    try {
      const response = await axios.get(`/subscriptions/count/${username}/`);
      if (response.data.success) {
        return response.data.count;
      } else {
        return "Error getting subscription count";
      }
    } catch (error) {
      console.log("[ERROR] getSubscriptionCount " + error);
    }
  }
};
