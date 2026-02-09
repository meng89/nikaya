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
	 {text: '1.椅子1',
	   handler: function(){go2("Vi1.htm")}},
	 {text: '2.椅子2',
	   handler: function(){go2("Vi2.htm")}},
	 {text: '3.椅子3',
	   handler: function(){go2("Vi3.htm")}},
	 {text: '4.椅子4',
	   handler: function(){go2("Vi4.htm")}},
	 {text: '5.象',
	   handler: function(){go2("Vi5.htm")}},
	 {text: '6.船1',
	   handler: function(){go2("Vi6.htm")}},
	 {text: '7.船2',
	   handler: function(){go2("Vi7.htm")}},
	 {text: '8.船3',
	   handler: function(){go2("Vi8.htm")}},
	 {text: '9.燈',
	   handler: function(){go2("Vi9.htm")}},
	 {text: '10.胡麻供養物',
	   handler: function(){go2("Vi10.htm")}},
	 {text: '11.對丈夫忠貞者1',
	   handler: function(){go2("Vi11.htm")}},
	 {text: '12.對丈夫忠貞者2',
	   handler: function(){go2("Vi12.htm")}},
	 {text: '13.媳婦1',
	   handler: function(){go2("Vi13.htm")}},
	 {text: '14.媳婦2',
	   handler: function(){go2("Vi14.htm")}},
	 {text: '15.鬱多羅',
	   handler: function(){go2("Vi15.htm")}},
	 {text: '16.吉瑞',
	   handler: function(){go2("Vi16.htm")}},
	 {text: '17.美髮師',
	   handler: function(){go2("Vi17.htm")}}
	             ]
	});

	var menu2 = new Ext.menu.Menu
	({id: 'mainMenu2',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '18.婢女',
	   handler: function(){go2("Vi18.htm")}},
	 {text: '19.勒枯麼',
	   handler: function(){go2("Vi19.htm")}},
	 {text: '20.飯汁女施主',
	   handler: function(){go2("Vi20.htm")}},
	 {text: '21.旃陀羅女',
	   handler: function(){go2("Vi21.htm")}},
	 {text: '22.賢女',
	   handler: function(){go2("Vi22.htm")}},
	 {text: '23.受那地那',
	   handler: function(){go2("Vi23.htm")}},
	 {text: '24.布薩女',
	   handler: function(){go2("Vi24.htm")}},
	 {text: '25.尼達',
	   handler: function(){go2("Vi25.htm")}},
	 {text: '26.蘇尼達',
	   handler: function(){go2("Vi26.htm")}},
	 {text: '27.施食女1',
	   handler: function(){go2("Vi27.htm")}},
	 {text: '28.施食女2',
	   handler: function(){go2("Vi28.htm")}}
	             ]
	});

	var menu3 = new Ext.menu.Menu
	({id: 'mainMenu3',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '29.出色',
	   handler: function(){go2("Vi29.htm")}},
	 {text: '30.施甘蔗女',
	   handler: function(){go2("Vi30.htm")}},
	 {text: '31.床座',
	   handler: function(){go2("Vi31.htm")}},
	 {text: '32.勒大',
	   handler: function(){go2("Vi32.htm")}},
	 {text: '33.估低勒',
	   handler: function(){go2("Vi33.htm")}},
	 {text: '34.閃耀',
	   handler: function(){go2("Vi34.htm")}},
	 {text: '35.貝色哇低',
	   handler: function(){go2("Vi35.htm")}},
	 {text: '36.麼里葛威',
	   handler: function(){go2("Vi36.htm")}},
	 {text: '37.大眼睛',
	   handler: function(){go2("Vi37.htm")}},
	 {text: '38.晝度樹',
	   handler: function(){go2("Vi38.htm")}}
	             ]
	});

	var menu4 = new Ext.menu.Menu
	({id: 'mainMenu4',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '39.深紅',
	   handler: function(){go2("Vi39.htm")}},
	 {text: '40.輝煌',
	   handler: function(){go2("Vi40.htm")}},
	 {text: '41.龍象',
	   handler: function(){go2("Vi41.htm")}},
	 {text: '42.阿羅麼',
	   handler: function(){go2("Vi42.htm")}},
	 {text: '43.施酸粥女',
	   handler: function(){go2("Vi43.htm")}},
	 {text: '44.住處',
	   handler: function(){go2("Vi44.htm")}},
	 {text: '45.四女子',
	   handler: function(){go2("Vi45.htm")}},
	 {text: '46.芒果樹',
	   handler: function(){go2("Vi46.htm")}},
	 {text: '47.黃色',
	   handler: function(){go2("Vi47.htm")}},
	 {text: '48.甘蔗',
	   handler: function(){go2("Vi48.htm")}},
	 {text: '49.禮拜',
	   handler: function(){go2("Vi49.htm")}},
	 {text: '50.樂朱馬勒',
	   handler: function(){go2("Vi50.htm")}}
	             ]
	});

	var menu5 = new Ext.menu.Menu
	({id: 'mainMenu5',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '51.青蛙天子',
	   handler: function(){go2("Vi51.htm")}},
	 {text: '52.奎宿',
	   handler: function(){go2("Vi52.htm")}},
	 {text: '53.車得學生婆羅門',
	   handler: function(){go2("Vi53.htm")}},
	 {text: '54.施蟹味者',
	   handler: function(){go2("Vi54.htm")}},
	 {text: '55.守門人',
	   handler: function(){go2("Vi55.htm")}},
	 {text: '56.應該被作的1',
	   handler: function(){go2("Vi56.htm")}},
	 {text: '57.應該被作的2',
	   handler: function(){go2("Vi57.htm")}},
	 {text: '58.針1',
	   handler: function(){go2("Vi58.htm")}},
	 {text: '59.針2',
	   handler: function(){go2("Vi59.htm")}},
	 {text: '60.龍象1',
	   handler: function(){go2("Vi60.htm")}},
	 {text: '61.龍象2',
	   handler: function(){go2("Vi61.htm")}},
	 {text: '62.龍象3',
	   handler: function(){go2("Vi62.htm")}},
	 {text: '63.車-小',
	   handler: function(){go2("Vi63.htm")}},
	 {text: '64.車-大',
	   handler: function(){go2("Vi64.htm")}}
	             ]
	});

	var menu6 = new Ext.menu.Menu
	({id: 'mainMenu6',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '65.在家者1',
	   handler: function(){go2("Vi65.htm")}},
	 {text: '66.在家者2',
	   handler: function(){go2("Vi66.htm")}},
	 {text: '67.施果實者',
	   handler: function(){go2("Vi67.htm")}},
	 {text: '68.施住房者1',
	   handler: function(){go2("Vi68.htm")}},
	 {text: '69.施住房者2',
	   handler: function(){go2("Vi69.htm")}},
	 {text: '70.施食物者',
	   handler: function(){go2("Vi70.htm")}},
	 {text: '71.大麥守護者',
	   handler: function(){go2("Vi71.htm")}},
	 {text: '72.戴耳環者1',
	   handler: function(){go2("Vi72.htm")}},
	 {text: '73.戴耳環者2',
	   handler: function(){go2("Vi73.htm")}},
	 {text: '74.波亞西',
	   handler: function(){go2("Vi74.htm")}}
	             ]
	});

	var menu7 = new Ext.menu.Menu
	({id: 'mainMenu7',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '75.雜蔓',
	   handler: function(){go2("Vi75.htm")}},
	 {text: '76.歡喜園',
	   handler: function(){go2("Vi76.htm")}},
	 {text: '77.寶石柱',
	   handler: function(){go2("Vi77.htm")}},
	 {text: '78.黃金',
	   handler: function(){go2("Vi78.htm")}},
	 {text: '79.芒果樹',
	   handler: function(){go2("Vi79.htm")}},
	 {text: '80.牧牛者',
	   handler: function(){go2("Vi80.htm")}},
	 {text: '81.坎達葛',
	   handler: function(){go2("Vi81.htm")}},
	 {text: '82.種種容色',
	   handler: function(){go2("Vi82.htm")}},
	 {text: '83.戴擦亮耳環者',
	   handler: function(){go2("Vi83.htm")}},
	 {text: '84.謝力色葛',
	   handler: function(){go2("Vi84.htm")}},
	 {text: '85.善置',
	   handler: function(){go2("Vi85.htm")}}
	             ]
	});


// 主選單 : 2.橫式主選單 ------------------------------
	var tb = new Ext.Toolbar();
	tb.render('toolbar');
	tb.add(
	{text:'首　頁',
	handler: function(){go2("../index.htm")}},
	{text:'女-1.椅子品',  menu: menu1}, // 下拉的選單
	{text:' 2.雜蔓品',  menu: menu2}, // 下拉的選單
	{text:' 3.晝度樹品',  menu: menu3}, // 下拉的選單
	{text:' 4.深紅品',  menu: menu4}, // 下拉的選單
	{text:' 男-5.車-大品',  menu: menu5}, // 下拉的選單
	{text:' 6.波亞西品',  menu: menu6}, // 下拉的選單
	{text:' 7.善置品',  menu: menu7}, // 下拉的選單
	{text:'　上則 /',
	handler: function(){pre_sutra()}},
	{text:'下則',
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
		if (myurl.match(/Vi(\d+)\.htm/) != null){var sutranum = myurl.replace(/^.*?(\d+)\.htm/i,"$1");}// 取出經號
		var pre_sutra = parseInt(sutranum,10) - 1; 
		// 前一經
		if(pre_sutra < 1){pre_sutra = 85;}
		pre_sutra = "Vi" + pre_sutra.toString() + ".htm";
		go2(pre_sutra);
	}
	function next_sutra() {
		var myurl=window.location.toString();
		if (myurl.match(/Vi(\d+)\.htm/) != null){var sutranum = myurl.replace(/^.*?(\d+)\.htm/i,"$1");}// 取出經號
		var next_sutra = parseInt(sutranum,10) + 1; 
		// 下一經
		if(next_sutra > 85) {next_sutra = 1;}
		next_sutra = "Vi" + next_sutra.toString() + ".htm";
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

	mycomp=mycomp.replace(/Vv.(\d+)/g, function(word,str1)
	{
		var mynum = "" + str1.toString();
		mynum = mynum.replace(/^.*(\d\d\d)/,"$1");
		mynum = '<a href="../Vi/Vi' + mynum + '.htm" target="xxx">Vv.' + str1.toString()+ '</a>';
  		return mynum;
  	}
	);

	mycomp=mycomp.replace(/Pv.(\d+)/g, function(word,str1)
	{
		var mynum = "" + str1.toString();
		mynum = mynum.replace(/^.*(\d\d\d)/,"$1");
		mynum = '<a href="../Pv/Pv' + mynum + '.htm" target="xxx">Pv.' + str1.toString()+ '</a>';
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
