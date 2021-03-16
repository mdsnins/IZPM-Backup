var member_array = Array();
var cur_pm_list = Array();
var cur_idx = 0;

function get_name(mno = -1, nullable = false, nullstring="") {
	if(mno != -1 && localStorage.getItem("cname" + mno) != null) {
		if(nullable && localStorage.getItem("cname" + mno) == localStorage.name)
			return nullstring;
		return localStorage.getItem("cname" + mno);	
	}
	else if(mno != -1 && localStorage.getItem("cname" + mno) == null && nullable)
		return nullstring;
	
	return localStorage.name;
}	

function set_name(mno = -1) {
	var name;
	if(mno == -1)
		name = prompt("기본 이름을 설정해주세요", get_name());
	else
		name = prompt(`(${member_dict[mno]}) 이름을 설정해주세요`, get_name(mno));

	if(name != null) {
		if(mno == -1)
			localStorage.name = name;
		else
			localStorage.setItem("cname" + mno, name);
		location.reload();
	}

}

function resolve_name(body, mno=-1, target_str = "&lt;위즈원&gt;") {
	var name = get_name(mno) || "WIZ*ONE";
	var chk = name[name.length - 1].charCodeAt(0) - 44032;
	var flag = true; //existence of the last part of Korean
	if(chk < 0 || 11171 < chk)
		flag = false;
	else if(chk % 28 == 0)
		flag = false;

	var target_len = target_str.length;
	var next_pos = target_str.length + 1;
	var t = -name.length;
	while((t = body.indexOf(target_str, t + name.length)) != -1) {
		try {
			if((body[t + target_len] == "이" || body[t + target_len] == "가") && body[t + next_pos] == " ")
				body = body.slice(0, t) + name + (flag ? "이" : "가") + body.slice(t + next_pos);
			else if((body[t + target_len] == "을" || body[t + target_len] == "를") && body[t + next_pos] == " ")
				body = body.slice(0, t) + name + (flag ? "을" : "를") + body.slice(t + next_pos);
			else if((body[t + target_len] == "은" || body[t + target_len] == "는") && body[t + next_pos] == " ")
				body = body.slice(0, t) + name + (flag ? "은" : "는") + body.slice(t + next_pos);	
			else
				body = body.slice(0,t) + name + body.slice(t + target_len);
		}
		catch {
			body = body.slice(0,t) + name + body.slice(t + target_len);
		}
	}
	return {body: body, last_match: t + name.length};
}

function add_card(i, mail)
{
	let t = resolve_name(mail.preview, member_dict[mail.member], "<위즈원>");
	mail.preview = t.body.substring(0, t.last_match);
	mail.preview += t.body.substring(t.last_match).replace(/<위즈원/g, "{{}}").replace(/<위즈/g, "{{}}").replace(/<위/g, "{{}}").replace("{{}}", get_name());
	var value = `<div class="col-md-4"><div class="card mb-4 shadow-sm" data-mail-index="${i}" data-mail-id="${mail.id}"><div class="card-body"><div class="row">`+
			`<div class="col-4 d-flex justify-content-center align-items-center"><img class="img-profile" src="img/profile/${member_dict[mail.member]}.jpg" /></div>` +
			`<div class="col-7"><strong>${mail.subject}</strong><br/>${mail.preview} <span class="text-muted">...</span></div></div>` +
			`<div class="d-flex justify-content-end align-items-center label-time"><small class="text-muted">${mail.time}</small></div></div></div></div>`

	$("#list_mail").append(value);
}

function filter_member(mno = -1)
{
	console.log("filter_member", mno);
	cur_pm_list =  [];
	cur_idx = 1;
	
	$("#list_mail").empty();

	if(mno == -1)
	{
		for(i=0; i<pm_list.length; i++)
			cur_pm_list.push(i)
	}
	else 
	{
		for(i=0; i<member_array[mno].length; i++)
			cur_pm_list.push(member_array[mno][i]);
			//add_card(member_array[mno][i], pm_list[member_array[mno][i]]);
	}

	for(i=0; i<cur_pm_list.length && i < 24; i++)
		add_card(cur_pm_list[i], pm_list[cur_pm_list[i]]);

	$("#navbarHeader").collapse("hide");
}

$(function() {
	if(localStorage.name == undefined)
		localStorage.name = "위즈원";
	
	for(var i=0; i<12; i++)
		member_array.push(Array());
	
	cur_idx = 1;
	uname = get_name();

	for(i=0; i<pm_list.length; i++)
	{
		if(member_dict[pm_list[i].member] == undefined || member_dict[pm_list[i].member] == -1)
			continue
		member_array[member_dict[pm_list[i].member]].push(i);
		cur_pm_list.push(i);	
	}

	for(i=0; i<pm_list.length && i < 24; i++)
		add_card(cur_pm_list[i], pm_list[cur_pm_list[i]]);

	for(i=0; i<12; i++)
	{
		if(member_array[i].length > 0)
		{
			var str = `<li><a href="#" class="text-white" onclick="filter_member(${i});">${member_dict[i]}</a></li>`;
			$("#member_list").append(str);
		}	
	}

	//Member name set
	$("#user_name").text(get_name());
	$("#change_name").click(function(){set_name()});
	
	for(i=0; i<12; i++) {
		$("#detail_name").append(`<div class="name-member col-xs-6 col-lg-4"><p class="text-muted">${member_dict[i]} : <a href="#" class="set-member-name text-muted" data-member="${i}">${get_name(i, true, "(설정)")}</a></p></div>`); 
	}

	$(".set-member-name").click(function() {
		set_name(parseInt($(this).data("member")));
	});

	//Dynamic onclick event binding
	$(document).on("click", ".card", function(e) {
		var mail = pm_list[parseInt($(this).data("mail-index"))];
		$("#modalMailView").text(mail.subject);
		$("#body_mail").attr("src", `mail/${mail.id}.html`);
		$("#body_mail").attr("data-member", member_dict[mail.member]);

		$("#view_mail").modal();
	});
	
	
	$("#body_mail").on("load", function() { 
		window.frames[0].document.body.innerHTML = resolve_name(window.frames[0].document.body.innerHTML, parseInt($("#body_mail").data("member"))).body;
	});
	// Infinite Scroll
	$(window).scroll(function() {
		if(cur_idx * 24 > cur_pm_list.length)
			return false;
		if($(window).scrollTop() + 10 < $(document).height() - $(window).height())
			return false;
		var threshold = ((cur_idx+1) * 24 < cur_pm_list.length) ? (cur_idx+1) * 24 : cur_pm_list.length;
		console.log(threshold);
		for(var i=cur_idx * 24; i < threshold; i++) {
			console.log("hello");
			add_card(cur_pm_list[i], pm_list[cur_pm_list[i]]);
		}

		cur_idx++;
	});

});