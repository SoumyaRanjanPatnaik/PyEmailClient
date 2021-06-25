// function ValidateEmail(inputText) {
//   var mailformat =
//     /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
//   if (inputText.value.match(mailformat)) {
//     alert("Valid email address!");
//     document.form1.text1.focus();
//     return true;
//   } else {
//     alert("You have entered an invalid email address!");
//     document.form1.text1.focus();
//     return false;
//   }
// }

function login() {
  eel.authenticate();
  let auth_begin = document.getElementById("auth-begin");

  window.open("./index.html", "_self");
}

eel.token_exists()(check);

function check(token){
  
  if (token == 'True'){
    let button = document.getElementById("button")
    let heading = document.getElementById("heading")
    heading.innerHTML = "You've Logged In Before"
    button.innerHTML="Continue to PyMail"
  }
}
