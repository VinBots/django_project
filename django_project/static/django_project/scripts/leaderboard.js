var tabs = document.querySelectorAll(".lboard_tabs ul li");
var level1 = document.querySelector(".level1");
var level2 = document.querySelector(".level2");
var level3 = document.querySelector(".level3");
var items = document.querySelectorAll(".lboard_item");

tabs.forEach(function(tab){
	tab.addEventListener("click", function(){
		var currenttab = tab.getAttribute("data-li");
		
		tabs.forEach(function(tab){
			tab.classList.remove("active");
		})

		tab.classList.add("active");

		items.forEach(function(item){
			item.style.display = "none";
		})

		if(currenttab == "level1"){
			level1.style.display = "block";
		}
		else if(currenttab == "level2"){
			level2.style.display = "block";
		}
		else if(currenttab == "level3"){
			level2.style.display = "block";
		}

	})
})