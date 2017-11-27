$(document).ready(function(){
	var vPP, vPQ, vSP, vSQ, vLP, vLQ, vCurr = 0;
	var ppFlag, pqFlag, spFlag, sqFlag, lpFlag, lqFlag = false;
	$('#divResult').on('change', '.table tr td.dbclicktd', function(){
		$this = $(this);
		if($.isNumeric($this.find('input:text').val())){
			vCurr = Number($this.find('input:text').val());
			switch($this.attr('class')){
				case "dbclicktd pp":
					ppFlag = true;
					vPP = vCurr;
					break;
				case "dbclicktd pq":						
					pqFlag = true;
					vPQ = vCurr;
					break;
				case "dbclicktd sp":
					spFlag = true;
					vSP = vCurr;
					break;
				case "dbclicktd sq":
					sqFlag = true;
					vSQ = vCurr;
					break;
				case "dbclicktd lp":
					lpFlag = true;
					vLP = vCurr;
					break;
				case "dbclicktd lq":
					lqFlag = true;
					vLQ = vCurr;
					break;
			}
		}else{
			alert('请输入整数或小数')
			$this.find('input:text').focus().select();
			return false;
		}

		$this.siblings('td.dbclicktd').each(function(i, item){
			if($.isNumeric($(item).text())){
				vCurr = Number($(item).text());
				switch($(item).attr('class')){
					case "dbclicktd pp":
						ppFlag = true;
						vPP = vCurr;
						break;
					case "dbclicktd pq":						
						pqFlag = true;
						vPQ = vCurr;
						break;
					case "dbclicktd sp":
						spFlag = true;
						vSP = vCurr;
						break;
					case "dbclicktd sq":
						sqFlag = true;
						vSQ= vCurr;
						break;
					case "dbclicktd lp":
						lpFlag = true;
						vLP= vCurr;
						break;
					case "dbclicktd lq":
						lqFlag = true;
						vLQ= vCurr;
						break;
				}
			}
			console.log(i);

			console.log($(item).text());
		});

		if(ppFlag && pqFlag && spFlag && sqFlag && lpFlag && lqFlag){
			var md = (vSP*vSQ -vPP*vPQ - vLP*vLQ);
			var dd = 0;
			if(vSQ>0){
				dd = (md / vSQ).toFixed(2);
			}
			
			$this.siblings('td.md').text(md);
			$this.siblings('td.dd').text(dd);
		}
	});
	// 毛差=（销售结算价*销售结算量）-（采购结算价*采购结算量）-（物流结算价*物流结算量）
	// 吨毛差=毛差/销售结算量    	
	$("#btnQuery").click(function(){
		var salesNo = $('#txtSalesNo').val();
		var area = $('#txtArea').val();
		var sourceAddress = $('#txtSourceAddress').val();
		var unloadDate = $('#txtUnloadDate').val();
		var salesMen = $('#txtSales').val();
		var clientType = $('#txtClientType').val();
		var salesDate = $('#txtSalesDate').val();
		var supplier = $('#txtSupplier').val();

		$.ajax({
			url:'/cghd/getorderinfo',
			type: 'get',
			data: {'salesNo': salesNo, 'area': area, 'sourceAddress': sourceAddress, 'unloadDate': unloadDate, 'salesMen': salesMen, 'clientType': clientType, 'salesDate': salesDate, 'supplier': supplier},
			datatype: 'json',
			success:function(data){
			var data = eval('(' + data + ')');
			var table = '<table class="table table-striped"> '+
					'<tr> '+
						'<th>销售单号</th>'+
						'<th>区域</th>'+
						'<th>客户性质</th>'+
						'<th>客户类型</th>'+
						'<th>客户名称</th>'+
						'<th>卸货日期</th>'+
						'<th>卸货时间</th>'+
						'<th>卸货地址</th>'+							
						// '<th>供应商ID</th>'+
						'<th>供应商</th>'+
						'<th>气源地</th>'+
						'<th>票制</th>'+
						// '<th>承运商ID</th>'+
						'<th>毛利</th>'+							
						'<th>挂牌价格</th>'+
						'<th>采购单价</th>'+
						'<th>销售单价</th>'+
						'<th>运输单价</th>'+
						'<th>吨公里价</th>'+
						'<th>运输距离</th>'+
						'<th>承运公司</th>'+
						'<th>装货日期</th>'+
						'<th>牵引车号</th>'+
						'<th>槽罐车号</th>'+
						'<th class="dbclicktd pq">采购结算量</th>'+
						'<th class="dbclicktd pp">采购结算价</th>'+
						'<th class="dbclicktd sq">销售结算量</th>'+
						'<th class="dbclicktd sp">销售结算价</th>'+
						'<th class="dbclicktd lq">物流结算量</th>'+
						'<th class="dbclicktd lp">物流结算价</th>'+
						'<th>销售员</th>'+
						'<th class="md">毛差</th>'+
						'<th class="dd">吨毛差</th>'+						
						'<th>备注</th>'+
						'<th style="display:none;">id</th>'+
					'</tr> ';
		    for(var i=0; i<data.length; i++) {
		    	var fPoQty= Number(data[i]["PO_QTY"]);
		    	var fPoPrice= Number(data[i]["PO_Price"]);
		    	var fSalesQty= Number(data[i]["Sales_QTY"]);
		    	var fSalesPrice= Number(data[i]["Sales_Price"]);
		    	var fLogisticsQty= Number(data[i]["Logistics_QTY"]);
		    	var fLogisticsPrice= Number(data[i]["Logistics_Price"]);	

		    	var fMDeviation = fSalesPrice*fSalesQty -fPoPrice*fPoQty -fLogisticsPrice*fLogisticsQty;

		    	var fDDeviation = 0;//fMDeviation/fSalesQty;
		    	if(Number(fSalesQty)>0)
		    		fDDeviation = (fMDeviation/fSalesQty).toFixed(3);

				table += '<tr> '+
						'<td>' + data[i]["Order_No"] + '</td>'+
						'<td>' + data[i]["Area"] + '</td>'+
						'<td>' + data[i]["In_Out"] + '</td>'+
						// '<td>' + data[i]["C_ID"] + '</td>'+
						'<td>' + data[i]["C_Type"] + '</td>'+
						'<td>' + data[i]["C_BriefName"] + '</td>'+
						'<td>' + data[i]["Unload_Date"] + '</td>'+
						'<td>' + data[i]["Unload_Time"] + '</td>'+
						'<td>' + data[i]["Unload_Address"] + '</td>'+
						'<td>' + data[i]["S_BriefName"] + '</td>'+
						'<td>' + data[i]["Source_Address"] + '</td>'+
						'<td>' + data[i]["Trade_Type"] + '</td>'+
						'<td>' + data[i]["Gap_Price"] + '</td>'+
						'<td>' + data[i]["GP_Price"] + '</td>'+
						'<td>' + data[i]["CG_Price"] + '</td>'+
						'<td>' + data[i]["Sales_Price"] + '</td>'+
						'<td>' + data[i]["Transport_Price"] + '</td>'+
						'<td>' + data[i]["DGL_Price"] + '</td>'+
						'<td>' + data[i]["Transport_Distance"] + '</td>'+
						'<td>' + data[i]["Carrier_BriefName"] + '</td>'+
						'<td>' + data[i]["Load_Date"] + '</td>'+
						'<td>' + data[i]["Tractor_No"] + '</td>'+
						'<td>' + data[i]["Tank_No"] + '</td>'+
						'<td class="dbclicktd pq">' + fPoQty + '</td>'+
						'<td class="dbclicktd pp">' + fPoPrice + '</td>'+
						'<td class="dbclicktd sq">' + fSalesQty + '</td>'+
						'<td class="dbclicktd sp">' + fSalesPrice + '</td>'+
						'<td class="dbclicktd lq">' + fLogisticsQty + '</td>'+
						'<td class="dbclicktd lp">' + fLogisticsPrice + '</td>'+
						'<td>' + data[i]["Salesmen"] + '</td>'+
						'<td class="md">' + fMDeviation + '</td>'+
						'<td class="dd">' + fDDeviation + '</td>'+
						'<td>' + data[i]["Dispatch_Mark"] + '</td>'+
						'<td style="display:none;">' + data[i]["id"] + '</td>'+
					'</tr>';
			}

			table += '</table';
						
			$("#divResult").html(table);	
			$('#kv-success-1').html("查询成功, 共有 " + data.length + " 条记录");
			$('#kv-success-1').fadeIn('show').fadeOut(3000);
			},
			error:function(err){
				console.log(err);
			}
		})	   	
	});

	$('#divResult').on('change', '.table tr td.dbclicktd', function(){			
		//区分当前编辑
		//计算逻辑
		// var t1=$(this).parent().find('td.dbclicktd').get(0)
	});		
});