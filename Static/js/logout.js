document.getElementById('logout').addEventListener('click', logout);

async function logout(){
	await eel.logout()();
	body = document.body;
	body.display='flex';
	body.style.alignItems='center';
	document.body.innerHTML("<h1 style = 'background-color: var(--primary-color); color: var(--text-color);' >You Have Been Logged Out</h1>")
}