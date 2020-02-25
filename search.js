const SEARCH_ENDPOINT = "http://localhost:5000/businesses";

const buildResultDOM = business => {
  let result = document.createElement("div");

  let id = document.createElement("p");
  id.innerHTML = `ID: ${business.id}`;

  let name = document.createElement("strong");
  name.innerHTML = `Name: ${business.name}`;

  let city = document.createElement("p");
  city.innerHTML = `City: ${business.city}`;

  let state = document.createElement("p");
  state.innerHTML = `State: ${business.state}`;

  result.append(id, name, city, state);
  return result;
};

/**
 * Process and display the search results.
 * @param {Object} data JSON returned by the API containing many businesses.
 */
const populateResults = data => {
  const resultsDiv = document.getElementById("results");
  // clear results
  resultsDiv.innerHTML = "";
  // populate new results
  data.businesses.map(buildResultDOM).forEach(businessDiv => {
    resultsDiv.appendChild(businessDiv);
  });
};

/**
 * Debounce limits the rate that the function `func` can fire.
 * If multiple attempts to call func are made before `wait` ms have passed,
 * the wait timer is rest.
 * Source: underscore.js: https://underscorejs.org/#debounce */
const debounce = function(func, wait, immediate = false) {
  var timeout;
  return function() {
    var context = this,
      args = arguments;
    var later = function() {
      timeout = null;
      if (!immediate) {
        func.apply(context, args);
      }
    };
    var callNow = immediate && !timeout;
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    if (callNow) {
      func.apply(context, args);
    }
  };
};

const search = debounce(searchVal => {
  let url = new URL(SEARCH_ENDPOINT);
  const params = { search: searchVal };

  url.search = new URLSearchParams(params).toString();

  fetch(url, {
    method: "GET",
    crossDomain: true,
    cache: "no-cache"
  })
    .then(response => {
      if (response.ok) {
        return response.json();
      }
    })
    .then(responseJson => {
      populateResults(responseJson);
    })
    .catch(error => {
      console.error(error);
    });
}, 1000);

// On document.ready, add event listeners on input to trigger calls to API.
document.addEventListener("DOMContentLoaded", function() {
  let searchBar = document.getElementById("search-bar");
  searchBar.addEventListener("input", function() {
    if (searchBar.value) {
      search(searchBar.value);
    }
  });
});
