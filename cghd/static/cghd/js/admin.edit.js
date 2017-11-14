(function ($) {
    $.getUrlParam = function (name) {
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
        var r = window.location.search.substr(1).match(reg);
        if (r != null) return unescape(r[2]);
        return null;
    };
    //字符串转日期格式，strDate要转为日期格式的字符串//dd/MM/yyyy
    $.getDateByStr = function (strDate) {
        var st = strDate;
        var a = st.split(" ");
        a[1] = a[1] || "";
        var b = a[0].split("/");
        var c = a[1].split(":");
        c[0] = c[0] || 0;
        c[1] = c[1] || 0;
        c[2] = c[2] || 0;
        var date = new Date(b[2], b[1] - 1, b[0], c[0], c[1], c[2]);
        return date;
    };
    
    $.SelectedCheckValidity = function(el, start, end) {
        var sValue = $(start).val();
        var eValue = $(end).val();
        if (eValue && sValue) {
            var startValue = $.getDateByStr(sValue);
            var endValue = $.getDateByStr(eValue);
            var datetime = new Date();
            datetime = new Date(datetime.getFullYear(), datetime.getMonth(), datetime.getDate());
            if (startValue <= datetime && datetime <= endValue) {
                $(el).multiselect('enable');
        } else {
                $(el).multiselect('deselect', "all");
                $(el).multiselect('select', "0");
                $(el).multiselect('disable');
        }
        }
    };
    $.startWith = function (source,str) {
        var reg = new RegExp("^" + str);
        return reg.test(source);
    }
    $.endWith = function (source, str) {
        var reg = new RegExp(str + "$");
        return reg.test(source);
    }
})(jQuery);

$(document).ready(function () {

    //$("input[type='text']").blur(function () { $(this).removeClass("highlight"); }).focus(function () { $(this).addClass("highlight"); });

    //$(".integer").numeric(false, function () { alert("只能输入数字"); this.value = ""; this.focus(); });

    if ($.fn.fileinput) {
        var fileuploadTags = $(".fileupload");
        var thumbnailPath = '/SysAttachment/ViewThumbnail/{0}';
        var delPath = '../DelAttachment/{0}?dataid={1}&fieldName={2}';// '/api/Attachment/{0}';
        //var dataPath = 'DelAttachment/{0}?fieldName={1}';
        var formModelkey = "#UUID";


        $.extend($.fn, {
            readonView: function (input, type) {
                type = type || "img";
                var uuid = $.trim(input.val());
                var btnpanel = $("<span target='view'></span>");
                var del = $("<button class='btn btn-default' type='button' target='view' view='" + type + "'>delete</button>");
                var link = $("<a class='btn btn-default' target='view' view='" + type + "' target='_blank'>view</a>");

                if (uuid && uuid != "0") {
                    link.attr("href", $.format(thumbnailPath, uuid));
                    del.attr("href", $.format(delPath, uuid, $(formModelkey).val(), input.attr("name")));
                    btnpanel.removeClass("hide");
                } else {
                    input.val("0");
                    btnpanel.addClass("hide");
                }

                del.on("click", function () {
                    $(this).deleteView(this);
                    return false;
                });
                btnpanel.append(del).append(link);
                input.prev().append(btnpanel); //.append(link);//.siblings(".help-inline")
            },
            UpdateView: function (input, type) {
                type = type || "img";
                var uuid = $.trim(input.val());
                var panel = input.parent().find("span[target='view']");
                var link = input.parent().find("a[view]");
                var del = input.parent().find("button[view]"); //.siblings(".help-inline")
                link.attr("href", $.format(thumbnailPath, uuid));
                //del.attr("href", $.format(delPath, uuid));
                del.attr("href", $.format(delPath, uuid, $(formModelkey).val(), input.attr("name")));
                if (uuid == "0") {
                    panel.addClass("hide");
                } else {
                    panel.removeClass("hide");
                }
            },
            deleteView: function (el) {
                var self = $(el);
                var type = self.attr("view");
                if (confirm("Are you sure you want to delete the record?")) {
                    $.ajax({
                        url: self.attr("href"),
                        type: "POST",
                        success: function (data, status) {
                            if (data) {
                                self.parent().addClass("hide");
                                var input = $(".fileupload", self.parents(".file-input"));
                                var fileinput = input.data("fileinput");
                                if (type == "img")
                                    fileinput.setCaption("Image To Upload");
                                else
                                    fileinput.setCaption("Target List CSV File");
                                var forfield = input.attr("forfield");
                                var hidden = $("#" + forfield);
                                hidden.val("0");
                            } else {
                                alert("delete error!");
                            }
                        },
                        error: function (data, status, text) {
                            if (text)
                                alert(text);
                        }
                    });
                }
            }
        });


        fileuploadTags.each(function (i, el) {

            var self = $(el);
            var forfield = self.attr("forfield");
            //console.log(forfield);

            var find = $.format("input[name={0}]", forfield);

            var input = $(find);
            //var img = input.siblings(".help-inline").find("img");
            //var passImage = input.parents().find("#passImage");
            //var UUID = $.trim(input.val());

            //if (UUID && UUID != "0") {
            //    img.attr("src", $.format(thumbnailPath, UUID));
            //    img.parent("a").attr("href", $.format(thumbnailPath, UUID));
            //    passImage.attr("src", $.format(thumbnailPath, UUID));
            //    //console.log(input.val(), img);
            //} else if (self.data("required") == "True") {
            //    input.val("");
            //}

            var caption = self.data("initialcaption");
            //console.log(caption);

            var imgFileinput = self.fileinput({
                uploadUrl: "upload/",
                overwriteInitial: true,
                initialCaption: caption || "Image To Upload",
                showPreview: false,
                //allowedFileTypes: ['image'],
                previewFileType: 'image',
                //elErrorContainer: ".file-error-message",
                autoReplace: true,
                dropZoneEnabled: false,
                maxFileCount: 1,
                maxFileNum: 1,
                removeLabel: "",
                uploadLabel: "",
                browseLabel: "",
                browseClass: "btn btn-default",
                previewClass: "previewIcon",
                maxFileSize: 102400,
                layoutTemplates: {
                    main1:
                        "<div class=\'input-group {class}\'>\n" +
                            "   {caption}\n" +
                            "   <div class=\'input-group-btn\'>\n" +
                            "       {browse}\n" +
                            "       {upload}\n" +
                            "       {remove}\n" +
                            "   </div>\n" +
                            "   {preview}" +
                            "</div>\n"
                },
                previewSettings: {
                    image: { width: "auto", height: "30px" }
                },
                defaultPreviewSettings: {
                    image: { width: "60px", height: "30px" }
                }
            });

            if (imgFileinput) {
                // imgFileinput.readonView(input); ////这个页面右边有上传图像显示，因此上传完毕后不需要View按钮。Image是必须的，因此不需要Delete按钮。
                imgFileinput.on("filebatchuploadsuccess", function (event, data, previewId, index) {

                    var self = $(this);
                    var forfield = self.attr("forfield");
                    var name = data.files[0].name;
                    var hidden = $(this.form[forfield]);

                    var err = data.response.err;

                    if (err.length > 0) {
                        alert("Selected file is not a valid image format or the file size is larger than 500KB." + err);
                    } else {
                        var UUID = data.response.file["UUID"];

                        hidden.val(UUID);
                        hidden.attr("data-name", name);

                        if (hidden.valid)
                            hidden.valid();

                        setTimeout(function () {
                            var fileinput = self.data("fileinput");
                            fileinput.setCaption(name);
                        }, 500);

                        hidden.UpdateView(input);
                        //var img = hidden.siblings(".help-inline").find("img");
                        var passImage = hidden.parents().find("#passImage");
                        //img.attr("src", $.format(thumbnailPath, UUID));
                        passImage.attr("src", $.format(thumbnailPath, UUID));
                        //img.parent("a").attr("href", $.format(thumbnailPath, UUID));
                    }
                });

                imgFileinput.on("filebatchselected", function (event, files) {
                    var error = false;
                    if (!($.endWith(files[0].name.toLowerCase(), ".jpg") || $.endWith(files[0].name.toLowerCase(), ".png") || $.endWith(files[0].name.toLowerCase(), ".ico") || $.endWith(files[0].name.toLowerCase(), ".jepg"))) {
                        error = true;
                        alert("Selected file is not a valid image format or the file size is larger than 500KB.");
                    } else if (files[0].size > 500 * 1024) {
                        error = true;
                        alert("Selected file is not a valid image format or the file size is larger than 500KB.”");
                    }
                    if (error) {
                        var el = $(event.currentTarget);
                        //el.fileinput("reset");
                        //el.fileinput("clear");
                        //event.result = false;
                        //el.fileinput("setCaption", el.data("initialcaption"));
                        setTimeout(function () {
                            el.fileinput("clear");
                            el.fileinput("setCaption", el.data("initialcaption"));
                        }, 500);
                    }
                });
            }
        });
        
        var targetMemberListFileinput = $(".TargetListFileUpload").fileinput({
            uploadUrl: "/TargetListFileUpload.ashx",
            overwriteInitial: true,
            initialCaption: "Target List CSV File",
            showPreview: false,
            //allowedFileTypes: ['text'],
            allowedPreviewTypes: 'text',
            previewFileType: 'text', // 'image',
            //elErrorContainer: ".file-error-message",
            autoReplace: true,
            dropZoneEnabled: false,
            showUpload: true,
            maxFileSize: 204800,
            maxFileCount: 1,
            maxFileNum: 1,
            removeLabel: "",
            uploadLabel: "",
            browseLabel: "",
            browseClass: "btn btn-default",
            previewClass: "previewIcon",
            layoutTemplates: {
                main1:
                    "<div class=\'input-group {class}\'>\n" +
                        "   {caption}\n" +
                        "   <div class=\'input-group-btn\'>\n" +
                        "       {browse}\n" +
                        "       {upload}\n" +
                        "       {remove}\n" +
                        "   </div>\n" +
                        "   {preview}" +
                    "</div>\n"
            },
            previewSettings: {
                image: { width: "auto", height: "30px" }
            },
            defaultPreviewSettings: {
                image: { width: "60px", height: "30px" }
            }
        });
        if (targetMemberListFileinput) {
            var input = $("#" + targetMemberListFileinput.attr("forfield"));
            targetMemberListFileinput.readonView(input, "csv");

            targetMemberListFileinput.on("filebatchselected", function (event, files) {
                var error = false;
                if (!($.endWith(files[0].name, ".csv") || $.endWith(files[0].name, ".CSV"))) {
                    error = true;
                    alert("Invalid file format. File for Member List must be in csv format.");
                } else if (files[0].size > 2048 * 1024) {
                    error = true;
                    alert("Invalid file format. Member list file must be csv format and size smaller than 2M.");
                }
                if (error) {
                    var el = $(event.currentTarget);
                    //el.fileinput("reset");
                    //el.fileinput("clear");
                    //el.fileinput("setCaption", el.data("initialcaption"));
                    setTimeout(function () {
                        el.fileinput("clear");
                        el.fileinput("setCaption", el.data("initialcaption"));
                    }, 500);
                }
            });

            targetMemberListFileinput.on("filebatchuploadsuccess", function (event, data, previewId, index) {

                var self = $(this);
                var forfield = self.attr("forfield");
                var name = data.files[0].name;
                var hidden = $(this.form[forfield]);

                var err = data.response.err;

                if (err.length > 0) {
                    alert("Invalid file format. File for Member List must be in csv format." + err);
                    //alert("File " + name + " upload fail, reason:" + err);
                } else {
                    var UUID = data.response.file["UUID"];
                    hidden.attr("data-name", name);
                    console.log("setvalur:uuid= " + UUID);

                    hidden.val(UUID);

                    if (hidden.valid)
                        hidden.valid();

                    setTimeout(function() {
                        var fileinput = self.data("fileinput");
                        fileinput.setCaption(name);
                        console.log("setCaption " + name);
                    }, 1000);
                    targetMemberListFileinput.UpdateView(input, "csv");
                }
            });
        }

    //}//)();
    
    // PassFileUpload 
    // 该上传功能仅允许上传pkpass文件，同时会解析pkpass文件，并将ModelID,Version等信息显示在UI界面。
    //(function () {
         fileuploadTags = $(".passfileupload");
         //thumbnailPath = '/SysAttachment/ViewThumbnail/{0}';
        // filePath = '/SysAttachment/ViewThumbnail/{0}';
        // delPath = '../DelAttachment/{0}?dataid={1}&fieldName={2}';// '/api/Attachment/{0}';
        ////var dataPath = 'DelAttachment/{0}?fieldName={1}';
        // formModelkey = "#UUID";

         fileuploadTags.each(function (i, el) {

             var self = $(el);
             var forfield = self.attr("forfield");
             //console.log(forfield);

             var find = $.format("input[name={0}]", forfield);

             var input = $(find);
             //var img = input.siblings(".help-inline").find("img");
             var UUID = $.trim(input.val());

             if (UUID && UUID != "0") {
                 //  img.attr("src", $.format(thumbnailPath, UUID));
                 //  img.parent("a").attr("href", $.format(thumbnailPath, UUID));

                 //console.log(input.val(), img);
             } else if (self.data("required") == "True") {
                 input.val("");
             }

             var caption = self.data("initialcaption");
             //console.log(caption);

             var imgFileinput = self.fileinput({
                 uploadUrl: "/PassFileUpload.ashx",
                 overwriteInitial: true,
                 initialCaption: caption || "Pass To Upload",
                 showPreview: false,
                 //allowedFileExtensions: ['pkpass'], // 'image',
                 //elErrorContainer: ".file-error-message",
                 autoReplace: true,
                 dropZoneEnabled: false,
                 showUpload: true,
                 maxFileSize: 204800,
                 maxFileCount: 1,
                 maxFileNum: 1,
                 removeLabel: "",
                 uploadLabel: "",
                 browseLabel: "",
                 browseClass: "btn btn-default",
                 previewClass: "previewIcon",
                 layoutTemplates: {
                     main1:
                         "<div class=\'input-group {class}\'>\n" +
                             "   {caption}\n" +
                             "   <div class=\'input-group-btn\'>\n" +
                             "       {browse}\n" +
                             "       {upload}\n" +
                             "       {remove}\n" +
                             "   </div>\n" +
                             "   {preview}" +
                         "</div>\n"
                 },
                 previewSettings: {
                     image: { width: "auto", height: "30px" }
                 },
                 defaultPreviewSettings: {
                     image: { width: "60px", height: "30px" }
                 }
             });

             if (imgFileinput) {
                 imgFileinput.on("filebatchuploadsuccess", function (event, data, previewId, index) {

                     var self = $(this);
                     var forfield = self.attr("forfield");
                     var name = data.files[0].name;
                     var hidden = $(this.form[forfield]);
                     var dataRequireField = data.response.file.RequireField;
                     var err = data.response.err;
                     var templateType = hidden.parents().find("#Type").val();
                     var templateRequireField = "";
                     if (dataRequireField.trim().length >0 ) {
                         hidden.parents().find("#templateBonusPointField,#templateSpendingFields,#templateCouponCodeFields,#templateCouponValueFields,#templateExpiryDateFields").each(function (i, item) {
                             templateRequireField += item.value + ",";
                         });
                     }
                        
                     if (err.toString() == "Error") {
                         alert("Parse the pkpass file error.");
                     }else if (err.length > 0) {
                         alert("Invalid file format. File for pass file must be in pkpass format." + err);
                     } else if (CheckRequireField(dataRequireField, templateRequireField, templateType)) {
                         alert("Dynamic field is not allowed in " + templateType + ", please remove it from Pass2U design and upload the pkpass file again.");                                            
                     }else {
                         var UUID = data.response.file["UUID"];
                         var thumbnailPath = data.response.file["FilePath"];
                         //hidden.val(UUID);//原来FilePath存储的值为UUID，改变为绝对路径
                         hidden.val(thumbnailPath);
                         if (hidden.valid)
                             hidden.valid();

                         setTimeout(function () {
                             var fileinput = self.data("fileinput");
                             fileinput.setCaption(name);
                         }, 1000);

                         var img = hidden.siblings(".help-inline").find("img");
                         var modelID = hidden.parents().find("#ModelId");
                         var version = hidden.parents().find("#Version");
                         var passJson = hidden.parents().find("#PassJson");
                         var requireField = hidden.parents().find("#RequireField");
                         modelID.val(data.response.file.ModelID);
                         version.val(data.response.file.Version);
                         passJson.val(data.response.file.PassJson);
                         requireField.val(dataRequireField);
                         //img.attr("src", $.format(thumbnailPath, UUID));
                         //img.parent("a").attr("href", $.format(thumbnailPath, UUID));
                     }

                 });

                 imgFileinput.on("filebatchselected", function (event, files) {
                     var error = false;
                     if (!($.endWith(files[0].name, ".pkpass") || $.endWith(files[0].name, ".PKPASS"))) {
                         error = true;
                         alert("Invalid file format. File for pass file must be in pkpass format.");
                     } else if (files[0].size > 2048 * 1024) {
                         error = true;
                         alert("Invalid file format. Pass file must be pkpass format and size smaller than 2M.");
                     }
                     if (error) {
                         var el = $(event.currentTarget);
                         //el.fileinput("reset");
                         //el.fileinput("clear");
                         //el.fileinput("setCaption", el.data("initialcaption"));
                         setTimeout(function () {
                             el.fileinput("clear");
                             el.fileinput("setCaption", el.data("initialcaption"));
                         }, 500);
                     }
                 });
             }
         });
    
    //MemberListFileUpload 
    // Pass/Promotion/LBS 上传csv
    //(function () {
         fileuploadTags = $(".memberlistfileupload");
         //thumbnailPath = '/SysAttachment/ViewThumbnail/{0}';


         fileuploadTags.each(function (i, el) {

             var self = $(el);
             var forfield = self.attr("forfield");
             //console.log(forfield);

             var find = $.format("input[name={0}]", forfield);

             var input = $(find);
             var img = input.siblings(".help-inline").find("table");
             var UUID = $.trim(input.val());

             if (UUID && UUID != "0") {
                 //  img.attr("src", $.format(thumbnailPath, UUID));
                 //  img.parent("a").attr("href", $.format(thumbnailPath, UUID));

                 //console.log(input.val(), img);
             } else if (self.data("required") == "True") {
                 input.val("");
             }

             var caption = self.data("initialcaption");
             //console.log(caption);

             var imgFileinput = self.fileinput({
                 uploadUrl: "/MemberListFileUpload.ashx",
                 overwriteInitial: true,
                 initialCaption: caption || "MemberList To Upload",
                 showPreview: false,
                 //allowedFileExtensions: ['csv'], // 'image',
                 //elErrorContainer: ".file-error-message",
                 autoReplace: true,
                 dropZoneEnabled: false,
                 showUpload: true,
                 maxFileSize: 204800,
                 maxFileCount: 1,
                 maxFileNum: 1,
                 removeLabel: "",
                 uploadLabel: "",
                 browseLabel: "",
                 browseClass: "btn btn-default",
                 previewClass: "previewIcon",
                 layoutTemplates: {
                     main1:
                         "<div class=\'input-group {class}\'>\n" +
                             "   {caption}\n" +
                             "   <div class=\'input-group-btn\'>\n" +
                             "       {browse}\n" +
                             "       {upload}\n" +
                             "       {remove}\n" +
                             "   </div>\n" +
                             "   {preview}" +
                         "</div>\n"
                 },
                 previewSettings: {
                     image: { width: "auto", height: "30px" }
                 },
                 defaultPreviewSettings: {
                     image: { width: "60px", height: "30px" }
                 }
             });

             if (imgFileinput) {
                 imgFileinput.on("filebatchuploadsuccess", function (event, data, previewId, index) {

                     var self = $(this);
                     var forfield = self.attr("forfield");
                     var name = data.files[0].name;
                     var hidden = $(this.form[forfield]);

                     var err = data.response.err;
                     var formatErr = data.response.file.err;
     
                     if (err.length > 0) {
                         alert("Invalid file format. File for Member List must be in csv format." + err);
                     }else if (formatErr.length > 0) {
                         alert(formatErr);
                     } else {
                         var UUID = data.response.file["UUID"];

                         hidden.val(UUID);

                         if (hidden.valid)
                             hidden.valid();

                         setTimeout(function() {
                             var fileinput = self.data("fileinput");
                             fileinput.setCaption(name);
                         }, 1000);

                         var img = hidden.siblings(".help-inline").find("img");
                         var str = "";
                         var headerObj;
                         var array = [];
                         for (var i = 0; i < data.response.file.DtTable.length; i++) {
                             if (i == 0) {
                                 headerObj = data.response.file.DtTable[0];
                                 array = $.map(headerObj, function(value, index) {
                                     return [value];
                                 });
                                 str += "<thead>";
                                 for (var j = 0; j < array.length; j++) {
                                     str += "<th>" + data.response.file.DtTable[i][array[j]] + "</th>";
                                 }
                                 str += "</thead><tbody>";
                             } else {
                                 str += "<tr>";
                                 for (var col = 0; col < array.length; col++) {
                                     str += "<td>" + data.response.file.DtTable[i][array[col]] + "</td>";
                                 }
                             }
                             str += "</tr>";
                         }
                         str += "</tbody>";

                         var MemberListTable = hidden.parents('#divGeneralSetting').find('table[data-pass-type="MemberListTable"]');
                         MemberListTable.empty();
                         MemberListTable.append(str);
                         MemberListTable.show();
                         var modelID = hidden.parents().find("#ModelId");
                         var version = hidden.parents().find("#Version");
                         var requireFiledTable = hidden.parents().find("#RequirdFieldTable");
                         requireFiledTable.hide();
                         modelID.val(data.response.file.ModelID);
                         version.val(data.response.file.Version);
                         //img.attr("src", $.format(thumbnailPath, UUID));
                         //img.parent("a").attr("href", $.format(thumbnailPath, UUID));

                         //把MemberNo列表回填到用于查询条件框中
                         var memberNoFieldName = self.data("lbs_member_no_field");
                         if (memberNoFieldName) {
                             var memberNoInput = self.parents(".row").eq(0).find('input[name="{}"]'.replace('{}', memberNoFieldName));
                             var dtTable = data.response.file.DtTable;

                             if (dtTable) {
                                 var memberNoArray = [];

                                 for (var i = 1; i < dtTable.length; i++) {
                                     var dtItem = dtTable[i];
                                     var memberNo = dtItem['MemberNo'];
                                     memberNoArray.push(memberNo);
                                 }

                                 memberNoInput.val(memberNoArray.join(','));
                             }

                         }
                         $(".disablewhenuploaded").multiselect('disable');
                         CheckCsvMemberNosInCRM();
                     }

                     });


                 imgFileinput.on("filebatchselected", function (event, files) {
                     var error = false;
                     if (!($.endWith(files[0].name, ".csv") || $.endWith(files[0].name, ".CSV"))) {
                         error = true;
                         alert("Invalid file format. File for Member List must be in csv format.");
                     } else if (files[0].size > 2048 * 1024) {
                         error = true;
                         alert("Invalid file format. Member list file must be csv format and size smaller than 2M.");
                     }
                     if (error) {
                         var el = $(event.currentTarget);
                         //el.fileinput("reset");
                         //el.fileinput("clear");
                         //el.fileinput("setCaption", el.data("initialcaption"));
                         setTimeout(function () {
                             el.fileinput("clear");
                             el.fileinput("setCaption", el.data("initialcaption"));
                         }, 500);
                     }
                 });
             }
         });



         function couponCodeUploadSuccHandler(event, data, previewId, index) {

             var self = $(this);
             var forfield = self.attr("forfield");
             var name = data.files[0].name;
             var hidden = $(this.form[forfield]);

             var err = data.response.err;
             var formatErr = data.response.file.err;

             if (err.length > 0) {
                 alert("Invalid file format. File for Coupon Code must be in csv format." + err);
             } else if (formatErr.length > 0) {
                 alert(formatErr);
             }else {
                 var UUID = data.response.file["UUID"];

                 hidden.val(UUID);

                 if (hidden.valid)
                     hidden.valid();

                 setTimeout(function () {
                     var fileinput = self.data("fileinput");
                     fileinput.setCaption(name);
                 }, 1000);

                 //var img = hidden.siblings(".help-inline").find("img");              
                 //img.attr("src", $.format(thumbnailPath, UUID));
                 //img.parent("a").attr("href", $.format(thumbnailPath, UUID));
             }
         }

    //couponcodelistfileupload 
    // 该上传功能仅允许上传CouponCodeList文件。
    //(function () {
        fileuploadTags = $(".couponcodelistfileupload");
        //thumbnailPath = '/SysAttachment/ViewThumbnail/{0}';

        fileuploadTags.each(function (i, el) {

            var self = $(el);
            var forfield = self.attr("forfield");
            //console.log(forfield);

            var find = $.format("input[name={0}]", forfield);

            var input = $(find);
            //var img = input.siblings(".help-inline").find("table");
            var UUID = $.trim(input.val());

            if (UUID && UUID != "0") {
                //  img.attr("src", $.format(thumbnailPath, UUID));
                //  img.parent("a").attr("href", $.format(thumbnailPath, UUID));

                //console.log(input.val(), img);
            } else if (self.data("required") == "True") {
                input.val("");
            }

            var caption = self.data("initialcaption");
            //console.log(caption);

            var couponCodeFileinput = self.fileinput({
                uploadUrl: "/CouponCodeListFileUpload.ashx",
                overwriteInitial: true,
                initialCaption: caption || "CouponCodeList To Upload",
                showPreview: false,
                //allowedFileExtensions: ['csv'], // 'image',
                //elErrorContainer: ".file-error-message",
                autoReplace: true,
                dropZoneEnabled: false,
                showUpload: true,
                maxFileSize: 204800,
                maxFileCount: 1,
                maxFileNum: 1,
                removeLabel: "",
                uploadLabel: "",
                browseLabel: "",
                browseClass: "btn btn-default",
                previewClass: "previewIcon",
                layoutTemplates: {
                    main1:
                        "<div class=\'input-group {class}\'>\n" +
                            "   {caption}\n" +
                            "   <div class=\'input-group-btn\'>\n" +
                            "       {browse}\n" +
                            "       {upload}\n" +
                            "       {remove}\n" +
                            "   </div>\n" +
                            "   {preview}" +
                        "</div>\n"
                },
                previewSettings: {
                    image: { width: "auto", height: "30px" }
                },
                defaultPreviewSettings: {
                    image: { width: "60px", height: "30px" }
                }
            });

            if (couponCodeFileinput) {
                couponCodeFileinput.on("filebatchuploadsuccess", couponCodeUploadSuccHandler);


                couponCodeFileinput.on("filebatchselected", function (event, files) {
                    var error = false;
                    if (!($.endWith(files[0].name, ".csv") || $.endWith(files[0].name, ".CSV"))) {
                        error = true;
                        alert("Invalid file format. File for Coupon Code must be in csv format.");
                    } else if (files[0].size > 2048 * 1024) {
                        error = true;
                        alert("Invalid file format. Coupon Code file must be csv format and size smaller than 2M.");
                    }
                    if (error) {
                        var el = $(event.currentTarget);
                        //el.fileinput("reset");
                        //el.fileinput("clear");
                        //el.fileinput("setCaption", el.data("initialcaption"));
                        setTimeout(function () {
                            el.fileinput("clear");
                            el.fileinput("setCaption", el.data("initialcaption"));
                        }, 500);
                    }
                });

            }
        });
    }
});
function CheckCsvMemberNosInCRM() 
{
    if ($("#Type").val() == "Membership Card" &&  $("#MemberListTable tbody tr").length > 0)
    {
        var memberNos = "";
        $("#MemberListTable tbody tr td:first-child").each(function (el) {
            memberNos += $(this).text() + ",";
        });
        $.ajax("/PMS/Pass/CheckCsvMemberNosInCRM", {
            data: $.param({ memberNos: memberNos }),
            type: "POST",
            dataType: "JSON",
            success: function (data) {
                if (data != null && !data.status) {
                    //alert(data);
                    $(".modal-body").text(data.data);
                    $("#modaldialog").modal({ backdrop: "static" });
                    $('#modaldialog').on('hidden.bs.modal', function () {
                        $("#Save").prop("disabled", true);
                    });
                    return false;
                }
                $("#Save").prop("disabled", false);
                return true;
            },
            error: function (errorMsg) {
                return false;
            }
        });
    }
    $("#Save").prop("disabled", false);
    return true;
}
//dataRequireField: PMS_PassTemplate.RequireField. ex.NextLevel,Bonus
//templateRequireField: Web.config fields. ex. "Bonus,BonusPoint,I.T TOKEN,STORE VALUE,Spending,Last 3 Months, etc.
//templateType: the selection from template
function CheckRequireField(dataRequireField, templateRequireField, templateType) {
    if ((templateType == "Membership Card" || templateType == "Non-Campaign Coupon") && dataRequireField.trim().length > 0) {
        var arrRequireField = dataRequireField.split(",");
        var arrTemplateRequireField = templateRequireField.split(",");
        for (var i = 0; i < arrRequireField.length; i++) {
            for (var j = 0; j < arrTemplateRequireField.length; j++) {
                if (arrTemplateRequireField[j] == arrRequireField[i]) {
                    break;
                } else if (j == arrTemplateRequireField.length - 1) {
                    return true;
                }
            }
        }
        return false;
    }
    return false;
}