$("#btnCreate").click(function(){
 	// 1.验证
	var flag = true;
	$("input.required").each(function(i, item){
		var itemText = $(item).val().trim();
		if(itemText.length<=0){
			$(item).parent().addClass("has-error");
			flag = false;
			// return false;
		}else {
		    $(item).parent().removeClass("has-error");
		}
	});
	if(!flag){
	  $("#kv-error-1").html("请务必填写上述所有内容").show();
	  return false;
	}

 	if(!$.isNumeric($('#txtDGLPrice').val())){
 		alert("吨公里价只能是整数或小数");
 		$('#txtDGLPrice').focus().select();
 		return false;
 	}
 	// 2.业务 	
 	$("#btnCreate").prop("disabled", "disabled");
 	buildData();
 	$("#btnCreate").prop("disabled", false);
});
 
function buildData(){
	var d = new Date();
	var year = d.getFullYear();
	var month = d.getMonth() + 1;
	var day = d.getDate();
	var sMonth = ("00"+month.toString()).slice(-2);
	var sDay =  ("00"+day.toString()).slice(-2);
	var now = year.toString() + sMonth + sDay;

	var th = '<table id="table1" class="table table-striped"> '+
			'<tr> '+
				'<th>销售单号</th> '+
				'<th>区域</th> '+
				'<th>客户性质</th> '+
				'<th>客户类型</th> '+
				'<th>客户名称</th> '+
				'<th style="display:none;">客户ID</th> '+
				'<th>卸气地址</th> '+
				'<th class="dbclicktd">卸货日期</th> '+
				'<th class="dbclicktd">卸货时间</th> '+
				'<th>供应商</th> '+
				'<th style="display:none;">供应商ID</th> '+
				'<th>气源</th> '+
				'<th>票制</th> '+
				'<th>毛利</th> '+
				'<th>挂牌价格</th> '+
				'<th>采购单价</th> '+
				'<th>销售单价</th> '+
				'<th>运输单价</th> '+
				'<th>吨公里价</th> '+
				'<th>运输距离</th> '+
				'<th>吨分卸费</th> '+
				'<th>销售员</th> '+
				'<th>下单日期</th> '+
				'<th>订单状态</th> '+
				'<th>备注</th> '+
			'</tr> ';
	
	var salesNo = now + "0001";
 	var area = "华东";
 	var inOut = "外部";
 	var clientType = "城市燃气";
 	var clientName = $("#txtClientName").val();
 	var clientID = "Client00001";
 	var unloadAddress = $("#txtUnloadAddress").val();
 	var unloadDate = $("#txtUnloadDate").val();
 	var unloadTime = $("#txtUnloadTime").val();
 	var supplier = $("#txtSupplier").val();
 	var supplierID = "Supplier00001";
 	var sourceAddress = $("#txtSourceAddress").val();
 	var tradeType = $("#selTradeType").val();
 	
 	var gpPrice = $("#txtGPPrice").val();
 	var poPrice = $("#txtPOPrice").val();
 	var salesPrice = $("#txtSalesPrice").val();
 	
 	var dglPrice = $("#txtDGLPrice").val();
 	var yjDistance = $("#txtYJDistance").val();
 	var dfxCost = $("#txtDFXCost").val();
 	// 运输单价=（吨公里价*运输距离）+吨分卸费
 	var ysPrice = (dglPrice * yjDistance) + Number(dfxCost) ;
 	// 毛利 = 销售单价-采购单价-运输单价
 	var gapPrice = salesPrice - poPrice - ysPrice;
 	var sales = $("#txtSales").val();
 	var createDate = year.toString() + "-" + sMonth + "-" + sDay;
 	var status = "有效";
 	var remark = $("#txtDispatchMark").val();
	var table = $("#table1") || [];
	
	if(table.length>0){
		salesNo = now + ("0000" + $("#table1 tr").length.toString()).slice(-4);
	}
	tr = '<tr> '+
				'<td>' + salesNo + '</td>' +
				'<td>' + area + '</td>' +
				'<td>' + inOut + '</td>' +
				'<td>' + clientType + '</td>' +
				'<td style="display:none;">' + clientID + '</td>' +
				'<td>' + clientName + '</td>' +
				'<td>' + unloadAddress + '</td>' +
				'<td class="dbclicktd">' + unloadDate + '</td>' +
				'<td class="dbclicktd">' + unloadTime + '</td>' +
				'<td style="display:none;">' + supplierID + '</td>' +
				'<td>' + supplier + '</td>' +
				'<td>' + sourceAddress + '</td>' +
				'<td>' + tradeType + '</td>' +
				'<td>' + gapPrice + '</td>' +
				'<td>' + gpPrice + '</td>' +
				'<td>' + poPrice + '</td>' +
				'<td>' + salesPrice + '</td>' +
				'<td>' + ysPrice + '</td>' +
				'<td>' + dglPrice + '</td>' +
				'<td>' + yjDistance + '</td>' +
				'<td>' + dfxCost + '</td>' +
				'<td>' + sales + '</td>' +
				'<td>' + createDate + '</td>' +
				'<td>' + status + '</td>' +
				'<td>' + remark + '</td>' +
		'</tr> ';
	if (table.length > 0){
		table = $("#table1").append(tr);
	}else{
		table = th + tr + '</table';
	}

	$("#divResult").html(table);	
	$("#hiddenData").val($("#divResult").html());
	$('#kv-success-1').html("创建订单成功");
	$('#kv-success-1').fadeIn('show').fadeOut(3000);
}