var thesquare = "left1";
var side = "left";
var lefttotal = 0;
var righttotal = 0;
var curid = 0;
var curvalue = 0;
var curvaluen = 0;
var curvaluem = 0;

function choosePets(squareclicked, curside) {
	if (squareclicked.id.includes("right")) {
		side = "right";
	} else {
		side = "left";
	}
	var popup = document.getElementById("modalboom");
	popup.style.visibility = 'visible';
	thesquare = squareclicked;
}

function closePets() {
	var popup = document.getElementById("modalboom");
	popup.style.visibility = 'hidden';
}

function addPet(id, itemvalue, neonmagic) {
	thesquare.innerHTML = "<img id='" + thesquare.id + "img' src='images/" + id + ".png'><div id='" + thesquare.id + "extras' class='extras'>" + neonmagic + "</div>";
	movePlus();
	closePets();
	thesquare.setAttribute("onClick", "removePet(this, side, " + itemvalue + ")");
	if (side == "left") {
		lefttotal = lefttotal + itemvalue;
	} else {
		righttotal = righttotal + itemvalue;
	}
	updateResults();
}

function removePet(squareclicked, curside, itemvalue) {
	if (squareclicked.id.includes("right")) {
		side = "right";
	} else {
		side = "left";
	}
	thesquare = squareclicked;
	squareclicked.innerHTML = "<img id='" + thesquare.id + "img' src='images/blank.png'><div id='" + thesquare.id + "extras' class='extras'></div>";
	organizePets();
	if (side == "left") {
		lefttotal = lefttotal - itemvalue;
	} else {
		righttotal = righttotal - itemvalue;
	}
	updateResults();
}

function updateResults() {
	var leftresult = "";
	var rightresult = "";
	if (lefttotal > righttotal) {
		leftresult = "Lose";
		rightresult = "Win";
		document.getElementById("offer1bar").style.backgroundImage = "linear-gradient(#f0a3a3, #f42323)";
		document.getElementById("middleresult").style.backgroundColor = "#f0a3a3";
	} else if (righttotal > lefttotal) {
		leftresult = "Win";
		rightresult = "Lose";
		document.getElementById("offer1bar").style.backgroundImage = "linear-gradient(#59CF79, #30C357)";
		document.getElementById("middleresult").style.backgroundColor = "#59CF79";
	} else if (righttotal == 0 && lefttotal == 0) {
		leftresult = "Fair";
		rightresult = "";
		document.getElementById("offer1bar").style.backgroundImage = "linear-gradient(#BCB6B5, #DFDDDC)";
		document.getElementById("middleresult").style.backgroundColor = "";
	} else {
		leftresult = "Fair";
		rightresult = "Fair";
		document.getElementById("offer1bar").style.backgroundImage = "linear-gradient(#59CF79, #30C357)";
		document.getElementById("middleresult").style.backgroundColor = "#59CF79";
	}
	var thedifference = Math.abs(lefttotal - righttotal);
	var thetotal = lefttotal + righttotal;
	var bigorsmall = "";
	if (thedifference == 0) {
		bigorsmall = "";
	} else if (thedifference / thetotal < .15) {
		bigorsmall = "Small ";
	} else if (thedifference / thetotal > .49) {
		bigorsmall = "Big ";
	}
	document.getElementById("middleresult").innerHTML = bigorsmall + leftresult;
	document.getElementById("wflmsg2").innerHTML = "<div class='wrapper2'>" + bigorsmall + leftresult + "<br><img src='images/" + leftresult + ".png'></div>";
	if (thetotal > 0) {
		var leftwidth = (lefttotal / thetotal) * 100;
		var rightwidth = (righttotal / thetotal) * 100;
	} else {
		leftwidth = 50;
		rightwidth = 50;
	}
	document.getElementById("offer1bar").style.width = leftwidth + "%";
	document.getElementById("offer2bar").style.width = rightwidth + "%";
	if (document.getElementById("gaugefair").innerHTML == "Fair") {
		document.getElementById("gaugefair").innerHTML = "";
	}
}

function movePlus() {
	var i = 1;
	while (i < 10) {
		if (document.getElementById(side + i + "img").src.indexOf("images/blank.png") <= 0) {
			i++;
		} else {
			document.getElementById(side + i + "img").src = "images/add.png";
			document.getElementById(side + i).setAttribute("onClick", "choosePets(this, side)");
			i = 10;
		}
	}
}

function organizePets() {
	var i = 1;
	var j = 2;
	while (j < 10) {
		if (document.getElementById(side + i + "img").src.indexOf("images/blank.png") >= 0 && j < 10) {
			document.getElementById(side + i + "img").src = document.getElementById(side + j + "img").src;
			document.getElementById(side + i + "extras").innerHTML = document.getElementById(side + j + "extras").innerHTML;
			document.getElementById(side + i).setAttribute("onClick", document.getElementById(side + j).getAttribute("onClick"));
			document.getElementById(side + j + "img").src = "images/blank.png";
			document.getElementById(side + j + "extras").innerHTML = "";
			document.getElementById(side + j).setAttribute("onClick", "");
		}
		i++;
		j++;
	}
	if (document.getElementById(side + "8img").src.indexOf("images/blank.png") <= 0 && document.getElementById(side + "8img").src.indexOf("images/add.png") <= 0 && document.getElementById(side + "9img").src.indexOf("images/blank.png") >= 0) {
		document.getElementById(side + "9img").src = "http://adoptmetradingvalues.com/images/add.png";
		document.getElementById(side + "9").setAttribute("onClick", "choosePets(this, side)");
	}
}

function getNeonChoices(id, value, valuen, valuem) {
	var popup = document.getElementById("neonboom");
	popup.style.visibility = 'visible';
	curid = id;
	curvalue = value;
	curvaluen = valuen;
	curvaluem = valuem;
}

function closeNeonChooser() {
	var popup = document.getElementById("neonboom");
	popup.style.visibility = 'hidden';
}

function switchItems(itemtype) {
	document.getElementById("animalgrid").style.display = "none";
	document.getElementById("foodgrid").style.display = "none";
	document.getElementById("vehiclegrid").style.display = "none";
	document.getElementById("petweargrid").style.display = "none";
	document.getElementById("toygrid").style.display = "none";
	document.getElementById("giftgrid").style.display = "none";
	document.getElementById("strollergrid").style.display = "none";
	document.getElementById("othergrid").style.display = "none";
	if (itemtype == "food") {
		document.getElementById("foodgrid").style.display = "";
		var images = document.querySelectorAll("#foodgrid img");
		for (var i = 0; i < images.length; i++) {
			images[i].src = images[i].getAttribute('data-src');
		}
	} else if (itemtype == "vehicles") {
		document.getElementById("vehiclegrid").style.display = "";
		var images = document.querySelectorAll("#vehiclegrid img");
		for (var i = 0; i < images.length; i++) {
			images[i].src = images[i].getAttribute('data-src');
		}
	} else if (itemtype == "petwear") {
		document.getElementById("petweargrid").style.display = "";
		var images = document.querySelectorAll("#petweargrid img");
		for (var i = 0; i < images.length; i++) {
			images[i].src = images[i].getAttribute('data-src');
		}
	} else if (itemtype == "toys") {
		document.getElementById("toygrid").style.display = "";
		var images = document.querySelectorAll("#toygrid img");
		for (var i = 0; i < images.length; i++) {
			images[i].src = images[i].getAttribute('data-src');
		}
	} else if (itemtype == "gifts") {
		document.getElementById("giftgrid").style.display = "";
		var images = document.querySelectorAll("#giftgrid img");
		for (var i = 0; i < images.length; i++) {
			images[i].src = images[i].getAttribute('data-src');
		}
	} else if (itemtype == "strollers") {
		document.getElementById("strollergrid").style.display = "";
		var images = document.querySelectorAll("#strollergrid img");
		for (var i = 0; i < images.length; i++) {
			images[i].src = images[i].getAttribute('data-src');
		}
	} else if (itemtype == "pets") {
		document.getElementById("animalgrid").style.display = "";
	} else if (itemtype == "other") {
		document.getElementById("othergrid").style.display = "";
	}
}

function sendNeonChoices() {
	var neonmagic = "";
	if (document.getElementById("neontype").value == "Neon") {
		curvalue = curvaluen;
		neonmagic = neonmagic + "<span style='background-color:#8DD102; color:#ffffff; border-radius:50%; padding:2px 6px;'>N</span>";
	} else if (document.getElementById("neontype").value == "Mega Neon") {
		curvalue = curvaluem;
		neonmagic = neonmagic + "<span style='background-color:#873FD5; color:#ffffff; padding:2px 4px;'>M</span>";
	} else if (document.getElementById("Fly").checked == false && document.getElementById("Ride").checked == false && curvalue > 1500) {
		curvalue = curvalue * 1.18;
	}
	if (document.getElementById("Fly").checked == true) {
		curvalue = curvalue + 20;
		neonmagic = neonmagic + "<span style='background-color:#2F99CD; color:#ffffff; border-radius:50%; padding:2px 6px;'>F</span>";
	}
	if (document.getElementById("Ride").checked == true) {
		curvalue = curvalue + 15;
		neonmagic = neonmagic + "<span style='background-color:#EC2C79; color:#ffffff; border-radius:50%; padding:2px 6px;'>R</span>";
	}
	if (document.getElementById("FG").checked == true) {
		curvalue = curvalue + 15;
		neonmagic = neonmagic + "G";
	}
	addPet(curid, curvalue, neonmagic);
	closeNeonChooser();
	document.getElementById("Fly").checked = false;
	document.getElementById("Ride").checked = false;
	document.getElementById("FG").checked = false;
	document.getElementById("neontype").value = "Regular";
	document.getElementById('FG').style.display = '';
	document.getElementById('fgtext').style.display = '';
}
var audio1 = new Audio("yay.mp3");
var audio2 = new Audio("doh.mp3");

function playAudio() {
	if (lefttotal < righttotal) {
		audio1.currentTime = 0;
		audio1.play();
	} else if (lefttotal > righttotal) {
		audio2.currentTime = 0;
		audio2.play();
	} else {}
}

function searchitem() {
	var searchterm = document.getElementById("Search").value;
	for (let element of document.getElementsByClassName("grid-item-white")) {
		if (element.id.toLowerCase().indexOf(searchterm.toLowerCase()) == -1) {
			element.style.display = 'none';
		} else {
			element.style.display = '';
		}
	}
}