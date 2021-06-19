let flag = true;
async function listmail(query=null){
	let maillist = document.getElementById("maillist-ul");
	let ids;
	flag=true;
	if(query==null){
		ids = await eel.get_ids()();
	}
	else{
		alert(query);
		ids = await eel.get_ids(query)();
		maillist.innerHTML="";

	}
	if (ids.length==0){
		alert("No results found");
		
	}
	console.log(ids)
	for (let index=0; index<ids.length; index++) {
		let header = await eel.get_mail_header(ids[index])();
		console.log(ids[index])
		maillist.innerHTML+="<li class='mail-prev' id='"+ids[index]+"' onclick='javascript:readmail()'><h2 class='from'>"+header['from']+"</h2><h2 class='subject'>"+header['subject']+"</h2></li>"
	}
}

async function search(){
	let field = document.getElementById("search-field");
	let field_value = field.value;
	field.value="";
	listmail(field_value)();
	flag=false;
}
