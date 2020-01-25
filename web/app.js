function GdGetHours()
{
	var dt = new Date();
	return dt.getHours() + "";
}

function GdRefreshPlot(gd_tablename)
{
    var cls_prefix;
    if (gd_tablename == "humidities")
    {
        cls_prefix = "#hp";
    }
    if (gd_tablename == "brightnesses")
    {
        cls_prefix = "#bp";
    }
	var gd_s_date = $( cls_prefix + "_t_start" ).datepicker("getDate");
	var gd_s_time = $( cls_prefix + "_h_start" ).val();
	var t_start = gd_s_date.getFullYear() + "" 
	+ ((gd_s_date.getMonth()+1)+"").padStart(2,"0") 
	+ (gd_s_date.getDate()+"").padStart(2,"0") + gd_s_time + "0000";
	var gd_e_date = $( cls_prefix + "_t_end" ).datepicker("getDate");
	var gd_e_time = $( cls_prefix + "_h_end" ).val();
	var t_end = gd_e_date.getFullYear() + "" 
	+ ((gd_e_date.getMonth()+1)+"").padStart(2,"0") 
	+ (gd_e_date.getDate()+"").padStart(2,"0") + gd_e_time + "0000";	
	var img_src = gd_tablename + "?plot&t_start=" + t_start + "&t_end=" + t_end;

	$(cls_prefix + "_plt").attr("src",img_src);
}


$(function(){

$( "#hp_t_start" ).datepicker({
  dateFormat: "yy-mm-dd",
  onSelect: function()
  {
  	GdRefreshPlot("humidities");
  }
}).datepicker("setDate", "-1d");
$( "#hp_t_end" ).datepicker({
  dateFormat: "yy-mm-dd",
  onSelect: function()
  {
  	GdRefreshPlot("humidities");
  }
}).datepicker("setDate", "+0d");
$( "#bp_t_start" ).datepicker({
  dateFormat: "yy-mm-dd",
  onSelect: function()
  {
  	GdRefreshPlot("brightnesses");
  }
}).datepicker("setDate", "-1d");
$( "#bp_t_end" ).datepicker({
  dateFormat: "yy-mm-dd",
  onSelect: function()
  {
  	GdRefreshPlot("brightnesses");
  }
}).datepicker("setDate", "+0d");

$( "#n_api").click(function(){
	$("#t_api").show();
	$("#t_humidity").hide();
	$("#t_brightness").hide();
});

$( "#n_humidity").click(function(){
	$("#t_api").hide();
	$("#t_humidity").show();
	$("#t_brightness").hide();
});

$( "#n_brightness").click(function(){
	$("#t_api").hide();
	$("#t_humidity").hide();
	$("#t_brightness").show();
});

$( "#hp_h_start" ).val(GdGetHours())
  .selectmenu({
  	width: 120,
  	change: function( event, ui ) {
  		GdRefreshPlot("humidities");
  	}
  })
  .selectmenu( "menuWidget" )
    .addClass( "overflow" );

$( "#hp_h_end" ).val(GdGetHours())
  .selectmenu({
  	width: 120,
  	change: function( event, ui ) {
  		GdRefreshPlot("humidities");
  	}
  })
  .selectmenu( "menuWidget" )
    .addClass( "overflow" );


$( "#bp_h_start" ).val(GdGetHours())
  .selectmenu({
  	width: 120,
  	change: function( event, ui ) {
  		GdRefreshPlot("brightnesses");
  	}
  })
  .selectmenu( "menuWidget" )
    .addClass( "overflow" );

$( "#bp_h_end" ).val(GdGetHours())
  .selectmenu({
  	width: 120,
  	change: function( event, ui ) {
  		GdRefreshPlot("brightnesses");
  	}
  })
  .selectmenu( "menuWidget" )
    .addClass( "overflow" );

});