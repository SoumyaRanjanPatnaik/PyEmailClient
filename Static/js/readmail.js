async function readmail(id){
	let pane = document.getElementById("readmail");
	mail_data=await eel.get_mail_body(id)();

	subject = mail_data["headers"]["subject"];
	sender = mail_data["headers"]["from"];
	reciever = mail_data["headers"]["to"];
	body = mail_data["body"];

	from_html = "<h3 id = 'from'><strong>From: </strong>" +"<span>"+ sender+"</span>"+"</h3>";
	to_html = "<h3 id = 'to'><strong>To: </strong>" +"<span>"+ reciever+"</span>"+"</h3>";
	subject_html = "<h3 id = 'to'><strong>Subject: </strong>" +"<span>"+ subject+"</span>"+"</h3>";
	body_html = "<iframe id = 'mail-body' style='display=block;' srcdoc = '"+body+"'></iframe>";
	
	pane.innerHTML = from_html + to_html +subject_html+"<br><br>"+ body_html;
}