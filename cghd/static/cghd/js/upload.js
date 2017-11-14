$(document).ready(function(){
	$('#btnSubmit').click(function(){
		$("#preview").html('');
		$("#preview").html('<img src="loader.gif"alt="Uploading...."/>');
		$("#formExcelUpload").ajaxForm({
			target: '#preview'
		}).submit();
	});
});