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
	 {text: '1集1-30',
	   handler: function(){go2("Ja1.htm")}},
	 {text: '　  31-60',
	   handler: function(){go2("Ja2.htm")}},
	 {text: '　  61-90',
	   handler: function(){go2("Ja3.htm")}},
	 {text: '　  91-120',
	   handler: function(){go2("Ja4.htm")}},
	 {text: '　 121-150',
	   handler: function(){go2("Ja5.htm")}},
	 {text: '2集151-170',
	   handler: function(){go2("Ja6.htm")}},
	 {text: '　 171-190',
	   handler: function(){go2("Ja7.htm")}},
	 {text: '　 191-210',
	   handler: function(){go2("Ja8.htm")}},
	 {text: '　 211-230',
	   handler: function(){go2("Ja9.htm")}},
	 {text: '　 231-250',
	   handler: function(){go2("Ja10.htm")}}
	             ]
	});

	var menu2 = new Ext.menu.Menu
	({id: 'mainMenu2',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '3集251-260',
	   handler: function(){go2("Ja11.htm")}},
	 {text: '　 261-270',
	   handler: function(){go2("Ja12.htm")}},
	 {text: '　 271-280',
	   handler: function(){go2("Ja13.htm")}},
	 {text: '　 281-290',
	   handler: function(){go2("Ja14.htm")}},
	 {text: '　 291-300',
	   handler: function(){go2("Ja15.htm")}},
	 {text: '4集301-310',
	   handler: function(){go2("Ja16.htm")}},
	 {text: '　 311-320',
	   handler: function(){go2("Ja17.htm")}},
	 {text: '　 321-330',
	   handler: function(){go2("Ja18.htm")}},
	 {text: '　 331-340',
	   handler: function(){go2("Ja19.htm")}},
	 {text: '　 341-350',
	   handler: function(){go2("Ja20.htm")}}
	             ]
	});

	var menu3 = new Ext.menu.Menu
	({id: 'mainMenu3',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '5集351-358',
	   handler: function(){go2("Ja21.htm")}},
	 {text: '　　359-366',
	   handler: function(){go2("Ja22.htm")}},
	 {text: '　　367-375',
	   handler: function(){go2("Ja23.htm")}},
	 {text: '6集376-380',
	   handler: function(){go2("Ja24.htm")}},
	 {text: '　　381-385',
	   handler: function(){go2("Ja25.htm")}},
	 {text: '　　386-390',
	   handler: function(){go2("Ja26.htm")}},
	 {text: '　　391-395',
	   handler: function(){go2("Ja27.htm")}},
	 {text: '7集396-400',
	   handler: function(){go2("Ja28.htm")}},
	 {text: '　　401-405',
	   handler: function(){go2("Ja29.htm")}},
	 {text: '　　406-410',
	   handler: function(){go2("Ja30.htm")}},
	 {text: '　　411-416',
	   handler: function(){go2("Ja31.htm")}}
	             ]
	});

	var menu4 = new Ext.menu.Menu
	({id: 'mainMenu4',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '8集417-421',
	   handler: function(){go2("Ja32.htm")}},
	 {text: '　　422-426',
	   handler: function(){go2("Ja33.htm")}},
	 {text: '9集427-430',
	   handler: function(){go2("Ja34.htm")}},
	 {text: '　　431-434',
	   handler: function(){go2("Ja35.htm")}},
	 {text: '　　435-438',
	   handler: function(){go2("Ja36.htm")}},
	 {text: '10集439-442',
	   handler: function(){go2("Ja37.htm")}},
	 {text: '　　443-446',
	   handler: function(){go2("Ja38.htm")}},
	 {text: '　　447-450',
	   handler: function(){go2("Ja39.htm")}},
	 {text: '　　451-454',
	   handler: function(){go2("Ja40.htm")}},
	 {text: '11集455-457',
	   handler: function(){go2("Ja41.htm")}},
	 {text: '　　458-460',
	   handler: function(){go2("Ja42.htm")}},
	 {text: '　　461-463',
	   handler: function(){go2("Ja43.htm")}}
	             ]
	});

	var menu5 = new Ext.menu.Menu
	({id: 'mainMenu5',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '12集464-465',
	   handler: function(){go2("Ja44.htm")}},
	 {text: '　　466-467',
	   handler: function(){go2("Ja45.htm")}},
	 {text: '　　468-469',
	   handler: function(){go2("Ja46.htm")}},
	 {text: '　　470-471',
	   handler: function(){go2("Ja47.htm")}},
	 {text: '　　472-473',
	   handler: function(){go2("Ja48.htm")}},
	 {text: '13集474-475',
	   handler: function(){go2("Ja49.htm")}},
	 {text: '　　476-477',
	   handler: function(){go2("Ja50.htm")}},
	 {text: '　　478-479',
	   handler: function(){go2("Ja51.htm")}},
	 {text: '　　480-481',
	   handler: function(){go2("Ja52.htm")}},
	 {text: '　　482-483',
	   handler: function(){go2("Ja53.htm")}}
	             ]
	});

	var menu6 = new Ext.menu.Menu
	({id: 'mainMenu6',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '484',
	   handler: function(){go2("Ja54.htm")}},
	 {text: '485',
	   handler: function(){go2("Ja55.htm")}},
	 {text: '486',
	   handler: function(){go2("Ja56.htm")}},
	 {text: '487',
	   handler: function(){go2("Ja57.htm")}},
	 {text: '488',
	   handler: function(){go2("Ja58.htm")}},
	 {text: '489',
	   handler: function(){go2("Ja59.htm")}},
	 {text: '490',
	   handler: function(){go2("Ja60.htm")}},
	 {text: '491',
	   handler: function(){go2("Ja61.htm")}},
	 {text: '492',
	   handler: function(){go2("Ja62.htm")}},
	 {text: '493',
	   handler: function(){go2("Ja63.htm")}},
	 {text: '494',
	   handler: function(){go2("Ja64.htm")}},
	 {text: '495',
	   handler: function(){go2("Ja65.htm")}},
	 {text: '496',
	   handler: function(){go2("Ja66.htm")}}
	             ]
	});

	var menu7 = new Ext.menu.Menu
	({id: 'mainMenu7',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '497',
	   handler: function(){go2("Ja67.htm")}},
	 {text: '498',
	   handler: function(){go2("Ja68.htm")}},
	 {text: '499',
	   handler: function(){go2("Ja69.htm")}},
	 {text: '500',
	   handler: function(){go2("Ja70.htm")}},
	 {text: '501',
	   handler: function(){go2("Ja71.htm")}},
	 {text: '502',
	   handler: function(){go2("Ja72.htm")}},
	 {text: '503',
	   handler: function(){go2("Ja73.htm")}},
	 {text: '504',
	   handler: function(){go2("Ja74.htm")}},
	 {text: '505',
	   handler: function(){go2("Ja75.htm")}},
	 {text: '506',
	   handler: function(){go2("Ja76.htm")}},
	 {text: '507',
	   handler: function(){go2("Ja77.htm")}},
	 {text: '508',
	   handler: function(){go2("Ja78.htm")}},
	 {text: '509',
	   handler: function(){go2("Ja79.htm")}},
	 {text: '510',
	   handler: function(){go2("Ja80.htm")}}
	             ]
	});

	var menu8 = new Ext.menu.Menu
	({id: 'mainMenu8',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '511',
	   handler: function(){go2("Ja81.htm")}},
	 {text: '512',
	   handler: function(){go2("Ja82.htm")}},
	 {text: '513',
	   handler: function(){go2("Ja83.htm")}},
	 {text: '514',
	   handler: function(){go2("Ja84.htm")}},
	 {text: '515',
	   handler: function(){go2("Ja85.htm")}},
	 {text: '516',
	   handler: function(){go2("Ja86.htm")}},
	 {text: '517',
	   handler: function(){go2("Ja87.htm")}},
	 {text: '518',
	   handler: function(){go2("Ja88.htm")}},
	 {text: '519',
	   handler: function(){go2("Ja89.htm")}},
	 {text: '520',
	   handler: function(){go2("Ja90.htm")}}
	             ]
	});

	var menu9 = new Ext.menu.Menu
	({id: 'mainMenu9',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '40集521',
	   handler: function(){go2("Ja91.htm")}},
	 {text: '　　522',
	   handler: function(){go2("Ja92.htm")}},
	 {text: '　　523',
	   handler: function(){go2("Ja93.htm")}},
	 {text: '　　524',
	   handler: function(){go2("Ja94.htm")}},
	 {text: '　　525',
	   handler: function(){go2("Ja95.htm")}},
	 {text: '50集526',
	   handler: function(){go2("Ja96.htm")}},
	 {text: '　　527',
	   handler: function(){go2("Ja97.htm")}},
	 {text: '　　528',
	   handler: function(){go2("Ja98.htm")}}
	             ]
	});

	var menu10 = new Ext.menu.Menu
	({id: 'mainMenu10',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '60集529',
	   handler: function(){go2("Ja99.htm")}},
	 {text: '　　530',
	   handler: function(){go2("Ja100.htm")}},
	 {text: '70集531',
	   handler: function(){go2("Ja101.htm")}},
	 {text: '　　532',
	   handler: function(){go2("Ja102.htm")}},
	 {text: '80集533',
	   handler: function(){go2("Ja103.htm")}},
	 {text: '　　534',
	   handler: function(){go2("Ja104.htm")}},
	 {text: '　　535',
	   handler: function(){go2("Ja105.htm")}},
	 {text: '　　536',
	   handler: function(){go2("Ja106.htm")}},
	 {text: '　　537',
	   handler: function(){go2("Ja107.htm")}}
	             ]
	});

	var menu11 = new Ext.menu.Menu
	({id: 'mainMenu11',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '538',
	   handler: function(){go2("Ja108.htm")}},
	 {text: '539',
	   handler: function(){go2("Ja109.htm")}},
	 {text: '540',
	   handler: function(){go2("Ja110.htm")}},
	 {text: '541',
	   handler: function(){go2("Ja111.htm")}},
	 {text: '542',
	   handler: function(){go2("Ja112.htm")}},
	 {text: '543',
	   handler: function(){go2("Ja113.htm")}},
	 {text: '544',
	   handler: function(){go2("Ja114.htm")}},
	 {text: '545',
	   handler: function(){go2("Ja115.htm")}},
	 {text: '546',
	   handler: function(){go2("Ja116.htm")}},
	 {text: ' 547',
	   handler: function(){go2("Ja117.htm")}}
	             ]
	});

// 主選單 : 2.橫式主選單 ------------------------------
	var tb = new Ext.Toolbar();
	tb.render('toolbar');
	tb.add(
	{text:'首　頁',
	handler: function(){go2("../index.htm")}},
	{text:'I.1集~',  menu: menu1}, // 下拉的選單
	{text:' 3集~',  menu: menu2}, // 下拉的選單
	{text:' 5集~',  menu: menu3}, // 下拉的選單
	{text:' 8集~',  menu: menu4}, // 下拉的選單
	{text:' 12集~',  menu: menu5}, // 下拉的選單
	{text:' 雜集',  menu: menu6}, // 下拉的選單
	{text:' 20集',  menu: menu7}, // 下拉的選單
	{text:' 30集',  menu: menu8}, // 下拉的選單
	{text:'II.40集~',  menu: menu9}, // 下拉的選單
	{text:' 60集~',  menu: menu10}, // 下拉的選單
	{text:' 大集',  menu: menu11}, // 下拉的選單
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
		if (myurl.match(/Ja(\d+)\.htm/) != null){var sutranum = myurl.replace(/^.*?(\d+)\.htm/i,"$1");}// 取出經號
		var pre_sutra = parseInt(sutranum,10) - 1; 
		// 前一經
		if(pre_sutra < 1){pre_sutra = 117;}
		pre_sutra = "Ja" + pre_sutra.toString() + ".htm";
		go2(pre_sutra);
	}
	function next_sutra() {
		var myurl=window.location.toString();
		if (myurl.match(/Ja(\d+)\.htm/) != null){var sutranum = myurl.replace(/^.*?(\d+)\.htm/i,"$1");}// 取出經號
		var next_sutra = parseInt(sutranum,10) + 1; 
		// 下一經
		if(next_sutra > 117) {next_sutra = 1;}
		next_sutra = "Ja" + next_sutra.toString() + ".htm";
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

	mycomp=mycomp.replace(/Cp.(\d+)/g, function(word,str1)
	{
		var mynum = "" + str1.toString();
		mynum = mynum.replace(/^.*(\d\d\d)/,"$1");
		mynum = '<a href="../Cp/Cp' + mynum + '.htm" target="xxx">Cp.' + str1.toString()+ '</a>';
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
