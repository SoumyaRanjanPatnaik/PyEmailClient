async function getlabels() {
    let labels = await eel.mail_labels()();
    for (let index = 0; index < labels.length; index++) {
        if (labels[index].type === 'user') {
            document.getElementById('label').innerHTML += "<li id='" + labels[index].id + "' onclick='load_label(this.id)'><a href = '#'><i class='fas fa-folder-open'></i><span>" + labels[index].name + "</span></a></li>"
        }
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
