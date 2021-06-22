let flag, reset, index, ids;

let maillist=document.getElementById("maillist-ul")

async function listmail(query=null){
	flag=true;
	index=0;
	if(query==null){
		ids = await eel.get_ids()();
	}
	else{
		ids = await eel.get_ids(query)();
		maillist.innerHTML=`<p style="text-align: center; color: red">Showing results for "${query}" </p>`;
	}
	if (ids.length==0){
		alert("No results found");
		
	}
	console.log(ids)
	append_list();
}

async function append_list(){

		let header = await eel.get_mail_header(ids[index])();
		console.log(ids[index])
		maillist.innerHTML+="<li class='mail-prev' id='"+ids[index]+"' onclick='javascript:readmail(this.id)'><h2 class='from'>"+header['from']+"</h2><h2 class='subject'>"+header['subject']+"</h2></li>"
		index++;
		reset = requestAnimationFrame(append_list);

} 

async function search(){
	let field = document.getElementById("search-field");
	let field_value = field.value;
	field.value="";
	listmail(field_value)();
	flag=false;
}

let search_bar = document.getElementById('search-bar');
function formsubmit_action(event){
	event.preventDefault()
	requestAnimationFrame(()=>{
		cancelAnimationFrame(reset);
		maillist.innerHTML=`<p style="text-align: center; color: red">LOADING...</p>`
	})
	search();
	return false;
}
search_bar.addEventListener('submit',formsubmit_action);