var in_word_div = 0;	// 判斷滑鼠是不是在文字的範圍中
var in_note_div = 0;	// 判斷滑鼠是不是在註解視窗的範圍中, 當不在這二個範圍中時, 註解視窗就消失

function get_str_title()
{
	var str_title = '<div id="toolbar"></div>';
	return str_title;
}
function write_str_title()
{
	var str_title = get_str_title();
	document.write(str_title);
}
function draw_layout () 
{
	var str_title = get_str_title();
    Ext.onReady(function()
{
       Ext.state.Manager.setProvider(new Ext.state.CookieProvider());
       var viewport = new Ext.Viewport
(
{
            layout:'border',
               items:
[{
            region:'north',
               contentEl: 'north',
               autoScroll: true,
               collapsible: true,
                title: str_title,
                    split: true,
                    height: 80,
                    border: false,
                    minSize: 1,
                    maxSize: 500,
                    margins:'0 0 0 0'
 },
/* {
                   region:'south',
                    contentEl: 'south',
                    title:'<font color="#3366FF"><span style="font-size:16pt">註解</font>',
                    split: true,
                    autoScroll: true,
                    collapsible: true,
                    height: 180,
                    border: false,
                    minSize: 1,
                    maxSize: 1000,
                    margins:'0 0 0 0'
 }, */
 /*{
               region:'west',
                    contentEl: 'west',
                    title:'功能表',
                    split:true,
                    width: 50,
                    minSize: 50,
                    maxSize: 300,
                    collapsible: true,
                    margins:'0 0 0 0',
                    layout:'accordion',
                    layoutConfig:
{
                   animate:true
  }
 },
 
*/
{
                   region:'east',
                    contentEl: 'east',
                    title: '<font color="#3366FF"><span style="font-size:14pt">巴利語經文-tipitaka.org<font color="#CC3300">(點右端»隱藏本欄)</font></font>',
                    split: true,
                    collapsible: true,
                    autoScroll: true,
                    width: '50%',
                    border: false,
                    minSize: 1,
                    maxSize: 900,
                    layout:'fit',
                    margins:'0 0 0 0'
 },
{
                   region: 'center',
                    contentEl: 'center',
                    title: '<font color="#3366FF"><span style="font-size:14pt">譯　文(莊春江譯)</font>',
                    autoScroll: true,
                    collapsible: true,
                    width: '50%',
                    border: false,
                    layout:'fit',
                    margins:'0 0 0 0'
                }
             ]
         });
		
// 主選單 : 1. 下拉的選單-只要改 text 和 go2 的連結網址--------------
	var menu1 = new Ext.menu.Menu
	({id: 'mainMenu1',
	 style: {overflow: 'visible'}, // For the Combo popup
	 items: [
	 {text: '1.蛇經',
	   handler: function(){go2("Su1.htm")}},
	 {text: '2.達尼亞經',
	   handler: function(){go2("Su2.htm")}},
	 {text: '3.犀牛角經',
	   handler: function(){go2("Su3.htm")}},
	 {text: '4.耕田婆羅墮若經',
	   handler: function(){go2("Su4.htm")}},
	 {text: '5.純陀經',
	   handler: function(){go2("Su5.htm")}},
	 {text: '6.敗亡經',
	   handler: function(){go2("Su6.htm")}},
	 {text: '7.賤民經',
	   handler: function(){go2("Su7.htm")}},
	 {text: '8.慈經',
	   handler: function(){go2("Su8.htm")}},
	 {text: '9.喜馬拉雅山經',
	   handler: function(){go2("Su9.htm")}},
	 {text: '10.阿羅婆迦經',
	   handler: function(){go2("Su10.htm")}},
	 {text: '11.勝利經',
	   handler: function(){go2("Su11.htm")}},
	 {text: '12.牟尼經',
	   handler: function(){go2("Su12.htm")}}
	             ]
	});

	var menu2 = new Ext.menu.Menu
	({id: 'mainMenu2',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '13.寶經',
	   handler: function(){go2("Su13.htm")}},
	 {text: '14.惡臭經',
	   handler: function(){go2("Su14.htm")}},
	 {text: '15.慚經',
	   handler: function(){go2("Su15.htm")}},
	 {text: '16.吉祥經',
	   handler: function(){go2("Su16.htm")}},
	 {text: '17.針毛經',
	   handler: function(){go2("Su17.htm")}},
	 {text: '18.法行經',
	   handler: function(){go2("Su18.htm")}},
	 {text: '19.婆羅門法經',
	   handler: function(){go2("Su19.htm")}},
	 {text: '20.船經',
	   handler: function(){go2("Su20.htm")}},
	 {text: '21.什麼戒經',
	   handler: function(){go2("Su21.htm")}},
	 {text: '22.奮起經',
	   handler: function(){go2("Su22.htm")}},
	 {text: '23.羅侯羅經',
	   handler: function(){go2("Su23.htm")}},
	 {text: '24.尼拘律葛波經',
	   handler: function(){go2("Su24.htm")}},
	 {text: '25.正確遊行經',
	   handler: function(){go2("Su25.htm")}},
	 {text: '26.如法經',
	   handler: function(){go2("Su26.htm")}}
	             ]
	});

	var menu3 = new Ext.menu.Menu
	({id: 'mainMenu3',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '27.出家經',
	   handler: function(){go2("Su27.htm")}},
	 {text: '28.勤奮經',
	   handler: function(){go2("Su28.htm")}},
	 {text: '29.善說經',
	   handler: function(){go2("Su29.htm")}},
	 {text: '30.孫陀利葛經',
	   handler: function(){go2("Su30.htm")}},
	 {text: '31.摩伽經',
	   handler: function(){go2("Su31.htm")}},
	 {text: '32.色逼亞經',
	   handler: function(){go2("Su32.htm")}},
	 {text: '33.謝勒經',
	   handler: function(){go2("Su33.htm")}},
	 {text: '34.箭經',
	   handler: function(){go2("Su34.htm")}},
	 {text: '35.襪謝德經',
	   handler: function(){go2("Su35.htm")}},
	 {text: '36.瞿迦梨迦經',
	   handler: function(){go2("Su36.htm")}},
	 {text: '37.那拉葛經',
	   handler: function(){go2("Su37.htm")}},
	 {text: '38.二種隨看經',
	   handler: function(){go2("Su38.htm")}}
	             ]
	});

	var menu4 = new Ext.menu.Menu
	({id: 'mainMenu4',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '39.欲經',
	   handler: function(){go2("Su39.htm")}},
	 {text: '40.洞窟…經',
	   handler: function(){go2("Su40.htm")}},
	 {text: '41.邪惡…經',
	   handler: function(){go2("Su41.htm")}},
	 {text: '42.純淨…經',
	   handler: function(){go2("Su42.htm")}},
	 {text: '43.最高的…經',
	   handler: function(){go2("Su43.htm")}},
	 {text: '44.老經',
	   handler: function(){go2("Su44.htm")}},
	 {text: '45.低舍彌勒經',
	   handler: function(){go2("Su45.htm")}},
	 {text: '46.玻索勒經',
	   handler: function(){go2("Su46.htm")}},
	 {text: '47.馬更地亞經',
	   handler: function(){go2("Su47.htm")}},
	 {text: '48.在崩解前經',
	   handler: function(){go2("Su48htm")}},
	 {text: '49.爭吵爭辯經',
	   handler: function(){go2("Su49.htm")}},
	 {text: '50.配置小經',
	   handler: function(){go2("Su50.htm")}},
	 {text: '51.配置大經',
	   handler: function(){go2("Su51.htm")}},
	 {text: '52.迅速經',
	   handler: function(){go2("Su52.htm")}},
	 {text: '53.取棍棒者經',
	   handler: function(){go2("Su53.htm")}},
	 {text: '54.舍利弗經',
	   handler: function(){go2("Su54.htm")}}
	             ]
	});

	var menu5 = new Ext.menu.Menu
	({id: 'mainMenu5',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '55.序　偈',
	   handler: function(){go2("Su55.htm")}},
	 {text: '56.阿逸多',
	   handler: function(){go2("Su56.htm")}},
	 {text: '57.低舍彌勒',
	   handler: function(){go2("Su57.htm")}},
	 {text: '58.富樓那葛',
	   handler: function(){go2("Su58.htm")}},
	 {text: '59.彌勒固',
	   handler: function(){go2("Su59.htm")}},
	 {text: '60.都達葛',
	   handler: function(){go2("Su60.htm")}},
	 {text: '61.優帕夕哇',
	   handler: function(){go2("Su61.htm")}},
	 {text: '62.難陀',
	   handler: function(){go2("Su62.htm")}},
	 {text: '63.黑瑪葛',
	   handler: function(){go2("Su63.htm")}},
	 {text: '64.度跌亞',
	   handler: function(){go2("Su64.htm")}},
	 {text: '65.葛波',
	   handler: function(){go2("Su65.htm")}},
	 {text: '66.若度耿泥',
	   handler: function(){go2("Su66.htm")}},
	 {text: '67.玻多吳達',
	   handler: function(){go2("Su67.htm")}},
	 {text: '68.優陀亞',
	   handler: function(){go2("Su68.htm")}},
	 {text: '69.迫沙拉',
	   handler: function(){go2("Su69.htm")}},
	 {text: '70.莫額臘闍',
	   handler: function(){go2("Su70.htm")}},
	 {text: '71.賓其亞',
	   handler: function(){go2("Su71.htm")}},
	 {text: '72.稱讚偈',
	   handler: function(){go2("Su72.htm")}},
	 {text: '73.隨誦偈',
	   handler: function(){go2("Su73.htm")}}
	             ]
	});

// 主選單 : 2.橫式主選單 ------------------------------
	var tb = new Ext.Toolbar();
	tb.render('toolbar');
	tb.add(
	{text:'首　頁',
	handler: function(){go2("../index.htm")}},
	{text:'　 1.蛇品',  menu: menu1}, // 下拉的選單
	{text:'　 2.小品',  menu: menu2}, // 下拉的選單
	{text:'　 3.大品',  menu: menu3}, // 下拉的選單
	{text:'　 4.八偈品',  menu: menu4}, // 下拉的選單
	{text:'　 5.彼岸道品',  menu: menu5}, // 下拉的選單
	{text:'　上一經/',
	handler: function(){pre_sutra()}},
	{text:'下一經',
	handler: function(){next_sutra()}}
	);
	tb.doLayout();
	$("td.x-toolbar-left").attr("align","center");// 將主選單置中
	$("em.x-btn-arrow button").hover(function() {$(this).click()});// 滑鼠移到按鈕時, 自動按下去
	$("#center,#east,#north").hover(function() {hide_menu()});// 移到三個主視窗就隱藏選單
	$(document).mouseleave(function() {hide_menu()}); // 離開畫面就隱藏選單
// 隱藏選單
	function hide_menu()
	{$("div[id^='mainMenu']").hide();    // 全部下拉選單消失
	 $("div[id^='mainMenu']").prev().hide(); // 下拉選單的陰影也消失
	 $("table.x-btn.x-btn-menu-active").removeClass("x-btn-menu-active");} // 按鈕呈現"未按下"
	function go2(url) {window.location.href = url}
	function pre_sutra() {
		var myurl=window.location.toString();
		if (myurl.match(/Su(\d+)\.htm/) != null){var sutranum = myurl.replace(/^.*?(\d+)\.htm/i,"$1");}// 取出經號
		var pre_sutra = parseInt(sutranum,10) - 1; 
		// 前一經
		if(pre_sutra < 1){pre_sutra = 73;}
		pre_sutra = "Su" + pre_sutra.toString() + ".htm";
		go2(pre_sutra);
	}
	function next_sutra() {
		var myurl=window.location.toString();
		if (myurl.match(/Su(\d+)\.htm/) != null){var sutranum = myurl.replace(/^.*?(\d+)\.htm/i,"$1");}// 取出經號
		var next_sutra = parseInt(sutranum,10) + 1; 
		// 下一經
		if(next_sutra > 73) {next_sutra = 1;}
		next_sutra = "Su" + next_sutra.toString() + ".htm";
		go2(next_sutra);
	}
// 選單結束 ----------------------
    });
}
function do_some_thing () 
{
	$(document).ready(function()
{
	$('head').append('<meta http-equiv="expires" content="-1">');
//    	$("#east").html($("#center").html());
    	$("#notediv").mouseover(function(){ in_note_div = 1; });	// 記錄滑鼠移入註解視窗
    	$("#notediv").mouseout(function(){ in_note_div = 0; });		// 記錄滑鼠移開註解視窗
    	$("#east").mouseover(function(){ check_note_div(); });		// 處理滑鼠移到主視窗的文字時, 要檢查此時是不是要取消註解視窗
    	$("#center").mouseover(function(){ check_note_div(); });	// 處理滑鼠移到主視窗的文字時, 要檢查此時是不是要取消註解視窗
    	add_agama_link("#south");
    	add_agama_link("#center");
	});}

    	// 經號連結
function add_agama_link(obj_div)
{
	var mycomp = $(obj_div).html();
	mycomp=mycomp.replace(/SA\.(\d+)/g, function(word,str1)
	 {
		mynum = '<a href="../SA/dm.php?keyword=' +str1+'" target="xxx">SA.' + str1 + '</a>';
  		return mynum;
  	}
	);

	mycomp=mycomp.replace(/SN\.(\d+\.\d+)/g, function(word,str1)
	 {
		mynum = '<a href="../SN/sn.php?keyword=' +str1+'" target="xxx">SN.' + str1 + '</a>';
  		return mynum;
  	}
	);

	mycomp=mycomp.replace(/MA\.(\d+)/g, function(word,str1)
	 {
		mynum = '<a href="../MA/dm.php?keyword=' +str1+'" target="xxx">MA.' + str1 + '</a>';
  		return mynum;
  	}
	);

	mycomp=mycomp.replace(/MN\.(\d+)/g, function(word,str1)
	 {
		mynum = '<a href="../MN/dm.php?keyword=' +str1+'" target="xxx">MN.' + str1 + '</a>';
  		return mynum;
  	}
	);

	mycomp=mycomp.replace(/DA\.(\d+)/g, function(word,str1)
	 {
		mynum = '<a href="../DA/dm.php?keyword=' +str1+'" target="xxx">DA.' + str1 + '</a>';
  		return mynum;
  	}
	);

	mycomp=mycomp.replace(/DN\.(\d+)/g, function(word,str1)
	 {
		mynum = '<a href="../DN/dm.php?keyword=' +str1+'" target="xxx">DN.' + str1 + '</a>';
  		return mynum;
  	}
  	);

	mycomp=mycomp.replace(/Ud\.(\d+)/g, function(word,str1)
	 {
		mynum = '<a href="../Ud/dm.php?keyword=' +str1+'" target="xxx">Ud.' + str1 + '</a>';
  		return mynum;
  	}
  	);

	mycomp=mycomp.replace(/It\.(\d+)/g, function(word,str1)
	 {
		mynum = '<a href="../It/dm.php?keyword=' +str1+'" target="xxx">It.' + str1 + '</a>';
  		return mynum;
  	}
  	);

	mycomp=mycomp.replace(/Ni.(\d+)/g, function(word,str1)
	{
		var mynum = "" + str1.toString();
		mynum = mynum.replace(/^.*(\d\d\d)/,"$1");
		mynum = '<a href="../Ni/Ni' + mynum + '.htm" target="xxx">Ni.' + str1.toString()+ '</a>';
  		return mynum;
  	}
	);

	mycomp=mycomp.replace(/Khp.(\d+)/g, function(word,str1)
	{
		var mynum = "" + str1.toString();
		mynum = '<a href="../Kh/Kh' + mynum + '.htm" target="xxx">Khp.' + str1.toString()+ '</a>';
  		return mynum;
  	}
	);

	mycomp=mycomp.replace(/Dhp.(\d+)/g, function(word,str1)
	{
		var mynum = "" + str1.toString();
		mynum = mynum.replace(/^.*(\d\d\d)/,"$1");
		mynum = '<a href="../Dh/Dh' + mynum + '.htm" target="xxx">Dhp.' + str1.toString()+ '</a>';
  		return mynum;
  	}
	);

	mycomp=mycomp.replace(/Sn.(\d+)/g, function(word,str1)
	{
		var mynum = "" + str1.toString();
		mynum = mynum.replace(/^.*(\d\d\d)/,"$1");
		mynum = '<a href="../Su/Su' + mynum + '.htm" target="xxx">Sn.' + str1.toString()+ '</a>';
  		return mynum;
  	}
	);

	mycomp=mycomp.replace(/Thag.(\d+)/g, function(word,str1)
	{
		var mynum = "" + str1.toString();
		mynum = mynum.replace(/^.*(\d\d\d)/,"$1");
		mynum = '<a href="../Th/Th' + mynum + '.htm" target="xxx">Thag.' + str1.toString()+ '</a>';
  		return mynum;
  	}
	);

	mycomp=mycomp.replace(/Apn.(\d+)/g, function(word,str1)
	{
		var mynum = "" + str1.toString();
		mynum = mynum.replace(/^.*(\d\d\d)/,"$1");
		mynum = '<a href="../Ap/Ap' + mynum + '.htm" target="xxx">Apn.' + str1.toString()+ '</a>';
  		return mynum;
  	}
	);

	mycomp=mycomp.replace(/Mi.(\d+)/g, function(word,str1)
	{
		var mynum = "" + str1.toString();
		mynum = mynum.replace(/^.*(\d\d\d)/,"$1");
		mynum = '<a href="../Mi/Mi' + mynum + '.htm" target="xxx">Mi.' + str1.toString()+ '</a>';
  		return mynum;
  	}
	);

	mycomp=mycomp.replace(/Ps.(\d+)/g, function(word,str1)
	{
		var mynum = "" + str1.toString();
		mynum = mynum.replace(/^.*(\d\d\d)/,"$1");
		mynum = '<a href="../Ps/Ps' + mynum + '.htm" target="xxx">Ps.' + str1.toString()+ '</a>';
  		return mynum;
  	}
	);

	mycomp=mycomp.replace(/AA\.(\d+\.\d+)/g, function(word,str1)
	 {
		mynum = '<a href="../AA/dm.php?keyword=' +str1+'" target="xxx">AA.' + str1 + '</a>';
  		return mynum;
  	}
	);

	mycomp=mycomp.replace(/AN\.(\d+\.\d+)/g, function(word,str1)
	 {
		mynum = '<a href="../AN/an.php?keyword=' +str1+'" target="xxx">AN.' + str1 + '</a>';
  		return mynum;
  	}
	);
	$(obj_div).html(mycomp);
}

note_array = new Array();

// 滑鼠移到註解時要秀出註解視窗

function note(obj,num)
{
	show_note(obj,num,0);	// 表示是全面的註解
}

function local(obj,num)
{
	show_note(obj,num,1);	// 表示是單一檔案的註解
}

function show_note(obj,num,local)
{
	in_word_div = 1;				// 表示滑鼠進入 名相文字
	loading = "載入中...";		// 第一次載入時的呈現文字
	
	// 先指定滑鼠 onMouseOut 的行為, 讓視窗消失
	$(obj).mouseout(function(){
		in_word_div = 0;
	});
	
	// 用 Ajax 讀取資料
	$("#notediv").html(loading);
	
	// 如果是讀過的檔案, 由陣列讀取資料
	if(local == 0)
	{
		filenum = Math.floor(num/100);
		// 這是讀取全面的註解
		if(note_array[filenum])
		{
			$("#notediv").html(note_array[filenum]);
			str = "#notediv #div" + num;
			$("#notediv").html($(str).html());
		add_agama_link("#notediv");
		}
		else
		{
			str = "../note/note" + filenum + ".htm #div" + num;		
			$("#notediv").load(str,function(data){
				note_array[filenum] = data;		// 全部資料放在 note_array 陣列中
		add_agama_link("#notediv");
			});
		}
		//add_agama_link("#notediv");
	}
	else
	{
		// 這是讀取單一檔案的註解
		str = "#note" + num;
		$("#notediv").html($(str).html());
	}
	
	// 呈現並調整框的位置
	$("#notediv").show();
	
	// 找出文字的上一層是在左邊或右邊
	var $myparent = $("#ext-comp-1004");	// 預設是左邊
	if($(obj).parent().parent().attr('id') == "east")
	{
		$myparent = $("#ext-comp-1003");
	}
	
	$("#notediv").css("top", $(obj).position().top + $myparent.position().top + 53);
	$("#notediv").css("left", $(obj).position().left + $myparent.position().left);
	if($(obj).position().left + $myparent.position().left + $("#notediv").width() > $(window).width())
	{
		$("#notediv").css("left", $(window).width() - $("#notediv").width() - 40);
	}
	if($("#notediv").position().top + $("#notediv").height() + $myparent.position().top - $(window).scrollTop() - 80  > $(window).height())
	{
		$("#notediv").css("top", $(obj).position().top  + $myparent.position().top - $("#notediv").height() + 6);
	}
	if($("#notediv").position().top < $(window).scrollTop())
	{
		$("#notediv").css("top", $(obj).position().top + $myparent.position().top + 53);
	}
}


function check_note_div()
{
	if (in_word_div == 0 && in_note_div == 0)
	{
		$("#notediv").hide();
	}
	else
	{
		$("#notediv").show();
	}
}
