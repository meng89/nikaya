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
	   {text: '1.佛陀品',
	      menu: new Ext.menu.Menu({  // 子選單設定在這裡
	      items: [
	         {text: '1.佛', handler: function(){go2("Ap1.htm")}},
	         {text: '2.辟支佛', handler: function(){go2("Ap2.htm")}},
	         {text: '3- 1.舍利弗', handler: function(){go2("Ap3.htm")}},
	         {text: '3- 2.大目揵連', handler: function(){go2("Ap4.htm")}},
	         {text: '3- 3.大迦葉', handler: function(){go2("Ap5.htm")}},
	         {text: '3- 4.阿那律', handler: function(){go2("Ap6.htm")}},
	         {text: '3- 5.滿慈子', handler: function(){go2("Ap7.htm")}},
	         {text: '3- 6.優波離', handler: function(){go2("Ap8.htm")}},
	         {text: '3- 7.阿若憍陳如', handler: function(){go2("Ap9.htm")}},
	         {text: '3- 8.賓頭羅婆羅墮若', handler: function(){go2("Ap10.htm")}},
	         {text: '3- 9.柯第勒瓦尼亞雷瓦達', handler: function(){go2("Ap11.htm")}},
	         {text: '3-10.阿難', handler: function(){go2("Ap12.htm")}}
		]})},
	   {text: '2.獅子座品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.獅子座施與者', handler: function(){go2("Ap13.htm")}},
	         {text: '2.一柱者', handler: function(){go2("Ap14.htm")}},
	         {text: '3.難陀', handler: function(){go2("Ap15.htm")}},
	         {text: '4.朱利槃特', handler: function(){go2("Ap16.htm")}},
	         {text: '5.逼林達婆蹉', handler: function(){go2("Ap17.htm")}},
	         {text: '6.羅侯羅', handler: function(){go2("Ap18.htm")}},
	         {text: '7.優波先那', handler: function(){go2("Ap19.htm")}},
	         {text: '8.護國', handler: function(){go2("Ap20.htm")}},
	         {text: '9.屠狗者', handler: function(){go2("Ap21.htm")}},
	         {text: '10.善吉祥', handler: function(){go2("Ap22.htm")}}
		]})},
	 {text: '3.須菩提品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.須菩提', handler: function(){go2("Ap23.htm")}},
	         {text: '2.優波瓦那', handler: function(){go2("Ap24.htm")}},
	         {text: '3.三歸依者', handler: function(){go2("Ap25.htm")}},
	         {text: '4.受持五戒者', handler: function(){go2("Ap26.htm")}},
	         {text: '5.投入食物者', handler: function(){go2("Ap27.htm")}},
	         {text: '6.香施與者', handler: function(){go2("Ap28.htm")}},
	         {text: '7.沙供養者', handler: function(){go2("Ap29.htm")}},
	         {text: '8.鬱低雅', handler: function(){go2("Ap30.htm")}},
	         {text: '9.一合掌者', handler: function(){go2("Ap31.htm")}},
	         {text: '10.亞麻衣施與者', handler: function(){go2("Ap32.htm")}}
		]})},
	 {text: '4.古達達那品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.古達達那', handler: function(){go2("Ap33.htm")}},
	         {text: '2.善來', handler: function(){go2("Ap34.htm")}},
	         {text: '3.大迦旃延', handler: function(){go2("Ap35.htm")}},
	         {text: '4.黑優陀夷', handler: function(){go2("Ap36.htm")}},
	         {text: '5.空虛王', handler: function(){go2("Ap37.htm")}},
	         {text: '6.勝解者', handler: function(){go2("Ap38.htm")}},
	         {text: '7.大蒜施與者', handler: function(){go2("Ap39.htm")}},
	         {text: '8.供物施與者', handler: function(){go2("Ap40.htm")}},
	         {text: '9.法輪者', handler: function(){go2("Ap41.htm")}},
	         {text: '10.劫樹者', handler: function(){go2("Ap42.htm")}}
		]})},
	 {text: '5.優波離品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.優波離', handler: function(){go2("Ap43.htm")}},
	         {text: '2.受那勾哩威色', handler: function(){go2("Ap44.htm")}},
	         {text: '3.葛利鉤達之子拔提亞', handler: function(){go2("Ap45.htm")}},
	         {text: '4.散尼踏帕葛', handler: function(){go2("Ap46.htm")}},
	         {text: '5.五把者', handler: function(){go2("Ap47.htm")}},
	         {text: '6.紅蓮覆蓋物者', handler: function(){go2("Ap48.htm")}},
	         {text: '7.床施與者', handler: function(){go2("Ap49.htm")}},
	         {text: '8.經行處施與者', handler: function(){go2("Ap50.htm")}},
	         {text: '9.須跋陀', handler: function(){go2("Ap51.htm")}},
	         {text: '10.純陀', handler: function(){go2("Ap52.htm")}}
		]})},
	 {text: '6.扇子品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.扇子施與者', handler: function(){go2("Ap53.htm")}},
	         {text: '2.百束光芒', handler: function(){go2("Ap54.htm")}},
	         {text: '3.床施與者', handler: function(){go2("Ap55.htm")}},
	         {text: '4.香水者', handler: function(){go2("Ap56.htm")}},
	         {text: '5.可騎的', handler: function(){go2("Ap57.htm")}},
	         {text: '6.有隨從座位者', handler: function(){go2("Ap58.htm")}},
	         {text: '7.五燈者', handler: function(){go2("Ap59.htm")}},
	         {text: '8.旗施與者', handler: function(){go2("Ap60.htm")}},
	         {text: '9.紅蓮', handler: function(){go2("Ap61.htm")}},
	         {text: '10.欖仁菩提樹', handler: function(){go2("Ap62.htm")}}
		]})},
	 {text: '7.自思惟者品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.自思惟者', handler: function(){go2("Ap63.htm")}},
	         {text: '2.阿沃花者', handler: function(){go2("Ap64.htm")}},
	         {text: '3.回來者', handler: function(){go2("Ap65.htm")}},
	         {text: '4.他人使明淨者', handler: function(){go2("Ap66.htm")}},
	         {text: '5.蓮藕施與者', handler: function(){go2("Ap67.htm")}},
	         {text: '6.善思惟者', handler: function(){go2("Ap68.htm")}},
	         {text: '7.衣服施與者', handler: function(){go2("Ap69.htm")}},
	         {text: '8.芒果施與者', handler: function(){go2("Ap70.htm")}},
	         {text: '9.善意者', handler: function(){go2("Ap71.htm")}},
	         {text: '10.花籃者', handler: function(){go2("Ap72.htm")}}
		]})},
	 {text: '8.那額色嗎勒品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.那額色嗎勒', handler: function(){go2("Ap73.htm")}},
	         {text: '2.足想者', handler: function(){go2("Ap74.htm")}},
	         {text: '3.佛想者', handler: function(){go2("Ap75.htm")}},
	         {text: '4.蓮芋施與者', handler: function(){go2("Ap76.htm")}},
	         {text: '5.一想者', handler: function(){go2("Ap77.htm")}},
	         {text: '6.草墊施與者', handler: function(){go2("Ap78.htm")}},
	         {text: '7.針施與者', handler: function(){go2("Ap79.htm")}},
	         {text: '8.波吒梨花者', handler: function(){go2("Ap80.htm")}},
	         {text: '9.站立合掌者', handler: function(){go2("Ap81.htm")}},
	         {text: '10.三朵紅蓮者', handler: function(){go2("Ap82.htm")}}
		]})},
	 {text: '9.香合歡樹品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.香合歡樹花者', handler: function(){go2("Ap83.htm")}},
	         {text: '2.行去想者', handler: function(){go2("Ap84.htm")}},
	         {text: '3.躺臥合掌者', handler: function(){go2("Ap85.htm")}},
	         {text: '4.向下花者', handler: function(){go2("Ap86.htm")}},
	         {text: '5.光芒想者', handler: function(){go2("Ap87.htm")}},
	         {text: '6.第二光芒想者', handler: function(){go2("Ap88.htm")}},
	         {text: '7.果實施與者', handler: function(){go2("Ap89.htm")}},
	         {text: '8.聲想者', handler: function(){go2("Ap90.htm")}},
	         {text: '9.菩提樹澆水者', handler: function(){go2("Ap91.htm")}},
	         {text: '10.紅蓮花者', handler: function(){go2("Ap92.htm")}}
		]})},
	 {text: '10.泥灰品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.泥灰團者', handler: function(){go2("Ap93.htm")}},
	         {text: '2.善思惟者', handler: function(){go2("Ap94.htm")}},
	         {text: '3.半塊布者', handler: function(){go2("Ap95.htm")}},
	         {text: '4.針施與者', handler: function(){go2("Ap96.htm")}},
	         {text: '5.香花環者', handler: function(){go2("Ap97.htm")}},
	         {text: '6.三朵花者', handler: function(){go2("Ap98.htm")}},
	         {text: '7.蜜團者', handler: function(){go2("Ap99.htm")}},
	         {text: '8.臥坐處施與者', handler: function(){go2("Ap100.htm")}},
	         {text: '9.服侍者', handler: function(){go2("Ap101.htm")}},
	         {text: '10.佛侍者', handler: function(){go2("Ap102.htm")}}
		]})}
	             ]
	});

	var menu2 = new Ext.menu.Menu
	({id: 'mainMenu2',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '11.施食施與者品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.施食施與者', handler: function(){go2("Ap103.htm")}},
	         {text: '2.智想者', handler: function(){go2("Ap104.htm")}},
	         {text: '3.一把青蓮者', handler: function(){go2("Ap105.htm")}},
	         {text: '4.足供養者', handler: function(){go2("Ap106.htm")}},
	         {text: '5.一把花者', handler: function(){go2("Ap107.htm")}},
	         {text: '6.水供養者', handler: function(){go2("Ap108.htm")}},
	         {text: '7.蘆葦花環者', handler: function(){go2("Ap109.htm")}},
	         {text: '8.座位侍者', handler: function(){go2("Ap110.htm")}},
	         {text: '9.球根草施與者', handler: function(){go2("Ap111.htm")}},
	         {text: '10.花粉供養者', handler: function(){go2("Ap112.htm")}}
		]})},
	 {text: '12.大隨從品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.大隨從者', handler: function(){go2("Ap113.htm")}},
	         {text: '2.善吉祥者', handler: function(){go2("Ap114.htm")}},
	         {text: '3.歸依者', handler: function(){go2("Ap115.htm")}},
	         {text: '4.一座者', handler: function(){go2("Ap116.htm")}},
	         {text: '5.金色花者', handler: function(){go2("Ap117.htm")}},
	         {text: '6.火葬柴堆供養者', handler: function(){go2("Ap118.htm")}},
	         {text: '7.佛想者', handler: function(){go2("Ap119.htm")}},
	         {text: '8.道想者', handler: function(){go2("Ap120.htm")}},
	         {text: '9.現起想者', handler: function(){go2("Ap121.htm")}},
	         {text: '10.出生供養者', handler: function(){go2("Ap122.htm")}}
		]})},
	 {text: '13.假杜鵑品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.假杜鵑', handler: function(){go2("Ap123.htm")}},
	         {text: '2.花塔者', handler: function(){go2("Ap124.htm")}},
	         {text: '3.粥施與者', handler: function(){go2("Ap125.htm")}},
	         {text: '4.香水者', handler: function(){go2("Ap126.htm")}},
	         {text: '5.當面稱讚者', handler: function(){go2("Ap127.htm")}},
	         {text: '6.花座位者', handler: function(){go2("Ap128.htm")}},
	         {text: '7.果實施與者', handler: function(){go2("Ap129.htm")}},
	         {text: '8.智想者', handler: function(){go2("Ap130.htm")}},
	         {text: '9.結花者', handler: function(){go2("Ap131.htm")}},
	         {text: '10.紅蓮供養者', handler: function(){go2("Ap132.htm")}}
		]})},
	 {text: '14.輝耀者品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.輝耀者', handler: function(){go2("Ap133.htm")}},
	         {text: '2.善見', handler: function(){go2("Ap134.htm")}},
	         {text: '3.檀香供養者', handler: function(){go2("Ap135.htm")}},
	         {text: '4.花覆蓋物者', handler: function(){go2("Ap136.htm")}},
	         {text: '5.獨處想者', handler: function(){go2("Ap137.htm")}},
	         {text: '6.黃玉蘭樹花者', handler: function(){go2("Ap138.htm")}},
	         {text: '7.義理教示者', handler: function(){go2("Ap139.htm")}},
	         {text: '8.一淨信者', handler: function(){go2("Ap140.htm")}},
	         {text: '9.沙羅花施與者', handler: function(){go2("Ap141.htm")}},
	         {text: '10.豆腐果樹果實施與者', handler: function(){go2("Ap142.htm")}}
		]})},
	 {text: '15.傘品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.非凡傘者', handler: function(){go2("Ap143.htm")}},
	         {text: '2.柱豎起者', handler: function(){go2("Ap144.htm")}},
	         {text: '3.欄杆建造者', handler: function(){go2("Ap145.htm")}},
	         {text: '4.有隨眾者', handler: function(){go2("Ap146.htm")}},
	         {text: '5.亞麻花者', handler: function(){go2("Ap147.htm")}},
	         {text: '6.塗膏施與者', handler: function(){go2("Ap148.htm")}},
	         {text: '7.道路施與者', handler: function(){go2("Ap149.htm")}},
	         {text: '8.木板施與者', handler: function(){go2("Ap150.htm")}},
	         {text: '9.頭飾者', handler: function(){go2("Ap151.htm")}},
	         {text: '10.床座施與者', handler: function(){go2("Ap152.htm")}}
		]})},
	 {text: '16.朱槿品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.朱槿', handler: function(){go2("Ap153.htm")}},
	         {text: '2.赤銅花者', handler: function(){go2("Ap154.htm")}},
	         {text: '3.路徑打掃者', handler: function(){go2("Ap155.htm")}},
	         {text: '4.葫蘆花供養者', handler: function(){go2("Ap156.htm")}},
	         {text: '5.曼陀羅花供養者', handler: function(){go2("Ap157.htm")}},
	         {text: '6.迦蘭波樹花者', handler: function(){go2("Ap158.htm")}},
	         {text: '7.低那素勒茉莉者', handler: function(){go2("Ap159.htm")}},
	         {text: '8.鐵木樹花者', handler: function(){go2("Ap160.htm")}},
	         {text: '9.紅厚殼樹花者', handler: function(){go2("Ap161.htm")}},
	         {text: '10.黃蓮施與者', handler: function(){go2("Ap162.htm")}}
		]})},
	 {text: '17.善侍奉者品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.善侍奉者', handler: function(){go2("Ap163.htm")}},
	         {text: '2.夾竹桃花者', handler: function(){go2("Ap164.htm")}},
	         {text: '3.硬食施與者', handler: function(){go2("Ap165.htm")}},
	         {text: '4.地點供養者', handler: function(){go2("Ap166.htm")}},
	         {text: '5.翅子樹傘者', handler: function(){go2("Ap167.htm")}},
	         {text: '6.酥施與者', handler: function(){go2("Ap168.htm")}},
	         {text: '7.素馨花者', handler: function(){go2("Ap169.htm")}},
	         {text: '8.布施與者', handler: function(){go2("Ap170.htm")}},
	         {text: '9.勸導者', handler: function(){go2("Ap171.htm")}},
	         {text: '10.五指印者', handler: function(){go2("Ap172.htm")}}
		]})},
	 {text: '18.黃蓮品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.黃蓮花環者', handler: function(){go2("Ap173.htm")}},
	         {text: '2.梯子施與者', handler: function(){go2("Ap174.htm")}},
	         {text: '3.夜花者', handler: function(){go2("Ap175.htm")}},
	         {text: '4.水井施與者', handler: function(){go2("Ap176.htm")}},
	         {text: '5.獅子座施與者', handler: function(){go2("Ap177.htm")}},
	         {text: '6.道路施物者', handler: function(){go2("Ap178.htm")}},
	         {text: '7.一盞燈火者', handler: function(){go2("Ap179.htm")}},
	         {text: '8.寶珠供養者', handler: function(){go2("Ap180.htm")}},
	         {text: '9.醫師', handler: function(){go2("Ap181.htm")}},
	         {text: '10.僧團侍者', handler: function(){go2("Ap182.htm")}}
		]})},
	 {text: '19.止瀉木花者品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.止瀉木花者', handler: function(){go2("Ap183.htm")}},
	         {text: '2.朱槿', handler: function(){go2("Ap184.htm")}},
	         {text: '3.勾頓巴勒布', handler: function(){go2("Ap185.htm")}},
	         {text: '4.五手者', handler: function(){go2("Ap186.htm")}},
	         {text: '5.仙豆施與者', handler: function(){go2("Ap187.htm")}},
	         {text: '6.菩提樹侍者', handler: function(){go2("Ap188.htm")}},
	         {text: '7.一思惟者', handler: function(){go2("Ap189.htm")}},
	         {text: '8.低葛尼花者', handler: function(){go2("Ap190.htm")}},
	         {text: '9.一行者', handler: function(){go2("Ap191.htm")}},
	         {text: '10.三莖花者', handler: function(){go2("Ap192.htm")}}
		]})},
	 {text: '20.月桂樹花者品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.月桂樹花者', handler: function(){go2("Ap193.htm")}},
	         {text: '2.草敷床', handler: function(){go2("Ap194.htm")}},
	         {text: '3.破碎人者', handler: function(){go2("Ap195.htm")}},
	         {text: '4.無憂花供養者', handler: function(){go2("Ap196.htm")}},
	         {text: '5.六瓣八角楓者', handler: function(){go2("Ap197.htm")}},
	         {text: '6.嫩葉供養者', handler: function(){go2("Ap198.htm")}},
	         {text: '7.鎮頭迦施與者', handler: function(){go2("Ap199.htm")}},
	         {text: '8.一把供養者', handler: function(){go2("Ap200.htm")}},
	         {text: '9.小鈴花者', handler: function(){go2("Ap201.htm")}},
	         {text: '10.素馨花者', handler: function(){go2("Ap202.htm")}}
		]})}
	             ]
	});

	var menu3 = new Ext.menu.Menu
	({id: 'mainMenu3',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '21.翅子樹花者品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.翅子樹花者', handler: function(){go2("Ap203.htm")}},
	         {text: '2.咪內勒花者', handler: function(){go2("Ap204.htm")}},
	         {text: '3.小鈴花者', handler: function(){go2("Ap205.htm")}},
	         {text: '4.渡過者', handler: function(){go2("Ap206.htm")}},
	         {text: '5.黃荊樹花者', handler: function(){go2("Ap207.htm")}},
	         {text: '6.水施與者', handler: function(){go2("Ap208.htm")}},
	         {text: '7.乳香樹花環者', handler: function(){go2("Ap209.htm")}},
	         {text: '8.荊棘金樹花者', handler: function(){go2("Ap210.htm")}},
	         {text: '9.台子施與者', handler: function(){go2("Ap211.htm")}},
	         {text: '10.惡防止者', handler: function(){go2("Ap212.htm")}}
		]})},
	 {text: '22.象品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.象施與者', handler: function(){go2("Ap213.htm")}},
	         {text: '2.草鞋施與者', handler: function(){go2("Ap214.htm")}},
	         {text: '3.諦想者', handler: function(){go2("Ap215.htm")}},
	         {text: '4.一想者', handler: function(){go2("Ap216.htm")}},
	         {text: '5.光芒想者', handler: function(){go2("Ap217.htm")}},
	         {text: '6.連結者', handler: function(){go2("Ap218.htm")}},
	         {text: '7.棕櫚樹葉扇子施與者', handler: function(){go2("Ap219.htm")}},
	         {text: '8.走近想者', handler: function(){go2("Ap220.htm")}},
	         {text: '9.酥施與者', handler: function(){go2("Ap221.htm")}},
	         {text: '10.惡防止者', handler: function(){go2("Ap222.htm")}}
		]})},
	 {text: '23.支撐物施與者品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.支撐物施與者', handler: function(){go2("Ap223.htm")}},
	         {text: '2.羊皮施與者', handler: function(){go2("Ap224.htm")}},
	         {text: '3.二寶者', handler: function(){go2("Ap225.htm")}},
	         {text: '4.保護施與者', handler: function(){go2("Ap226.htm")}},
	         {text: '5.無病者', handler: function(){go2("Ap227.htm")}},
	         {text: '6.六瓣八角楓花者', handler: function(){go2("Ap228.htm")}},
	         {text: '7.黃金頭飾者', handler: function(){go2("Ap229.htm")}},
	         {text: '8.核頭飾者', handler: function(){go2("Ap230.htm")}},
	         {text: '9.善作包頭飾物者', handler: function(){go2("Ap231.htm")}},
	         {text: '10.一禮拜者', handler: function(){go2("Ap232.htm")}}
		]})},
	 {text: '24.水座品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.水座施與者', handler: function(){go2("Ap233.htm")}},
	         {text: '2.容器守護者', handler: function(){go2("Ap234.htm")}},
	         {text: '3.沙羅花者', handler: function(){go2("Ap235.htm")}},
	         {text: '4.蓆子施與者', handler: function(){go2("Ap236.htm")}},
	         {text: '5.欄杆建造者', handler: function(){go2("Ap237.htm")}},
	         {text: '6.美麗作者', handler: function(){go2("Ap238.htm")}},
	         {text: '7.豆腐果樹花者', handler: function(){go2("Ap239.htm")}},
	         {text: '8.芒果獻供施與者', handler: function(){go2("Ap240.htm")}},
	         {text: '9.基壇建造者', handler: function(){go2("Ap241.htm")}},
	         {text: '10.手斧施與者', handler: function(){go2("Ap242.htm")}}
		]})},
	 {text: '25.豆子施與者品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.豆子施與者', handler: function(){go2("Ap243.htm")}},
	         {text: '2.鐵木樹花絲者', handler: function(){go2("Ap244.htm")}},
	         {text: '3.蓮花池花絲者', handler: function(){go2("Ap245.htm")}},
	         {text: '4.鈴響花者', handler: function(){go2("Ap246.htm")}},
	         {text: '5.小屋熏香者', handler: function(){go2("Ap247.htm")}},
	         {text: '6.鉢施與者', handler: function(){go2("Ap248.htm")}},
	         {text: '7.遺骨供養者', handler: function(){go2("Ap249.htm")}},
	         {text: '8.車前草花供養者', handler: function(){go2("Ap250.htm")}},
	         {text: '9.紅莧樹者', handler: function(){go2("Ap251.htm")}},
	         {text: '10.阿勃勒施與者', handler: function(){go2("Ap252.htm")}}
		]})},
	 {text: '26.稱讚者品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.稱讚者', handler: function(){go2("Ap253.htm")}},
	         {text: '2.一座(食)施與者', handler: function(){go2("Ap254.htm")}},
	         {text: '3.火葬用柴堆供養者', handler: function(){go2("Ap255.htm")}},
	         {text: '4.三朵黃玉蘭樹花者', handler: function(){go2("Ap256.htm")}},
	         {text: '5.七朵波吒梨者', handler: function(){go2("Ap257.htm")}},
	         {text: '6.鞋施與者', handler: function(){go2("Ap258.htm")}},
	         {text: '7.新芽供養者', handler: function(){go2("Ap259.htm")}},
	         {text: '8.樹葉施與者', handler: function(){go2("Ap260.htm")}},
	         {text: '9.小屋施與者', handler: function(){go2("Ap261.htm")}},
	         {text: '10.第一朵花者', handler: function(){go2("Ap262.htm")}}
		]})},
	 {text: '27.蓮花拋起品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.拋向虛空者', handler: function(){go2("Ap263.htm")}},
	         {text: '2.塗油者', handler: function(){go2("Ap264.htm")}},
	         {text: '3.半月形[花]者', handler: function(){go2("Ap265.htm")}},
	         {text: '4.燈施與者', handler: function(){go2("Ap266.htm")}},
	         {text: '5.球根草施與者', handler: function(){go2("Ap267.htm")}},
	         {text: '6.魚施與者', handler: function(){go2("Ap268.htm")}},
	         {text: '7.快速鵝者', handler: function(){go2("Ap269.htm")}},
	         {text: '8.乳香樹花者', handler: function(){go2("Ap270.htm")}},
	         {text: '9.來到住所者', handler: function(){go2("Ap271.htm")}},
	         {text: '10.渡過者', handler: function(){go2("Ap272.htm")}}
		]})},
	 {text: '28.黃金枕頭品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.黃金枕頭者', handler: function(){go2("Ap273.htm")}},
	         {text: '2.一把芝麻施與者', handler: function(){go2("Ap274.htm")}},
	         {text: '3.花籃者', handler: function(){go2("Ap275.htm")}},
	         {text: '4.塗油施與者', handler: function(){go2("Ap276.htm")}},
	         {text: '5.一合掌者', handler: function(){go2("Ap277.htm")}},
	         {text: '6.塑料施與者', handler: function(){go2("Ap278.htm")}},
	         {text: '7.火葬用柴堆供養者', handler: function(){go2("Ap279.htm")}},
	         {text: '8.芋頭施與者', handler: function(){go2("Ap280.htm")}},
	         {text: '9.一白蓮', handler: function(){go2("Ap281.htm")}},
	         {text: '10.越度者', handler: function(){go2("Ap282.htm")}}
		]})},
	 {text: '29.樹葉施與者品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.樹葉施與者', handler: function(){go2("Ap283.htm")}},
	         {text: '2.果實施與者', handler: function(){go2("Ap284.htm")}},
	         {text: '3.迎接者', handler: function(){go2("Ap285.htm")}},
	         {text: '4.一朵花者', handler: function(){go2("Ap286.htm")}},
	         {text: '5.摩伽婆花者', handler: function(){go2("Ap287.htm")}},
	         {text: '6.侍奉施與者', handler: function(){go2("Ap288.htm")}},
	         {text: '7.阿波陀那者', handler: function(){go2("Ap289.htm")}},
	         {text: '8.七日出家者', handler: function(){go2("Ap290.htm")}},
	         {text: '9.佛侍者', handler: function(){go2("Ap291.htm")}},
	         {text: '10.先行者', handler: function(){go2("Ap292.htm")}}
		]})},
	 {text: '30.火葬用柴堆供養者品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.火葬用柴堆供養者', handler: function(){go2("Ap293.htm")}},
	         {text: '2.花戴上者', handler: function(){go2("Ap294.htm")}},
	         {text: '3.傘施與者', handler: function(){go2("Ap295.htm")}},
	         {text: '4.聲想者', handler: function(){go2("Ap296.htm")}},
	         {text: '5.牛頭放置者', handler: function(){go2("Ap297.htm")}},
	         {text: '6.腳供養者', handler: function(){go2("Ap298.htm")}},
	         {text: '7.地點宣說者', handler: function(){go2("Ap299.htm")}},
	         {text: '8.歸依者', handler: function(){go2("Ap300.htm")}},
	         {text: '9.芒果串者', handler: function(){go2("Ap301.htm")}},
	         {text: '10.隨投入者', handler: function(){go2("Ap302.htm")}}
		]})}
	             ]
	});

	var menu4 = new Ext.menu.Menu
	({id: 'mainMenu4',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '31.紅蓮花絲品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.紅蓮花絲者', handler: function(){go2("Ap303.htm")}},
	         {text: '2.一切香者', handler: function(){go2("Ap304.htm")}},
	         {text: '3.最好食物施與者', handler: function(){go2("Ap305.htm")}},
	         {text: '4.法想者', handler: function(){go2("Ap306.htm")}},
	         {text: '5.果實施與者', handler: function(){go2("Ap307.htm")}},
	         {text: '6.淨信者', handler: function(){go2("Ap308.htm")}},
	         {text: '7.園林施與者', handler: function(){go2("Ap309.htm")}},
	         {text: '8.塗膏施與者', handler: function(){go2("Ap310.htm")}},
	         {text: '9.佛想者', handler: function(){go2("Ap311.htm")}},
	         {text: '10.洞窟施與者', handler: function(){go2("Ap312.htm")}}
		]})},
	 {text: '32.守護施與品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.守護施與者', handler: function(){go2("Ap313.htm")}},
	         {text: '2.食物施與者', handler: function(){go2("Ap314.htm")}},
	         {text: '3.行去想者', handler: function(){go2("Ap315.htm")}},
	         {text: '4.七紅蓮者', handler: function(){go2("Ap316.htm")}},
	         {text: '5.花座施與者', handler: function(){go2("Ap317.htm")}},
	         {text: '6.座位{親交}[稱讚]者', handler: function(){go2("Ap318.htm")}},
	         {text: '7.聲想者', handler: function(){go2("Ap319.htm")}},
	         {text: '8.三種光芒者', handler: function(){go2("Ap320.htm")}},
	         {text: '9.康達利花者', handler: function(){go2("Ap321.htm")}},
	         {text: '10.黃蓮花環者', handler: function(){go2("Ap322.htm")}}
		]})},
	 {text: '33.亞麻花品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.亞麻花者', handler: function(){go2("Ap323.htm")}},
	         {text: '2.沙供養者', handler: function(){go2("Ap324.htm")}},
	         {text: '3.笑生出者', handler: function(){go2("Ap325.htm")}},
	         {text: '4.牲祭主人', handler: function(){go2("Ap326.htm")}},
	         {text: '5.相想者', handler: function(){go2("Ap327.htm")}},
	         {text: '6.食物投入者', handler: function(){go2("Ap328.htm")}},
	         {text: '7.黃荊樹花者', handler: function(){go2("Ap329.htm")}},
	         {text: '8.大花朵茉莉包頭飾物者', handler: function(){go2("Ap330.htm")}},
	         {text: '9.花傘者', handler: function(){go2("Ap331.htm")}},
	         {text: '10.有隨眾傘施與者', handler: function(){go2("Ap332.htm")}}
		]})},
	 {text: '34.香水品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.香熏香者', handler: function(){go2("Ap333.htm")}},
	         {text: '2.水供養者', handler: function(){go2("Ap334.htm")}},
	         {text: '3.紅厚殼樹花者', handler: function(){go2("Ap335.htm")}},
	         {text: '4.一塊布施與者', handler: function(){go2("Ap336.htm")}},
	         {text: '5.水滴搖動者', handler: function(){go2("Ap337.htm")}},
	         {text: '6.光明的作者', handler: function(){go2("Ap338.htm")}},
	         {text: '7.草屋施與者', handler: function(){go2("Ap339.htm")}},
	         {text: '8.上衣施與者', handler: function(){go2("Ap340.htm")}},
	         {text: '9.法聽聞者', handler: function(){go2("Ap341.htm")}},
	         {text: '10.拋紅蓮者', handler: function(){go2("Ap342.htm")}}
		]})},
	 {text: '35.一株紅蓮品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.一株紅蓮者', handler: function(){go2("Ap343.htm")}},
	         {text: '2.三株青蓮花環者', handler: function(){go2("Ap344.htm")}},
	         {text: '3.旗施與者', handler: function(){go2("Ap345.htm")}},
	         {text: '4.三朵小鈴供養者', handler: function(){go2("Ap346.htm")}},
	         {text: '5.蘆葦屋者', handler: function(){go2("Ap347.htm")}},
	         {text: '6.黃玉蘭樹花者', handler: function(){go2("Ap348.htm")}},
	         {text: '7.紅蓮供養者', handler: function(){go2("Ap349.htm")}},
	         {text: '8.一把草施與者', handler: function(){go2("Ap350.htm")}},
	         {text: '9.鎮頭迦果施與者', handler: function(){go2("Ap351.htm")}},
	         {text: '10.一合掌者', handler: function(){go2("Ap352.htm")}}
		]})},
	 {text: '36.聲想品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.聲想者', handler: function(){go2("Ap353.htm")}},
	         {text: '2.麥束者', handler: function(){go2("Ap354.htm")}},
	         {text: '3.緊叔迦供養者', handler: function(){go2("Ap355.htm")}},
	         {text: '4.有鞘的荊棘金樹施與者', handler: function(){go2("Ap356.htm")}},
	         {text: '5.拐杖施與者', handler: function(){go2("Ap357.htm")}},
	         {text: '6.芒果粥施與者', handler: function(){go2("Ap358.htm")}},
	         {text: '7.好袋子施與者', handler: function(){go2("Ap359.htm")}},
	         {text: '8.床施與者', handler: function(){go2("Ap360.htm")}},
	         {text: '9.歸依者', handler: function(){go2("Ap361.htm")}},
	         {text: '10.鉢食者', handler: function(){go2("Ap362.htm")}}
		]})},
	 {text: '37.曼陀羅花者品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.曼陀羅花者', handler: function(){go2("Ap363.htm")}},
	         {text: '2.葫蘆花者', handler: function(){go2("Ap364.htm")}},
	         {text: '3.蓮莖施與者', handler: function(){go2("Ap365.htm")}},
	         {text: '4.花絲花者', handler: function(){go2("Ap366.htm")}},
	         {text: '5.六瓣八角楓花者', handler: function(){go2("Ap367.htm")}},
	         {text: '6.迦蘭波樹花者', handler: function(){go2("Ap368.htm")}},
	         {text: '7.阿勃勒樹花者', handler: function(){go2("Ap369.htm")}},
	         {text: '8.一朵黃玉蘭樹花者', handler: function(){go2("Ap370.htm")}},
	         {text: '9.香合歡樹花者', handler: function(){go2("Ap371.htm")}},
	         {text: '10.乳香樹花者', handler: function(){go2("Ap372.htm")}}
		]})},
	 {text: '38.菩提樹禮拜品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.菩提樹禮拜者', handler: function(){go2("Ap373.htm")}},
	         {text: '2.波吒釐樹花者', handler: function(){go2("Ap374.htm")}},
	         {text: '3.三株青蓮花環者', handler: function(){go2("Ap375.htm")}},
	         {text: '4.黃葛樹花者', handler: function(){go2("Ap376.htm")}},
	         {text: '5.黑板樹者', handler: function(){go2("Ap377.htm")}},
	         {text: '6.一把香料者', handler: function(){go2("Ap378.htm")}},
	         {text: '7.火葬用柴堆供養者', handler: function(){go2("Ap379.htm")}},
	         {text: '8.大花朵茉莉棕櫚樹葉扇子者', handler: function(){go2("Ap380.htm")}},
	         {text: '9.大花朵茉莉花串者', handler: function(){go2("Ap381.htm")}},
	         {text: '10.無患子樹果實施與者', handler: function(){go2("Ap382.htm")}}
		]})},
	 {text: '39.阿哇得樹果實品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.阿哇得樹果實施與者', handler: function(){go2("Ap383.htm")}},
	         {text: '2.麵包樹施與者', handler: function(){go2("Ap384.htm")}},
	         {text: '3.聚果榕樹果實施與者', handler: function(){go2("Ap385.htm")}},
	         {text: '4.黃葛樹果實施與者', handler: function(){go2("Ap386.htm")}},
	         {text: '5.三色花樹果實施與者', handler: function(){go2("Ap387.htm")}},
	         {text: '6.葛藤果實施與者', handler: function(){go2("Ap388.htm")}},
	         {text: '7.芭蕉樹果實施與者', handler: function(){go2("Ap389.htm")}},
	         {text: '8.波羅蜜樹果實施與者', handler: function(){go2("Ap390.htm")}},
	         {text: '9.受那勾里威色', handler: function(){go2("Ap391.htm")}},
	         {text: '10.前業碎片片段', handler: function(){go2("Ap392.htm")}}
		]})},
	 {text: '40.逼林達婆蹉品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.逼林達婆蹉', handler: function(){go2("Ap393.htm")}},
	         {text: '2.謝勒', handler: function(){go2("Ap394.htm")}},
	         {text: '3.一切稱譽者', handler: function(){go2("Ap395.htm")}},
	         {text: '4.蜜施與者', handler: function(){go2("Ap396.htm")}},
	         {text: '5.紅蓮重閣者', handler: function(){go2("Ap397.htm")}},
	         {text: '6.巴古勒', handler: function(){go2("Ap398.htm")}},
	         {text: '7.其哩嗎難陀', handler: function(){go2("Ap399.htm")}},
	         {text: '8.乳香樹帳棚者', handler: function(){go2("Ap400.htm")}},
	         {text: '9.一切施與者', handler: function(){go2("Ap401.htm")}},
	         {text: '10.阿逸多', handler: function(){go2("Ap402.htm")}}
		]})},
	 {text: '41.彌勒品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.低舍彌勒', handler: function(){go2("Ap403.htm")}},
	         {text: '2.富樓那葛', handler: function(){go2("Ap404.htm")}},
	         {text: '3.彌勒固', handler: function(){go2("Ap405.htm")}},
	         {text: '4.都達葛', handler: function(){go2("Ap406.htm")}},
	         {text: '5.優帕夕哇', handler: function(){go2("Ap407.htm")}},
	         {text: '6.難陀葛', handler: function(){go2("Ap408.htm")}},
	         {text: '7.黑瑪葛', handler: function(){go2("Ap409.htm")}},
	         {text: '8.度跌亞', handler: function(){go2("Ap410.htm")}},
	         {text: '9.若度耿泥', handler: function(){go2("Ap411.htm")}},
	         {text: '10.優跌那', handler: function(){go2("Ap412.htm")}}
		]})},
	 {text: '42.跋大哩品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.跋大哩', handler: function(){go2("Ap413.htm")}},
	         {text: '2.一傘者', handler: function(){go2("Ap414.htm")}},
	         {text: '3.低那素勒茉莉衣者', handler: function(){go2("Ap415.htm")}},
	         {text: '4.蜜肉施與者', handler: function(){go2("Ap416.htm")}},
	         {text: '5.鐵木樹幼芽', handler: function(){go2("Ap417.htm")}},
	         {text: '6.一盞燈火者', handler: function(){go2("Ap418.htm")}},
	         {text: '7.腰花者', handler: function(){go2("Ap419.htm")}},
	         {text: '8.粥施與者', handler: function(){go2("Ap420.htm")}},
	         {text: '9.一粑鉈飯施與者', handler: function(){go2("Ap421.htm")}},
	         {text: '10.床施與者', handler: function(){go2("Ap422.htm")}}
		]})}
	             ]
	});

	var menu5 = new Ext.menu.Menu
	({id: 'mainMenu5',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '43.一次掃除者品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.一次掃除者', handler: function(){go2("Ap423.htm")}},
	         {text: '2.一塊布施與者', handler: function(){go2("Ap424.htm")}},
	         {text: '3.一個座位施與者', handler: function(){go2("Ap425.htm")}},
	         {text: '4.七串團花樹花者', handler: function(){go2("Ap426.htm")}},
	         {text: '5.荊棘金樹花者', handler: function(){go2("Ap427.htm")}},
	         {text: '6.酥油醍醐施與者', handler: function(){go2("Ap428.htm")}},
	         {text: '7.一法聽聞者', handler: function(){go2("Ap429.htm")}},
	         {text: '8.善思惟者', handler: function(){go2("Ap430.htm")}},
	         {text: '9.金色小鈴者', handler: function(){go2("Ap431.htm")}},
	         {text: '10.金旗者', handler: function(){go2("Ap432.htm")}}
		]})},
	 {text: '44.單獨住者品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.單獨住者', handler: function(){go2("Ap433.htm")}},
	         {text: '2.一海螺者', handler: function(){go2("Ap434.htm")}},
	         {text: '3.神變想者', handler: function(){go2("Ap435.htm")}},
	         {text: '4.智稱讚者', handler: function(){go2("Ap436.htm")}},
	         {text: '5.甘蔗棒者', handler: function(){go2("Ap437.htm")}},
	         {text: '6.葛蘭玻施與者', handler: function(){go2("Ap438.htm")}},
	         {text: '7.黃酸棗施與者', handler: function(){go2("Ap439.htm")}},
	         {text: '8.訶子施與者', handler: function(){go2("Ap440.htm")}},
	         {text: '9.芒果串者', handler: function(){go2("Ap441.htm")}},
	         {text: '10.芒果樹果實者', handler: function(){go2("Ap442.htm")}}
		]})},
	 {text: '45.欖仁品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.欖仁核者', handler: function(){go2("Ap443.htm")}},
	         {text: '2.棗子施與者', handler: function(){go2("Ap444.htm")}},
	         {text: '3.木瓜者', handler: function(){go2("Ap445.htm")}},
	         {text: '4.胡桃施與者', handler: function(){go2("Ap446.htm")}},
	         {text: '5.河枝花花朵者', handler: function(){go2("Ap447.htm")}},
	         {text: '6.黃酸棗者', handler: function(){go2("Ap448.htm")}},
	         {text: '7.獅子座者', handler: function(){go2("Ap449.htm")}},
	         {text: '8.腳踏凳者', handler: function(){go2("Ap450.htm")}},
	         {text: '9.欄杆建造者', handler: function(){go2("Ap451.htm")}},
	         {text: '10.菩提樹屋施與者', handler: function(){go2("Ap452.htm")}}
		]})},
	 {text: '46.基壇施與者品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.基壇施與者', handler: function(){go2("Ap453.htm")}},
	         {text: '2.孔雀羽毛團扇者', handler: function(){go2("Ap454.htm")}},
	         {text: '3.搧獅子座者', handler: function(){go2("Ap455.htm")}},
	         {text: '4.持三火把者', handler: function(){go2("Ap456.htm")}},
	         {text: '5.踏墊施與者', handler: function(){go2("Ap457.htm")}},
	         {text: '6.樹林荊棘金樹者', handler: function(){go2("Ap458.htm")}},
	         {text: '7.一把傘者', handler: function(){go2("Ap459.htm")}},
	         {text: '8.花種類者', handler: function(){go2("Ap460.htm")}},
	         {text: '9.帕低花者', handler: function(){go2("Ap461.htm")}},
	         {text: '10.香料供養者', handler: function(){go2("Ap462.htm")}}
		]})},
	 {text: '47.沙羅樹花者品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.沙羅樹花者', handler: function(){go2("Ap463.htm")}},
	         {text: '2.火葬用柴堆供養者', handler: function(){go2("Ap464.htm")}},
	         {text: '3.火葬用柴堆熄滅者', handler: function(){go2("Ap465.htm")}},
	         {text: '4.橋施與者', handler: function(){go2("Ap466.htm")}},
	         {text: '5.大花朵茉莉棕櫚樹葉扇子者', handler: function(){go2("Ap467.htm")}},
	         {text: '6.阿哇得樹果實者', handler: function(){go2("Ap468.htm")}},
	         {text: '7.麵包樹果實施與者', handler: function(){go2("Ap469.htm")}},
	         {text: '8.黃葛樹果實施與者', handler: function(){go2("Ap470.htm")}},
	         {text: '9.自己辯才者', handler: function(){go2("Ap471.htm")}},
	         {text: '10.相解說者', handler: function(){go2("Ap472.htm")}}
		]})},
	 {text: '48.蘆葦花環品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.蘆葦花環者', handler: function(){go2("Ap473.htm")}},
	         {text: '2.寶珠供養者', handler: function(){go2("Ap474.htm")}},
	         {text: '3.百火把者', handler: function(){go2("Ap475.htm")}},
	         {text: '4.大花朵茉莉扇子者', handler: function(){go2("Ap476.htm")}},
	         {text: '5.粥施與者', handler: function(){go2("Ap477.htm")}},
	         {text: '6.八餐食物券施與者', handler: function(){go2("Ap478.htm")}},
	         {text: '7.山-紅厚殼樹者', handler: function(){go2("Ap479.htm")}},
	         {text: '8.南瓜果實施與者', handler: function(){go2("Ap480.htm")}},
	         {text: '9.草鞋施與者', handler: function(){go2("Ap481.htm")}},
	         {text: '10.沙-經行處者', handler: function(){go2("Ap482.htm")}}
		]})},
	 {text: '49.糞掃衣品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.糞掃衣想者', handler: function(){go2("Ap483.htm")}},
	         {text: '2.佛想者', handler: function(){go2("Ap484.htm")}},
	         {text: '3.蓮藕施與者', handler: function(){go2("Ap485.htm")}},
	         {text: '4.智稱讚者', handler: function(){go2("Ap486.htm")}},
	         {text: '5.檀香-花環者', handler: function(){go2("Ap487.htm")}},
	         {text: '6.遺骨供養者', handler: function(){go2("Ap488.htm")}},
	         {text: '7.沙生起者', handler: function(){go2("Ap489.htm")}},
	         {text: '8.渡過者', handler: function(){go2("Ap490.htm")}},
	         {text: '9.法喜好者', handler: function(){go2("Ap491.htm")}},
	         {text: '10.沙羅樹帳棚者', handler: function(){go2("Ap492.htm")}}
		]})},
	 {text: '50.小鈴花品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.三朵小鈴花者', handler: function(){go2("Ap493.htm")}},
	         {text: '2.糞掃衣供養者', handler: function(){go2("Ap494.htm")}},
	         {text: '3.荊棘金樹花者', handler: function(){go2("Ap495.htm")}},
	         {text: '4.緊叔迦樹花者', handler: function(){go2("Ap496.htm")}},
	         {text: '5.半塊布施與者', handler: function(){go2("Ap497.htm")}},
	         {text: '6.酥醍醐施與者', handler: function(){go2("Ap498.htm")}},
	         {text: '7.水施與者', handler: function(){go2("Ap499.htm")}},
	         {text: '8.沙塔者', handler: function(){go2("Ap500.htm")}},
	         {text: '9.蘆葦屋施與者', handler: function(){go2("Ap501.htm")}},
	         {text: '10.豆腐果樹果實施與者', handler: function(){go2("Ap502.htm")}}
		]})},
	 {text: '51.翅子樹品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.三朵翅子樹花者', handler: function(){go2("Ap503.htm")}},
	         {text: '2.一鉢施與者', handler: function(){go2("Ap504.htm")}},
	         {text: '3.無患子樹果實者', handler: function(){go2("Ap505.htm")}},
	         {text: '4.阿哇得樹果實者', handler: function(){go2("Ap506.htm")}},
	         {text: '5.玻達樹果實者', handler: function(){go2("Ap507.htm")}},
	         {text: '6.拘櫞樹果實施與者', handler: function(){go2("Ap508.htm")}},
	         {text: '7.阿介利樹果實施與者', handler: function(){go2("Ap509.htm")}},
	         {text: '8.阿莫達樹果實者', handler: function(){go2("Ap510.htm")}},
	         {text: '9.棕櫚樹果實施與者', handler: function(){go2("Ap511.htm")}},
	         {text: '10.椰子樹果實施與者', handler: function(){go2("Ap512.htm")}}
		]})},
	 {text: '52.果實施與者品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.古樂基亞果實施與者', handler: function(){go2("Ap513.htm")}},
	         {text: '2.蘋果樹果實施與者', handler: function(){go2("Ap514.htm")}},
	         {text: '3.苦楝樹果實者', handler: function(){go2("Ap515.htm")}},
	         {text: '4.露兜樹花者', handler: function(){go2("Ap516.htm")}},
	         {text: '5.鐵木樹花者', handler: function(){go2("Ap517.htm")}},
	         {text: '6.三果木樹花者', handler: function(){go2("Ap518.htm")}},
	         {text: '7.止瀉木花者', handler: function(){go2("Ap519.htm")}},
	         {text: '8.聲想者', handler: function(){go2("Ap520.htm")}},
	         {text: '9.一切果實施與者', handler: function(){go2("Ap521.htm")}},
	         {text: '10.戴上紅蓮者', handler: function(){go2("Ap522.htm")}}
		]})},
	 {text: '53.草施與者品品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.一把草施與者', handler: function(){go2("Ap523.htm")}},
	         {text: '2.床施與者', handler: function(){go2("Ap524.htm")}},
	         {text: '3.歸依者', handler: function(){go2("Ap525.htm")}},
	         {text: '4.塗油施與者', handler: function(){go2("Ap526.htm")}},
	         {text: '5.好綿布施與者', handler: function(){go2("Ap527.htm")}},
	         {text: '6.拐杖施與者', handler: function(){go2("Ap528.htm")}},
	         {text: '7.山-內勒供養者', handler: function(){go2("Ap529.htm")}},
	         {text: '8.菩提樹打掃者', handler: function(){go2("Ap530.htm")}},
	         {text: '9.蓖麻果實施與者', handler: function(){go2("Ap531.htm")}},
	         {text: '10.極芳香者', handler: function(){go2("Ap532.htm")}}
		]})},
	 {text: '54.迦旃延品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.大迦旃延', handler: function(){go2("Ap533.htm")}},
	         {text: '2.跋迦梨', handler: function(){go2("Ap534.htm")}},
	         {text: '3.大劫賓那', handler: function(){go2("Ap535.htm")}},
	         {text: '4.末羅人之子達玻', handler: function(){go2("Ap536.htm")}},
	         {text: '5.鳩摩羅迦葉', handler: function(){go2("Ap537.htm")}},
	         {text: '6.婆醯雅', handler: function(){go2("Ap538.htm")}},
	         {text: '7.摩訶俱絺羅', handler: function(){go2("Ap539.htm")}},
	         {text: '8.優樓頻螺迦葉', handler: function(){go2("Ap540.htm")}},
	         {text: '9.羅陀', handler: function(){go2("Ap541.htm")}},
	         {text: '10.空虛王', handler: function(){go2("Ap542.htm")}}
		]})},
	 {text: '55.拔提亞品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.侏儒拔提亞', handler: function(){go2("Ap543.htm")}},
	         {text: '2.更柯雷瓦達', handler: function(){go2("Ap544.htm")}},
	         {text: '3.夕瓦里', handler: function(){go2("Ap545.htm")}},
	         {text: '4.婆耆舍', handler: function(){go2("Ap546.htm")}},
	         {text: '5.難達葛', handler: function(){go2("Ap547.htm")}},
	         {text: '6.黑優陀夷', handler: function(){go2("Ap548.htm")}},
	         {text: '7.無畏', handler: function(){go2("Ap549.htm")}},
	         {text: '8.羅麼色耿其雅', handler: function(){go2("Ap550.htm")}},
	         {text: '9.哇那婆蹉', handler: function(){go2("Ap551.htm")}},
	         {text: '10.小極香者', handler: function(){go2("Ap552.htm")}}
		]})},
	 {text: '56.名聲品',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.名聲', handler: function(){go2("Ap553.htm")}},
	         {text: '2.那提迦葉', handler: function(){go2("Ap554.htm")}},
	         {text: '3.伽耶迦葉', handler: function(){go2("Ap555.htm")}},
	         {text: '4.金毘羅', handler: function(){go2("Ap556.htm")}},
	         {text: '5.跋耆子', handler: function(){go2("Ap557.htm")}},
	         {text: '6.鬱多羅', handler: function(){go2("Ap558.htm")}},
	         {text: '7.另位鬱多羅', handler: function(){go2("Ap559.htm")}},
	         {text: '8.賢勝利', handler: function(){go2("Ap560.htm")}},
	         {text: '9.尸婆迦', handler: function(){go2("Ap561.htm")}},
	         {text: '10.優波瓦那', handler: function(){go2("Ap562.htm")}},
	         {text: '11.護國', handler: function(){go2("Ap563.htm")}}
		]})}
	             ]
	});

	var menu6 = new Ext.menu.Menu
	({id: 'mainMenu6',
	 style: {overflow: 'visible'},
	 items: [
	 {text: '1.蘇昧達品(57.)',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.蘇昧達', handler: function(){go2("Ap564.htm")}},
	         {text: '2.腰帶施與者', handler: function(){go2("Ap565.htm")}},
	         {text: '3.帳棚施與者', handler: function(){go2("Ap566.htm")}},
	         {text: '4.橋', handler: function(){go2("Ap567.htm")}},
	         {text: '5.蘆葦花環者', handler: function(){go2("Ap568.htm")}},
	         {text: '6.一鉢食施與者', handler: function(){go2("Ap569.htm")}},
	         {text: '7.一匙食物施與者', handler: function(){go2("Ap570.htm")}},
	         {text: '8.七朵青蓮花環者', handler: function(){go2("Ap571.htm")}},
	         {text: '9.五燈者', handler: function(){go2("Ap572.htm")}},
	         {text: '10.水施與者', handler: function(){go2("Ap573.htm")}}
		]})},
	 {text: '2.一布薩者品(58.)',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.一布薩者', handler: function(){go2("Ap574.htm")}},
	         {text: '2.乳香樹花者', handler: function(){go2("Ap575.htm")}},
	         {text: '3.糖果施與者', handler: function(){go2("Ap576.htm")}},
	         {text: '4.一座施與者', handler: function(){go2("Ap577.htm")}},
	         {text: '5.五燈者施與者', handler: function(){go2("Ap578.htm")}},
	         {text: '6.蘆葦花環者', handler: function(){go2("Ap579.htm")}},
	         {text: '7.摩訶波闍波提喬達彌', handler: function(){go2("Ap580.htm")}},
	         {text: '8.讖摩', handler: function(){go2("Ap581.htm")}},
	         {text: '9.蓮華色', handler: function(){go2("Ap582.htm")}},
	         {text: '10.帕大者臘', handler: function(){go2("Ap583.htm")}}
		]})},
	 {text: '3.捲髮者品(59.)',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.捲髮者', handler: function(){go2("Ap584.htm")}},
	         {text: '2.居沙喬達彌', handler: function(){go2("Ap585.htm")}},
	         {text: '3.法施', handler: function(){go2("Ap586.htm")}},
	         {text: '4.色古拉', handler: function(){go2("Ap587.htm")}},
	         {text: '5.難陀', handler: function(){go2("Ap588.htm")}},
	         {text: '6.受那', handler: function(){go2("Ap589.htm")}},
	         {text: '7.賢者葛逼勒', handler: function(){go2("Ap590.htm")}},
	         {text: '8.耶輸陀羅', handler: function(){go2("Ap591.htm")}},
	         {text: '9.一萬', handler: function(){go2("Ap592.htm")}},
	         {text: '10.一萬八千', handler: function(){go2("Ap593.htm")}}
		]})},
	 {text: '4.女剎帝利品(60.)',
	      menu: new Ext.menu.Menu({
	      items: [
	         {text: '1.亞色哇低', handler: function(){go2("Ap594.htm")}},
	         {text: '2.八萬四千', handler: function(){go2("Ap595.htm")}},
	         {text: '3.青蓮施與者', handler: function(){go2("Ap596.htm")}},
	         {text: '4.辛額勒的母親', handler: function(){go2("Ap597.htm")}},
	         {text: '5.白', handler: function(){go2("Ap598.htm")}},
	         {text: '6.殊妙難陀', handler: function(){go2("Ap599.htm")}},
	         {text: '7.迦尸富裕者', handler: function(){go2("Ap600.htm")}},
	         {text: '8.傅尼葛', handler: function(){go2("Ap601.htm")}},
	         {text: '9.蓭婆巴利', handler: function(){go2("Ap602.htm")}},
	         {text: '10.美善者', handler: function(){go2("Ap603.htm")}}
		]})}
	             ]
	});


// 主選單 : 2.橫式主選單 ------------------------------
	var tb = new Ext.Toolbar();
	tb.render('toolbar');
	tb.add(
	{text:'首　頁',
	handler: function(){go2("../index.htm")}},
	{text:'Ⅰ. 1~品',  menu: menu1}, // 下拉的選單
	{text:' 11~品',  menu: menu2}, // 下拉的選單
	{text:' 21~品',  menu: menu3}, // 下拉的選單
	{text:' 31~品',  menu: menu4}, // 下拉的選單
	{text:' Ⅱ. 43~品',  menu: menu5}, // 下拉的選單
	{text:' [Ⅲ.]長老尼',  menu: menu6}, // 下拉的選單
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
		if (myurl.match(/Ap(\d+)\.htm/) != null){var sutranum = myurl.replace(/^.*?(\d+)\.htm/i,"$1");}// 取出經號
		var pre_sutra = parseInt(sutranum,10) - 1; 
		// 前一經
		if(pre_sutra < 1){pre_sutra = 603;}
		pre_sutra = "Ap" + pre_sutra.toString() + ".htm";
		go2(pre_sutra);
	}
	function next_sutra() {
		var myurl=window.location.toString();
		if (myurl.match(/Ap(\d+)\.htm/) != null){var sutranum = myurl.replace(/^.*?(\d+)\.htm/i,"$1");}// 取出經號
		var next_sutra = parseInt(sutranum,10) + 1; 
		// 下一經
		if(next_sutra > 603) {next_sutra = 1;}
		next_sutra = "Ap" + next_sutra.toString() + ".htm";
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

	mycomp=mycomp.replace(/Bv.(\d+)/g, function(word,str1)
	{
		var mynum = "" + str1.toString();
		mynum = mynum.replace(/^.*(\d\d\d)/,"$1");
		mynum = '<a href="../Bv/Bv' + mynum + '.htm" target="xxx">Bv.' + str1.toString()+ '</a>';
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

	mycomp=mycomp.replace(/Bv.(\d+)/g, function(word,str1)
	{
		var mynum = "" + str1.toString();
		mynum = mynum.replace(/^.*(\d\d\d)/,"$1");
		mynum = '<a href="../Bv/Bv' + mynum + '.htm" target="xxx">Bv.' + str1.toString()+ '</a>';
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
