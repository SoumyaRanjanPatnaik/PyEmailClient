

async function theme(toggle=0){
	/*
	Funnction to load or toggle theme.

	PARAMS:
		toggle: function won't toggle theme (loads theme) if toggle =0, 
				and if toggle is 1.
	RETURNS: true
	*/
	let curr_theme_string=await eel.theme_read()();
	let curr_theme = JSON.parse(curr_theme_string)
	curr_theme.value=(curr_theme.value+toggle)%2;
	if (curr_theme.value==0){
		//Dark theme values
		document.documentElement.style.setProperty("--primary-color"," rgba(0, 0, 0, 0.96)")
		document.documentElement.style.setProperty("--secondary-color"," rgba(2, 150, 2, 0.986)")
		document.documentElement.style.setProperty("--ternary-color","rgb(46, 46, 46)")
		document.documentElement.style.setProperty("--accents-color"," #35ac1b")
		document.documentElement.style.setProperty("--text-color"," rgb(255, 255, 255)")
		document.documentElement.style.setProperty("--text-color-secondary"," rgb(189, 186, 186)")
		document.documentElement.style.setProperty("--form-bg-color"," rgba(26, 26, 26, 0.418)")
		document.documentElement.style.setProperty("--maillist-bg-color","rgb(14, 14, 14)")
		document.documentElement.style.setProperty("--maillist-box-shadow-color","rgb(0, 0, 0)")
		document.getElementById("search-now").src = "./img/Logos/search_light.png"
	}
	
	else{
		//Light Thmme values
		document.documentElement.style.setProperty("--primary-color"," rgb(250, 250, 250)")
		document.documentElement.style.setProperty("--secondary-color"," rgba(58, 173, 255, 0.774)")
		document.documentElement.style.setProperty("--ternary-color","rgb(233, 233, 233)")
		document.documentElement.style.setProperty("--accents-color"," rgb(139, 216, 255)")
		document.documentElement.style.setProperty("--text-color"," rgb(32, 32, 32)")
		document.documentElement.style.setProperty("--text-color-secondary"," rgb(71,71,71)")
		document.documentElement.style.setProperty("--form-bg-color"," rgba(0, 0, 0, 0.178)")
		document.documentElement.style.setProperty("--maillist-bg-color","rgb(248, 248, 248)")
		document.documentElement.style.setProperty("--maillist-box-shadow-color","rgb(240, 240, 240)")
		document.getElementById("search-now").src = "./img/Logos/search_dark.png"
	}
	curr_theme_string = JSON.stringify(curr_theme);
	eel.theme_write(curr_theme_string);
	return true;
}