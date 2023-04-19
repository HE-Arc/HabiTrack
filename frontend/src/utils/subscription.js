import axios from "axios";

export const fetchSubscriptions = async (username) => {
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
    const response = await axios.get(`/subscriptions/user/${username}/`);
    if (response.data.success) {
      returnValue.success = response.data.success;
      returnValue.data = response.data.subscriptions;
    } else {
      returnValue.errors = [response.data.error];
    }
  } catch (error) {
    returnValue.errors = error.response.data.errors;
  }
  return returnValue;
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
    const response = await axios.get(`/subscriptions/count/${username}/`);
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
