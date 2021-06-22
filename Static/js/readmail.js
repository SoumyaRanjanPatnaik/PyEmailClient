async function readmail(id){
	let pane = document.getElementById("readmail");
	pane.innerHTML = `<p style="text-align: center; color: red">LOADING...</p>`
	mail_data=await eel.get_mail_body(id)();

	subject = mail_data["headers"]["subject"];
	sender = mail_data["headers"]["from"];
	reciever = mail_data["headers"]["to"];
	body = mail_data["body"];

	from_html = "<h3 id = 'from'><strong>From: </strong>" +"<span>"+ sender+"</span>"+"</h3>";
	to_html = "<h3 id = 'to'><strong>To: </strong>" +"<span>"+ reciever+"</span>"+"</h3>";
	subject_html = "<h1 id = 'readmail-subject'><span>"+ subject+"</span>"+"</h1>";
	body_html = "<iframe id = 'mail-body'  srcdoc = '"+body+"'></iframe>";
	pane.innerHTML = subject_html+"<br>" + from_html + to_html +"<br><br>"+ body_html;
}