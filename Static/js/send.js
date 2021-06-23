function sendmail() {
  let mail_id = document.getElementById("email");
  if (ValidateEmail(mail_id)) {
    let mail_subject = document.getElementById("compose-subject").value;
    let mail_content = document.getElementById("mail-content").value;
    eel.send_mail(mail_id.value, mail_subject, mail_content);
    document.getElementById("compose-form").reset();
    toggle_compose();
  }
}

function ValidateEmail(inputText) {
  var mailformat =
    /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
  if (inputText.value.match(mailformat)) {
    return true;
  } else {
    alert("You have entered an invalid email address!");
    inputText.focus();
    inputText.value="";
    return false;
  }
}
