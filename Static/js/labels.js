async function getlabels(){
    let labels = await eel.mail_labels()();
    for (let index = 0; index < labels['imp'].length; index++) {
        if(labels['imp'][index]=='INBOX'){
            document.getElementById('label').innerHTML += "<li id="+labels['imp'][index]+" class='active'><a href = '#'><span>"+labels['imp'][index]+"</span></a></li>"
            continue;
        }
        document.getElementById('label').innerHTML += "<li id="+labels['imp'][index]+"><a href = '#'><span>"+labels['imp'][index]+"</span></a></li>"
    }
    if (labels['other'].length>0){
        document.getElementById('label').innerHTML += "<li><a href = '#'><span>Others</span></a><div class = 'sub-menu-1'><ul id = 'other_label'></ul></div></li>"
    }
    for (let index = 0; index < labels['other'].length; index++) {
        document.getElementById('other_label').innerHTML += "<li><a href = '#'>"+labels['other'][index]+"</a></li>"
    }
}
