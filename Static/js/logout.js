document.getElementById('logout').addEventListener('click', logout);

async function logout(){
	logout_prompt = confirm ("Are you sure you want to logout?");
	if(logout_prompt){
		await eel.logout()();
		body = document.querySelector('body');
		body.style.alignItems = 'center';
		body.style.justifyContent = 'center';
		body.innerHTML= `You have been logged out</p>`;
		eel.terminate()
	}
		
}