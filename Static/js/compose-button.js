let compose = document.getElementById('compose-icon');
let dialog = document.getElementById('compose-window');
let send = document.getElementById('send-mail');
let nav = document.getElementsByClassName('menu-bar')[0];

let wrapper = document.getElementsByClassName('wrapper')[0];

let curr = 0;
function  toggle_compose(){
    compose.style.transition='transform 0.3s ease-in-out'
    send.style.transition='transform 0.2s ease-in-out'
    if(curr===0){
        compose.style.transform='rotate(135deg)';
        send.style.transform='scale(1,1)';
        dialog.style.display='flex';
        dialog.style.zIndex='100000'
        nav.style.overflow='hidden';
        curr++;
        wrapper.style.display='block'
    }
    else{
        compose.style.transform='rotate(0deg)';
        send.style.transform='scale(0,0)';
        dialog.style.display='none';
        nav.style.overflow='auto';
        wrapper.style.display='none';
        curr--;
    }
}