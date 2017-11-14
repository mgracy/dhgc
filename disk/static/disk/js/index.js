/**
 * 
 * @authors Your Name (you@example.org)
 * @date    2017-03-07 15:05:12
 * @version $Id$
 */

/* ------------------------------------------------------------------ */
/*    File
/* ------------------------------------------------------------------ */
$('input[type=button]').click(function(){
    if (window.File && window.FileReader && window.FileList && window.Blob) {
        console.log( 'browser ok' )
        $('#files').click();

    } else {
        showOverlay("Your current browser does not support file uploads\n\rPlease update or change a browser\n\rIt is recommended to use Google/firefox");
        // alert('Your current browser does not support file uploads\n\rPlease update or change a browser\n\rIt is recommended to use Google/firefox')
        return;
    }
})



function handleFileSelect(e){

    var files = e.target.files;
    var output = [];
    var maxSize = 5;
    var xhr = new XMLHttpRequest();
    
	

    for (var i=0, f; f = files[i]; i++) {
        output.push( escape(f.name), "===", f.size, "===", f.lastModifiedDate.toLocaleDateString() )
        // File-size
        if ( parseInt(output[2]) >= maxSize*Math.pow(1024, 2) ) {

            console.log( parseInt(output[2]) );
            $('#files-info').val( '当前限制上传文件大小不超过'+maxSize+'MB' );
            showOverlay('当前限制上传文件大小不超过'+maxSize+'MB');

            files = null; output = [];
            $('#files').val("");
		
			
        } else {
            console.log('=======size-ok:'+parseInt(output[2]))
                 console.log($('#files').val())
	       	$("#form").submit();
            /* xhr.open( "post", "/upload", true );
            // xhr.setRequestHeader("Content-type","application/x-www-form-urlencoded");
            xhr.onreadystatechange = function() {
                if( xhr.status ==200 ) {
                    if( xhr.readyState ==4 ) {
                        console.log(xhr.responseText);
                    }
                }
            };
            xhr.upload.onprogress = function(event){
                event = event || window.event
                // event object update-info;
                var pre = Math.floor(100 * parseFloat(event.loaded) / parseFloat(event.total));
                $("#files-info").val( "当前上传进度为：" + pre + "%" );
                if( pre==100 ) {
                    $('.show-file').css("display", "block");
                }
            }
            // filename,
            var sData = new FormData();
            sData.append( "file", f)
            xhr.send( sData )
            console.log( sData ); */
            /*
            sData.append( "files[]", f);
            var ops = {
                "method": "post",
                "url"   : "upload.php",
                "data"  : "sData",
                "processDate" : false,
                "contentType" : false,
                "success"     : function(data){
                    console.log( data );
                }
            }
            $.ajax(ops);
            */
            break
        }
        $('#files').val("");
        files = null; output = [];
    }
    $('#files-info').val( output.join('') );
}
document.getElementById('files').addEventListener('change', handleFileSelect, false);



/* ------------------------------------------------------------------ */
/*    Heart
/* ------------------------------------------------------------------ */
$('#h-animate').css({
    top: $(document).height() / 2.7 + 'px'
});
$('#h-animate').css({
    'margin-left': -$('#h-animate').width() / 2 + 'px'// startPage heart
});

// hover
$('#h-animate').mouseenter(function() {
    $('#h-animate').css({
        'margin': 'auto',
        'width': 'auto'
    });
    var offset = $(this).offset();
    $(this).html("&#10084;"); //Change heart
    // Get heart W/H
    var spanWidth = $(this).width();
    var spanHeight = $(this).height();

    var width = $(document).width() - spanWidth - 10; //-10 due to font adjustment 
    var height = $(document).height() - spanHeight - 10; //-10 due to font adjustment
    // random W/H
    var x = (Math.random() * width);
    var y = (Math.random() * height);

  //Ensure new position will not accidently be under mouse again
    while (x >= (offset.left - spanWidth / 4) && x <= (offset.left + spanWidth)) {
        x = (Math.random() * width);
    }
    while (y >= (offset.top - spanHeight / 4) && y <= (offset.top + spanHeight)) {
        y = (Math.random() * height);
    }
    var randomR = parseInt(Math.random()*255);
    var randomG = parseInt(Math.random()*255);
    var randomB = parseInt(Math.random()*255);
    var randomO = Math.random() + 0.01
    var randomColor = "rgba("+randomR+","+randomG+","+randomB+","+randomO+")"
    $(this).css('left', x);
    $(this).css('top', y);
    $(this).css('color', randomColor)
});

// resizing position
$(window).resize(function() {
    $('#h-animate').css({
        top: $(document).height() / 3 + 'px'
    });
    $('#h-animate').css({
        'left': "50%"
    });
    $('#h-animate').css({
        'margin-left': -$('#h-animate').width() / 2 + 'px'
    });
});



// /* ------------------------------------------------------------------ */
// /*    BackGround
// /* ------------------------------------------------------------------ */
// $('body').vegas({
//     overlay: '/static/img/overlay.png',
//     slides: [
//         // { src: 'img/banner8.jpg' },
//         // { src: 'img/banner7.jpg' },
//         // { src: 'img/banner6.jpg' },
//         // { src: 'img/banner5.jpg' },
//         // { src: 'img/banner4.jpg' },
//         { src: '/static/img/bannerq3.jpg' },
//         { src: '/static/img/bannerq2.jpg' },
//         { src: '/static/img/bannerq1.jpg' },
//     ],
// })



/* ------------------------------------------------------------------ */
/*    Page-Loader
/* ------------------------------------------------------------------ */
// // Wait for window load
// $(window).load(function() {
// // Animate loader off screen
//     $(".page-loader").fadeOut( "slow" );
    
//     new WOW().init();

//     new Clipboard($('button')[0]);
// });



/* ------------------------------------------------------------------ */
/*    Shade
/* ------------------------------------------------------------------ */
function showOverlay(info, buttt) {
    info = info || "您有消息~";
    buttt = buttt || "OK";
    $("#ok").html( buttt );
    $('.text-info').html( info );
    $(".popup-window").fadeIn(500);
    // To prevent the failure CSS
    setTimeout("$('.stick').toggleClass(function() {return $(this).is('.open, .close') ? 'open close' : 'open'})",400)
};



    /* -------------------------------------------------------------- */
    /*    Shade/1. window.animate
    /* -------------------------------------------------------------- */
    $(document).ready(function() {
        function hideOverlay() {
            $("#shade").animate( {"top": "100px"}, 50, function() {
                $(this).animate( {"top": "-999px"}, 200, function() {
                    $(".popup-window").fadeOut(300, function() {
                        $("#shade").css({"top":"0"});
                    });
                });
            })

        };
        $(".shade-container").click(function() {
            // To prevent the failure CSS
            $(".stick").toggleClass(function () {
                if($(this).is('.open, .close')){ hideOverlay()
                    return 'open close';
                };
                return $(this).is('.open, .close') ? 'open close' : 'open';
            });
            return false;
        });
        $(".popup-window").click( function(){
            // To prevent the failure CSS
            $(".stick").toggleClass(function () {
                if($(this).is('.open, .close')){ hideOverlay()
                    return 'open close';
                };
                return $(this).is('.open, .close') ? 'open close' : 'open';
            });
            return false;   
        });

    });

/* ------------------------------------------------------------------ */
/*    search
/* ------------------------------------------------------------------ */
$('.search-text-icon').click(function() {
   
    if( !$("#files-info").val() || $("#files-info").val().length < 4 ) {
        $("#files-info").focus().val("").attr("placeholder","搜索内容不能为空或长度小于4个字符");
	
    } else {
       // $("#search").submit()

        /* ------------------------------ */
        /*     search-submit
        /* ------------------------------ */
	var op = {
    	    "method" : "get",
    	    "url" : "/disk/search/",
            "data": "kw=" + $("#files-info").val(),
    	    "success" : function(data) {
                console.log(data);
        		addSearchFile(data);
            },
    	    "error" : function(error) {
    	    	console.log(error);
    	    }
        };

	function addSearchFile(data) {
	    data = eval('('+data+')');
	    $('.file-content').remove();
	    for(var i=0; i<data.length; i++) {
    		var html = 
    		'<div class="file-content">' +
                '<div class="file-name" style="width:24%;margin-left:1%">'+data[i].name+'</div>' +
                '<div class="file-size" style="width:10%;">'+data[i].size+'</div>' +
                '<div class="file-date" style="width:10%;">'+data[i].downloads+'</div>' +
                '<div class="file-date" style="width:20%;">'+data[i].created_date+'</div>' +
                '<div class="file-link" style="width:35%; padding-right: 80px; text-overflow: ellipsis; overflow: hidden;">' +
                    '<span>' +
                        'https://pan.tanzhouvip.com/s/'+data[i].size+
                    '</span>' +
                '</div>' +
                '<button><a href="/s/'+data[i].size+'">Download</a></button>' +
            '</div>'
    		$('.show-file').append( html ).show();
	    }
	}
	
	$.ajax(op);

    };
})

// /* ------------------------------------------------------------------ */
// /*    qqad
// /* ------------------------------------------------------------------ */
// $('.adbtn').each(function(i){
//     $(this).click(function(){
// 	if(i==0){
//         window.location.href="tencent://message/?uin=2463597788&Site=可里老师&Menu=no"
//      }
//         if(i==1){
// 	window.location.href="tencent://message/?uin=1463590088&Site=可里老师&Menu=no"
// 	}
// 	if(i==2){
// 	window.location.href="tencent://message/?uin=1263591188&Site=可里老师&Menu=no"
// 	}
//     })
// })
