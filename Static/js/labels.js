async function getlabels(){
    let labels = await eel.mail_labels()();
    for (let index = 0; index < labels['imp'].length; index++) {
        if(labels['imp'][index]=='INBOX'){
            document.getElementById('label').innerHTML += "<li id='"+labels['imp'][index]+"' class='active' onclick=load_label('INBOX')><a href = '#'><span>"+labels['imp'][index]+"</span></a></li>"
            continue;
        }
        document.getElementById('label').innerHTML += "<li id='"+labels['imp'][index]+`' onclick='load_label(this.id)'><a href = '#'><span>`+labels['imp'][index]+"</span></a></li>"
    }
    if (labels['other'].length>0){
        document.getElementById('label').innerHTML += "<li id = 'other'><a href = '#'><span>Others</span></a><div class = 'sub-menu-2'><ul id = 'other_label'></ul></div></li>"
    }
    for (let index = 0; index < labels['other'].length; index++) {
        document.getElementById('other_label').innerHTML += "<li><a href = '#'>"+labels['other'][index]+"</a></li>"
    }
}

function load_label(id){
    stop_maillist();
    try{
        active_id=document.getElementsByClassName('active')[0].id;
        document.getElementById(active_id).classList.remove('active')
    }
    catch{}
    document.getElementById(id).classList.add('active');
    if(id=='SENT'){
        listmail(`in:${id}`, false, 'to')
    }
    else{
        listmail(`in:${id}`,false);
    }

}