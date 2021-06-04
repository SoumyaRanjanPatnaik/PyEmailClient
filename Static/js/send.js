eel.expose(sendmail);
function sendmail(){
    let mail_id = document.getElementById("email").value
    let mail_subject = document.getElementById('subject').value
    let mail_content = document.getElementById('mail-content').value
    eel.send_mail(mail_id, mail_subject, mail_content);
    document.getElementById('compose-form').reset()
    toggle_compose();;
}

