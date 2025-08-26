document.querySelector("form").addEventListener("submit", function (event) {
  event.preventDefault();

  var email = document.getElementById("email").value;
  var senha = document.getElementById("senha").value;

  var formData = new FormData();
  formData.append("email", email);
  formData.append("senha", senha);
  fetch("/users/login", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (response.ok) {
        window.location.href = response.url;
      } else {
        throw new Error("Erro ao fazer login");
      }
    })
    .catch((error) => {
      console.error("Erro:", error);
    });
});