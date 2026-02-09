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
	 {text: '第一品',
	   handler: function(){go2("Th1.htm")}},
	 {text: '第二品',
	   handler: function(){go2("Th2.htm")}},
	 {text: '第三品',
	   handler: function(){go2("Th3.htm")}},
	 {text: '第四品',
	   handler: function(){go2("Th4.htm")}},
	 {text: '第五品',
	   handler: function(){go2("Th5.htm")}},
	 {text: '第六品',
	   handler: function(){go2("Th6.htm")}},
	 {text: '第七品',
	   handler: function(){go2("Th7.htm")}},
	 {text: '第八品',
	   handler: function(){go2("Th8.htm")}},
	 {text: '第九品',
	   handler: function(){go2("Th9.htm")}},
	 {text: '第十品',
	   handler: function(){go2("Th10.htm")}},
	 {text: '第十一品',
	   handler: function(){go2("Th11.htm")}},
	 {text: '第十二品',
	   handler: function(){go2("Th12.htm")}}
	             ]
	});

	var menu2 = new Ext.menu.Menu
	({id: 'mainMenu2',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '第一品',
	   handler: function(){go2("Th13.htm")}},
	 {text: '第二品',
	   handler: function(){go2("Th14.htm")}},
	 {text: '第三品',
	   handler: function(){go2("Th15.htm")}},
	 {text: '第四品',
	   handler: function(){go2("Th16.htm")}},
	 {text: '第五品',
	   handler: function(){go2("Th17.htm")}}
	             ]
	});

	var menu3 = new Ext.menu.Menu
	({id: 'mainMenu3',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '1.安額尼葛婆羅墮若',
	   handler: function(){go2("Th18.htm")}},
	 {text: '2.帕者亞',
	   handler: function(){go2("Th19.htm")}},
	 {text: '3.巴古勒',
	   handler: function(){go2("Th20.htm")}},
	 {text: '4.達尼亞',
	   handler: function(){go2("Th21.htm")}},
	 {text: '5.象子',
	   handler: function(){go2("Th22.htm")}},
	 {text: '6.枯遮受逼得',
	   handler: function(){go2("Th23.htm")}},
	 {text: '7.防護',
	   handler: function(){go2("Th24.htm")}},
	 {text: '8.雨者',
	   handler: function(){go2("Th25.htm")}},
	 {text: '9.亞受遮',
	   handler: function(){go2("Th26.htm")}},
	 {text: '10.沙低麼低亞',
	   handler: function(){go2("Th27.htm")}},
	 {text: '11.優波離',
	   handler: function(){go2("Th28.htm")}},
	 {text: '12.鬱多羅-守護者',
	   handler: function(){go2("Th29.htm")}},
	 {text: '13.征服者',
	   handler: function(){go2("Th30.htm")}},
	 {text: '14.喬達摩',
	   handler: function(){go2("Th31.htm")}},
	 {text: '15.哈哩得',
	   handler: function(){go2("Th32.htm")}},
	 {text: '16.離垢者',
	   handler: function(){go2("Th33.htm")}}
	             ]
	});

	var menu4 = new Ext.menu.Menu
	({id: 'mainMenu4',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '1.那額色嗎勒',
	   handler: function(){go2("Th34.htm")}},
	 {text: '2.玻估',
	   handler: function(){go2("Th35.htm")}},
	 {text: '3.色逼亞',
	   handler: function(){go2("Th36.htm")}},
	 {text: '4.難達葛',
	   handler: function(){go2("Th37.htm")}},
	 {text: '5.曾布葛',
	   handler: function(){go2("Th38.htm")}},
	 {text: '6.謝那葛',
	   handler: function(){go2("Th39.htm")}},
	 {text: '7.生成者',
	   handler: function(){go2("Th40.htm")}},
	 {text: '8.羅侯羅',
	   handler: function(){go2("Th41.htm")}},
	 {text: '9.檀香',
	   handler: function(){go2("Th42.htm")}},
	 {text: '10.如法',
	   handler: function(){go2("Th43.htm")}},
	 {text: '11.色迫葛',
	   handler: function(){go2("Th44.htm")}},
	 {text: '12.喜悅者',
	   handler: function(){go2("Th45.htm")}}
	             ]
	});

	var menu5 = new Ext.menu.Menu
	({id: 'mainMenu5',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '1.王授',
	   handler: function(){go2("Th46.htm")}},
	 {text: '2.善生成者',
	   handler: function(){go2("Th47.htm")}},
	 {text: '3.其哩嗎難陀',
	   handler: function(){go2("Th48.htm")}},
	 {text: '4.善意者',
	   handler: function(){go2("Th49.htm")}},
	 {text: '5.增長者',
	   handler: function(){go2("Th50.htm")}},
	 {text: '6.那提迦葉',
	   handler: function(){go2("Th51.htm")}},
	 {text: '7.伽耶迦葉',
	   handler: function(){go2("Th52.htm")}},
	 {text: '8.穿樹皮衣者',
	   handler: function(){go2("Th53.htm")}},
	 {text: '9.勝鷹者',
	   handler: function(){go2("Th54.htm")}},
	 {text: '10.名聲授',
	   handler: function(){go2("Th55.htm")}},
	 {text: '11.受那勾里威色',
	   handler: function(){go2("Th56.htm")}},
	 {text: '12.憍尸迦',
	   handler: function(){go2("Th57.htm")}}
	             ]
	});

	var menu6 = new Ext.menu.Menu
	({id: 'mainMenu6',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '1.優樓頻羅迦葉',
	   handler: function(){go2("Th58.htm")}},
	 {text: '2.作醫治者',
	   handler: function(){go2("Th59.htm")}},
	 {text: '3.大龍',
	   handler: function(){go2("Th60.htm")}},
	 {text: '4.筏',
	   handler: function(){go2("Th61.htm")}},
	 {text: '5.瑪魯迦之子',
	   handler: function(){go2("Th62.htm")}},
	 {text: '6.色帕達色',
	   handler: function(){go2("Th63.htm")}},
	 {text: '7.葛低亞那',
	   handler: function(){go2("Th64.htm")}},
	 {text: '8.鹿網',
	   handler: function(){go2("Th65.htm")}},
	 {text: '9.輔相子戰勝者',
	   handler: function(){go2("Th66.htm")}},
	 {text: '10.善意者',
	   handler: function(){go2("Th67.htm")}},
	 {text: '11.已沐浴牟尼',
	   handler: function(){go2("Th68.htm")}},
	 {text: '12.梵授',
	   handler: function(){go2("Th69.htm")}},
	 {text: '13.吉祥醍醐',
	   handler: function(){go2("Th70.htm")}},
	 {text: '14.一切欲者',
	   handler: function(){go2("Th71.htm")}}
	             ]
	});

	var menu7 = new Ext.menu.Menu
	({id: 'mainMenu7',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '7集 1.美妙海',
	   handler: function(){go2("Th72.htm")}},
	 {text: '　　2.侏儒拔提亞',
	   handler: function(){go2("Th73.htm")}},
	 {text: '　　3.吉祥',
	   handler: function(){go2("Th74.htm")}},
	 {text: '　　4.屠狗者',
	   handler: function(){go2("Th75.htm")}},
	 {text: '　　5.折斷蘆葦',
	   handler: function(){go2("Th76.htm")}},
	 {text: '8集 1.大迦旃延',
	   handler: function(){go2("Th77.htm")}},
	 {text: '　　2.吉祥友',
	   handler: function(){go2("Th78.htm")}},
	 {text: '　　3.摩訶槃特',
	   handler: function(){go2("Th79.htm")}},
	 {text: '9集 1.生成者',
	   handler: function(){go2("Th80.htm")}},
	 {text: '10集1.葛優陀夷',
	   handler: function(){go2("Th81.htm")}},
	 {text: '　　 2.單獨住者',
	   handler: function(){go2("Th82.htm")}},
	 {text: '　　 3.大劫賓那',
	   handler: function(){go2("Th83.htm")}},
	 {text: '　　 4.朱利槃特',
	   handler: function(){go2("Th84.htm")}},
	 {text: '　　 5.葛波',
	   handler: function(){go2("Th85.htm")}},
	 {text: '　　 6.優波先那',
	   handler: function(){go2("Th86.htm")}},
	 {text: '　　 7.喬達摩',
	   handler: function(){go2("Th87.htm")}}
	             ]
	});

	var menu8 = new Ext.menu.Menu
	({id: 'mainMenu8',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '11集1.正義務',
	   handler: function(){go2("Th88.htm")}},
	 {text: '12集1.持戒者',
	   handler: function(){go2("Th89.htm")}},
	 {text: '　　 2.善引導者',
	   handler: function(){go2("Th90.htm")}},
	 {text: '13集1.受那勾哩威色',
	   handler: function(){go2("Th91.htm")}},
	 {text: '14集1.柯第勒瓦尼亞雷瓦達',
	   handler: function(){go2("Th92.htm")}},
	 {text: '　　 2.牛授',
	   handler: function(){go2("Th93.htm")}},
	 {text: '16集1.阿若憍陳如',
	   handler: function(){go2("Th94.htm")}},
	 {text: '　　 2.優陀夷',
	   handler: function(){go2("Th95.htm")}}
	             ]
	});

	var menu9 = new Ext.menu.Menu
	({id: 'mainMenu9',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '1.勝解者',
	   handler: function(){go2("Th96.htm")}},
	 {text: '2.播臘帕哩亞',
	   handler: function(){go2("Th97.htm")}},
	 {text: '3.油商',
	   handler: function(){go2("Th98.htm")}},
	 {text: '4.護國',
	   handler: function(){go2("Th99.htm")}},
	 {text: '5.瑪魯迦之子',
	   handler: function(){go2("Th100.htm")}},
	 {text: '6.謝勒',
	   handler: function(){go2("Th101.htm")}},
	 {text: '7.葛利鉤達之子拔提亞',
	   handler: function(){go2("Th102.htm")}},
	 {text: '8.鴦掘摩羅',
	   handler: function(){go2("Th103.htm")}},
	 {text: '9.阿那律',
	   handler: function(){go2("Th104.htm")}},
	 {text: '10.播臘玻哩亞',
	   handler: function(){go2("Th105.htm")}}
	             ]
	});

	var menu10 = new Ext.menu.Menu
	({id: 'mainMenu10',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '30集1.鬼宿',
	   handler: function(){go2("Th106.htm")}},
	 {text: '　　 2.舍利弗',
	   handler: function(){go2("Th107.htm")}},
	 {text: '　　 3.阿難',
	   handler: function(){go2("Th108.htm")}},
	 {text: '40集 1.大迦葉',
	   handler: function(){go2("Th109.htm")}},
	 {text: '50集 1.得勒晡得',
	   handler: function(){go2("Th110.htm")}},
	 {text: '60集 1.大目揵連',
	   handler: function(){go2("Th111.htm")}},
	 {text: ' 大 集 1.婆耆舍',
	   handler: function(){go2("Th112.htm")}}
	             ]
	});

// 主選單 : 2.橫式主選單 ------------------------------
	var tb = new Ext.Toolbar();
	tb.render('toolbar');
	tb.add(
	{text:'首　頁',
	handler: function(){go2("../index.htm")}},
	{text:'　1集',  menu: menu1}, // 下拉的選單
	{text:' 2集',  menu: menu2}, // 下拉的選單
	{text:' 3集',  menu: menu3}, // 下拉的選單
	{text:' 4集',  menu: menu4}, // 下拉的選單
	{text:' 5集',  menu: menu5}, // 下拉的選單
	{text:' 6集',  menu: menu6}, // 下拉的選單
	{text:' 7集~',  menu: menu7}, // 下拉的選單
	{text:' 11集~',  menu: menu8}, // 下拉的選單
	{text:' 20集',  menu: menu9}, // 下拉的選單
	{text:' 30集~',  menu: menu10}, // 下拉的選單
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
		if (myurl.match(/Th(\d+)\.htm/) != null){var sutranum = myurl.replace(/^.*?(\d+)\.htm/i,"$1");}// 取出經號
		var pre_sutra = parseInt(sutranum,10) - 1; 
		// 前一經
		if(pre_sutra < 1){pre_sutra = 112;}
		pre_sutra = "Th" + pre_sutra.toString() + ".htm";
		go2(pre_sutra);
	}
	function next_sutra() {
		var myurl=window.location.toString();
		if (myurl.match(/Th(\d+)\.htm/) != null){var sutranum = myurl.replace(/^.*?(\d+)\.htm/i,"$1");}// 取出經號
		var next_sutra = parseInt(sutranum,10) + 1; 
		// 下一經
		if(next_sutra > 112) {next_sutra = 1;}
		next_sutra = "Th" + next_sutra.toString() + ".htm";
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

	mycomp=mycomp.replace(/Jat\.(\d+)/g, function(word,str1)
	 {
		mynum = '<a href="../Ja/ja.php?keyword=' +str1+'" target="xxx">Jat.' + str1 + '</a>';
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
