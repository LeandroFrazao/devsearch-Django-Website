let form = document.getElementById("login-form");

form.addEventListener("submit", (e) => {
  e.preventDefault();
  console.log("Form was submitted");
  let formData = {
    username: form.username.value,
    password: form.password.value,
  };

  let URL = "http://127.0.0.1:8000/api/users/token/";

  fetch(URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Data:", data.access);
      if (data.access) {
        localStorage.setItem("token", data.access);
        window.location =
          "file:///E:/Projects/Udemy-Django-2021/Django-Website-2021/frontend/projects-list.html";
      } else {
        alert("Username OR password did not work");
      }
    });
});
