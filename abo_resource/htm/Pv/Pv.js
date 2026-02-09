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
	 {text: '1.如田',
	   handler: function(){go2("Pv1.htm")}},
	 {text: '2.豬嘴',
	   handler: function(){go2("Pv2.htm")}},
	 {text: '3.腐爛嘴',
	   handler: function(){go2("Pv3.htm")}},
	 {text: '4.麵粉娃娃',
	   handler: function(){go2("Pv4.htm")}},
	 {text: '5.牆外',
	   handler: function(){go2("Pv5.htm")}},
	 {text: '6.吃五子',
	   handler: function(){go2("Pv6.htm")}},
	 {text: '7.吃七子',
	   handler: function(){go2("Pv7.htm")}},
	 {text: '8.公牛',
	   handler: function(){go2("Pv8.htm")}},
	 {text: '9.大織匠',
	   handler: function(){go2("Pv9.htm")}},
	 {text: '10.光禿',
	   handler: function(){go2("Pv10.htm")}},
	 {text: '11.龍像',
	   handler: function(){go2("Pv11.htm")}},
	 {text: '12.蛇',
	   handler: function(){go2("Pv12.htm")}}
	             ]
	});

	var menu2 = new Ext.menu.Menu
	({id: 'mainMenu2',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '13.輪迴脫離者',
	   handler: function(){go2("Pv13.htm")}},
	 {text: '14.舍利弗上座母',
	   handler: function(){go2("Pv14.htm")}},
	 {text: '15.魅得',
	   handler: function(){go2("Pv15.htm")}},
	 {text: '16.難陀',
	   handler: function(){go2("Pv16.htm")}},
	 {text: '17.戴擦亮耳環者',
	   handler: function(){go2("Pv17.htm")}},
	 {text: '18.坎哈',
	   handler: function(){go2("Pv18.htm")}},
	 {text: '19.守財長者',
	   handler: function(){go2("Pv19.htm")}},
	 {text: '20.朱羅長者',
	   handler: function(){go2("Pv20.htm")}},
	 {text: '21.安古樂',
	   handler: function(){go2("Pv21.htm")}},
	 {text: '22.鬱多羅母',
	   handler: function(){go2("Pv22.htm")}},
	 {text: '23.線',
	   handler: function(){go2("Pv23.htm")}},
	 {text: '24.耳禿',
	   handler: function(){go2("Pv24.htm")}},
	 {text: '25.烏玻哩',
	   handler: function(){go2("Pv25.htm")}}
	             ]
	});

	var menu3 = new Ext.menu.Menu
	({id: 'mainMenu3',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '26.不裂開',
	   handler: function(){go2("Pv26.htm")}},
	 {text: '27.住沙那的上座',
	   handler: function(){go2("Pv27.htm")}},
	 {text: '28.車匠',
	   handler: function(){go2("Pv28.htm")}},
	 {text: '29.穀殼',
	   handler: function(){go2("Pv29.htm")}},
	 {text: '30.男童',
	   handler: function(){go2("Pv30.htm")}},
	 {text: '31.謝里尼',
	   handler: function(){go2("Pv31.htm")}},
	 {text: '32.捕鹿獵人',
	   handler: function(){go2("Pv32.htm")}},
	 {text: '33.捕鹿獵人2',
	   handler: function(){go2("Pv33.htm")}},
	 {text: '34.欺瞞的裁判官',
	   handler: function(){go2("Pv34.htm")}},
	 {text: '35.遺骨譭謗者',
	   handler: function(){go2("Pv35.htm")}}
	             ]
	});

	var menu4 = new Ext.menu.Menu
	({id: 'mainMenu4',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '36.蓭婆色葛樂',
	   handler: function(){go2("Pv36.htm")}},
	 {text: '37.謝力色葛',
	   handler: function(){go2("Pv37.htm")}},
	 {text: '38.難陀葛',
	   handler: function(){go2("Pv38.htm")}},
	 {text: '39.奎宿',
	   handler: function(){go2("Pv39.htm")}},
	 {text: '40.甘蔗',
	   handler: function(){go2("Pv40.htm")}},
	 {text: '41.少年',
	   handler: function(){go2("Pv41.htm")}},
	 {text: '42.王子',
	   handler: function(){go2("Pv42.htm")}},
	 {text: '43.食糞者',
	   handler: function(){go2("Pv43.htm")}},
	 {text: '44.食糞女',
	   handler: function(){go2("Pv44.htm")}},
	 {text: '45.眾',
	   handler: function(){go2("Pv45.htm")}},
	 {text: '46.華氏城',
	   handler: function(){go2("Pv46.htm")}},
	 {text: '47.芒果林',
	   handler: function(){go2("Pv47.htm")}},
	 {text: '48.車軸樹',
	   handler: function(){go2("Pv48.htm")}},
	 {text: '49.財物收集',
	   handler: function(){go2("Pv49.htm")}},
	 {text: '50.長者子',
	   handler: function(){go2("Pv50.htm")}},
	 {text: '51.六萬鎚',
	   handler: function(){go2("Pv51.htm")}}
	             ]
	});


// 主選單 : 2.橫式主選單 ------------------------------
	var tb = new Ext.Toolbar();
	tb.render('toolbar');
	tb.add(
	{text:'首　頁',
	handler: function(){go2("../index.htm")}},
	{text:'　 1.蛇品',  menu: menu1}, // 下拉的選單
	{text:'　 2.烏玻哩品',  menu: menu2}, // 下拉的選單
	{text:'　 3.小品',  menu: menu3}, // 下拉的選單
	{text:'　 4.大品',  menu: menu4}, // 下拉的選單
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
		if (myurl.match(/Pv(\d+)\.htm/) != null){var sutranum = myurl.replace(/^.*?(\d+)\.htm/i,"$1");}// 取出經號
		var pre_sutra = parseInt(sutranum,10) - 1; 
		// 前一經
		if(pre_sutra < 1){pre_sutra = 51;}
		pre_sutra = "Pv" + pre_sutra.toString() + ".htm";
		go2(pre_sutra);
	}
	function next_sutra() {
		var myurl=window.location.toString();
		if (myurl.match(/Pv(\d+)\.htm/) != null){var sutranum = myurl.replace(/^.*?(\d+)\.htm/i,"$1");}// 取出經號
		var next_sutra = parseInt(sutranum,10) + 1; 
		// 下一經
		if(next_sutra > 51) {next_sutra = 1;}
		next_sutra = "Pv" + next_sutra.toString() + ".htm";
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

	mycomp=mycomp.replace(/Thig.(\d+)/g, function(word,str1)
	{
		var mynum = "" + str1.toString();
		mynum = mynum.replace(/^.*(\d\d\d)/,"$1");
		mynum = '<a href="../Ti/Ti' + mynum + '.htm" target="xxx">Thig.' + str1.toString()+ '</a>';
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
