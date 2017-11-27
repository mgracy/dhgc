$(function() {
  $('#divResult').on('dblclick', '.table tr td.dbclicktd', tdClick);

    function tdClick(){
        var tdnode = $(this);
        var tdtext = tdnode.text();
        tdnode.html("");
        var input = $("<input style='width:80px;'>");
        input.val(tdtext); //    input.attr("value",tdtext);
        input.keyup(function(event){
            var myEvent = event || window.event;
            var keyCode = myEvent.keyCode;
            if(keyCode == 13){
                var inputnode = $(this);
                var inputtext = inputnode.val();
                var td = inputnode.parent();
                td.html(inputtext);
                td.click(tdClick);
            }
            if(keyCode == 27){  //判断是否按下ESC键
                $(this).parent().html(tdtext);
                $(this).parent().click(tdClick);
            }
        });

        tdnode.append(input);
        tdnode.children("input").trigger("select");
        //输入框失去焦点，所执行的方法
        input.blur(function(){
            tdnode.html($(this).val());
            tdnode.click(tdClick);
        });
        tdnode.unbind("click");
    }

  var urlPath = "{{urlPath}}";
  $("ul.navContent li a").each(function(index, item){
      if($(item).attr('href') == urlPath){
          $(item).parent().addClass('active');
          return false;
      }
  });
  /*换肤*/
  $(".dropdown .changecolor li").click(function() {
    var style = $(this).attr("id");
    $("link[title!='']").attr("disabled", "disabled");
    $("link[title='" + style + "']").removeAttr("disabled");

    $.cookie('mystyle', style, {
      expires: 7
    }); // 存储一个带7天期限的 cookie 
  })
  //gracy.ma 2017/11/8
  // var cookie_style = $.cookie("mystyle"); 
  // if(cookie_style!=null){ 
  //     $("link[title!='']").attr("disabled","disabled"); 
  //  $("link[title='"+cookie_style+"']").removeAttr("disabled"); 
  // } 
  /*左侧导航栏显示隐藏功能*/
  $(".subNav").click(function() {
    /*显示*/
    if ($(this).find("span:first-child").attr('class') == "title-icon glyphicon glyphicon-chevron-down") {
      $(this).find("span:first-child").removeClass("glyphicon-chevron-down");
      $(this).find("span:first-child").addClass("glyphicon-chevron-up");
      $(this).removeClass("sublist-down");
      $(this).addClass("sublist-up");
    }
    /*隐藏*/
    else {
      $(this).find("span:first-child").removeClass("glyphicon-chevron-up");
      $(this).find("span:first-child").addClass("glyphicon-chevron-down");
      $(this).removeClass("sublist-up");
      $(this).addClass("sublist-down");
    }
    // 修改数字控制速度， slideUp(500)控制卷起速度
    $(this).next(".navContent").slideToggle(300).siblings(".navContent").slideUp(300);
  })
  /*左侧导航栏缩进功能*/
  $(".left-main .sidebar-fold").click(function() {

    if ($(this).parent().attr('class') == "left-main left-full") {
      $(this).parent().removeClass("left-full");
      $(this).parent().addClass("left-off");

      $(this).parent().parent().find(".right-product").removeClass("right-full");
      $(this).parent().parent().find(".right-product").addClass("right-off");

    } else {
      $(this).parent().removeClass("left-off");
      $(this).parent().addClass("left-full");

      $(this).parent().parent().find(".right-product").removeClass("right-off");
      $(this).parent().parent().find(".right-product").addClass("right-full");
    }
  })

  /*左侧鼠标移入提示功能*/
  $(".sBox ul li").mouseenter(function() {
    if ($(this).find("span:last-child").css("display") == "none") {
      $(this).find("div").show();
    }
  }).mouseleave(function() {
    $(this).find("div").hide();
  })

  window.IsEdit = false;
  window.onbeforeunload = function () {
    if (window.IsEdit === true)
        return "Are you sure to leave without save?";
  };

  $("#Create,#Search,#Save,#Reset").on("click", function () {
      window.IsEdit = false;
      return true;
  });  

  $("#btnCancel").click(function(){
    $("input:text").val("");
    $("input[type='date']").val("");
    $("input[type='time']").val("");
    $("input[type='number']").val("");
  });

  $("#btnSubmit").click(function(){
    $("#hiddenData").val($("#divResult").html());

    var flag = true;
    $("td.dbclicktd").each(function(i, item){
      var itemText = $(item).text();
      if(itemText == "NaN" || itemText == "None" || itemText == "0" || itemText.length<=0){
        flag = false;
        return false;
      }
    });
    if(!flag){
        $("#kv-error-1").html("请务必填写红字列对应的字段").show().fadeOut(5000);
        return false;
    }

    if($("#hiddenData").val().length<20){
      $("#kv-error-1").prepend("请先完成相应操作后再点提交").show().fadeOut(3000);
      return false;
    }

    $("#form1").submit();
  });

  $('.datepicker').datetimepicker({
      language: 'en',
      format: 'yyyy-mm-dd',
      maskInput: true,           // disables the text input mask
      pickDate: true,            // disables the date picker
      pickTime: false,            // disables de time picker
      // enables the 12-hour format time picker
      // set a minimum date
      //startDate: new Date(0),
      endDate: Infinity,          // set a maximum date
      todayBtn: true,
      autoclose: true,
      minView: '2',
      forceParse: false,
      todayHighlight: true,
      keyboardNavigation: false
  });
});