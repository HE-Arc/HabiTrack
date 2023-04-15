import axios from "axios";

export const fetchSubscriptions = async (user) => {
  try {
    console.log(user.value.id);
    const response = await axios.get(`/subscriptions/user/${user.value.id}`);
    console.log(response.data);
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
