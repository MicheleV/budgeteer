import React, { useState } from "react";
import ReactDOM, { render } from "react-dom";

const App = () => {
  const [state, setState] = useState("Fetch");

  return <button onClick={() => {
    setState("Fetched (or fetching...)");

    fetch('http://localhost:1337/api/expenses?category_id=1&format=json&huge_page=yes&start=2020-01-01&end=2020-12-31')
    .then(function(response) {
        // When the page is loaded convert it to text
        return response.text()
    })
    .then(function(html) {
        // Initialize the DOM parser
        console.log(html)
        var token = html.match(/csrfmiddlewaretoken.*/g)[0].replace('csrfmiddlewaretoken" value="','').slice(0,-2)
        return token
    })
    .then(function(token) {
          var data = {
            // csrfmiddlewaretoken: token,
            username: 'xxx',
            password: 'xxxx'
          }
          console.log(token)
          fetch('http://localhost:1337/accounts/login/', {
            method: 'POST',
            body: JSON.stringify(data),
            headers: { "X-CSRFToken": token },
            credentials: 'same-origin'
          })
          .then(data => {
            console.log(data); // JSON data parsed by `data.json()` call
          });

    })
    .catch(function(err) {  
        console.log('Failed to fetch page: ', err);  
    });

  }}>{state}</button>
};

ReactDOM.render(
  <App />,
  document.getElementById("root")
);