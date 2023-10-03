$(document).ready(function(){

	$("#btn-grid").click(function(){
		$("#vue-grid").removeClass('erp-hidden');
		
		$("#vue-liste").removeClass('erp-hidden');
		$("#vue-liste").addClass('erp-hidden');		
	});

	$("#btn-liste").click(function(){
		$("#vue-liste").removeClass('erp-hidden');
		
		$("#vue-grid").removeClass('erp-hidden');
		$("#vue-grid").addClass('erp-hidden');					
	});
});