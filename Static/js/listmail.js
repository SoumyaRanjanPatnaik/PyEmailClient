async function listmail(){
	const ids = await eel.get_ids()();
	console.log(ids)
	let maillist = document.getElementById("maillist-ul");
	for (let index=0; index<ids.length; index++) {
		let header = await eel.get_mail_header(ids[index])();
		console.log(ids[index])
		maillist.innerHTML+="<li class='mail-prev' id='"+ids[index]+"'><h2 class='from'>"+header['from']+"</h2><h2 class='subject'>"+header['subject']+"</h2></li>"
	}
}

eel.expose(list_content);
function list_content(content){
	let maillist = document.getElementById("maillist-ul");
	maillist.innerHTML+=content;
}