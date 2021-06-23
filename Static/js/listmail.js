let flag, reset, index, ids, name_to_show;

let maillist=document.getElementById("maillist-ul")

async function listmail(query=null, show_query=true, above_subject='from'){
	flag=true;
	index=0;
	if(query==null){
		ids = await eel.get_ids()();
	}
	else{
		ids = await eel.get_ids(query)();
		if(show_query){
			maillist.innerHTML=`<p style="text-align: center; color: red">Showing results for ${query} </p>`;
		}else if(query!='in:INBOX'){
			maillist.innerHTML=`<p style="text-align: center; color: red">${query} </p>`;
		}
		else{
			maillist.innerHTML="";
		}
	}
	if (ids.length==0){
		alert("No results found");
		
	}
	name_to_show = above_subject;
	console.log(ids)
	append_list();
}

async function append_list(){
	if(index>=ids.length){
		return;
	}
	let header = await eel.get_mail_header(ids[index])();
	console.log(ids[index])
	maillist.innerHTML+="<li class='mail-prev' id='"+ids[index]+"' onclick='mail_prev_focus(this.id); readmail(this.id)'><h2 class='from'>"+header[name_to_show]+"</h2><h2 class='subject'>"+header['subject']+"</h2></li>"
	index++;
	reset = requestAnimationFrame(append_list);

} 

async function search(){
	let field = document.getElementById("search-field");
	let field_value = field.value;
	field.value="";
	index=0;
	append_list();
	listmail(field_value)();
	flag=false;
}

function stop_maillist(){
	requestAnimationFrame(()=>{
		cancelAnimationFrame(reset);
		maillist.innerHTML=`<p style="text-align: center; color: red">LOADING...</p>`
	})
}

let search_bar = document.getElementById('search-bar');
function formsubmit_action(event){
	event.preventDefault()
	stop_maillist()
	search();
	return false;
}
search_bar.addEventListener('submit',formsubmit_action);

function mail_prev_focus(id){
	try{
		active_prev_id = document.getElementsByClassName('active-prev')[0].id;
		document.getElementById(active_prev_id).classList.remove('active-prev');
	}
	catch{}
	document.getElementById(id).classList.add('active-prev');
}