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

async function list_content(query=null){
	let maillist = document.getElementById("maillist-ul");
	if(query!=null){
		maillist.innerHTML= await eel.maillist_html(query)();
	}
	else{

		maillist.innerHTML= await eel.maillist_html()();
	}
	console.log( maillist.innerHTML)
}