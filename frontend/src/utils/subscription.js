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
export const isUserSubscribed = async (user, template) => {
  try {
    const response = await axios.get(
      `/subscriptions/${user.value.id}/subscribed/${template.id}/`
    );
    if (response.data.success && response.data.subscribed) {
      return true;
    } else {
      return false;
    }
  } catch (error) {
    console.log(error);
  }
};

// Subscribe user to a template
export const subOrUnsubScribe = async (route, user, template) => {
  await axios
    .post(`/users/${user.value.id}/${route}/${template.id}/`, {})
    .then((response) => {
      // handle success response
      if (response.data.success) {
        return true;
      } else {
        return false;
      }
    })
    .catch((error) => {
      // handle error response
      console.log(error);
      return false;
    });
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
