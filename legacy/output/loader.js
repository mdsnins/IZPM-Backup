var member_dict =
{
 "장원영": 0,
 "미야와키 사쿠라": 1,
 "조유리": 2,
 "최예나": 3,
 "안유진": 4,
 "야부키 나코": 5,
 "권은비": 6,
 "강혜원": 7,
 "혼다 히토미": 8,
 "김채원": 9,
 "김민주": 10,
 "이채연": 11,
 
 0:"장원영",
 1:"미야와키 사쿠라",
 2:"조유리",
 3:"최예나",
 4:"안유진",
 5:"야부키 나코",
 6:"권은비",
 7:"강혜원",
 8:"혼다 히토미",
 9:"김채원",
 10:"김민주",
 11:"이채연"
}
var member_array = Array();

function add_card(i, mail)
{
	var value = `<div class="col-md-4"><div class="card mb-4 shadow-sm" data-mail-index="${i}" data-mail-id="${mail.id}"><div class="card-body"><div class="row">`+
			`<div class="col-4 d-flex justify-content-center align-items-center"><img class="img-profile" src="img/profile/${member_dict[mail.member]}.jpg" /></div>` +
			`<div class="col-7"><strong>${mail.subject}</strong><br/>${mail.preview} <span class="text-muted">...</span></div></div>` +
			`<div class="d-flex justify-content-end align-items-center label-time"><small class="text-muted">${mail.time}</small></div></div></div></div>`

	$("#list_mail").append(value);
}

function filter_member(mno = -1)
{
	if(mno == -1)
	{
		$("#list_mail").empty();
		for(i=0; i<pm_list.length; i++)
			add_card(i, pm_list[i]);
	}
	else 
	{
		$("#list_mail").empty();
		for(i=0; i<member_array[mno].length; i++)
		{
			add_card(member_array[mno][i], pm_list[member_array[mno][i]]);
		}
	}
	$(".card").click(function() {
		var mail = pm_list[parseInt($(this).data("mail-index"))];
		$("#modalMailView").text(mail.subject);
		$("#body_mail").attr("src", `mail/${mail.id}.html`);

		$("#view_mail").modal();
	});
	
}

$(function() {
	for(var i=0; i<12; i++)
		member_array.push(Array());

	$("#list_mail").empty();
	

	for(i=0; i<pm_list.length; i++)
	{
		if(member_dict[pm_list[i].member] != undefined)
			member_array[member_dict[pm_list[i].member]].push(i);
		
		add_card(i, pm_list[i]);
	
	}
	$(".card").click(function() {
		var mail = pm_list[parseInt($(this).data("mail-index"))];
		$("#modalMailView").text(mail.subject);
		$("#body_mail").attr("src", `mail/${mail.id}.html`);

		$("#view_mail").modal();
	});
	
	for(i=0; i<12; i++)
	{
		if(member_array[i].length > 0)
		{
			var str = `<li><a href="#" class="text-white" onclick="filter_member(${i});">${member_dict[i]}</a></li>`;
			$("#member_list").append(str);
		}	
	}
});

