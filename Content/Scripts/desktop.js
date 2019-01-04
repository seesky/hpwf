$(function(){
   $(window).resize(function(){
	  $('#desktop').portal({width:$(parent.window).width()-255});
   });
	     
   $('#desktop').portal({
	   border:false,
	   fit:false,
	   width:$(parent.window).width()-255
   });
		 
		 
   $('.data-grid tbody tr').hover(
       function(){
           $(this).addClass('data-grid-tr-over'); 
       },function(){
           $(this).removeClass('data-grid-tr-over'); 
       }
   );
         
   //initEvent();
		 
});
  

      
/**
 * 初始化事件
 */  
function initEvent(){
	//个人资料
	$('#userEdit').click(function() {
	  var userDialog=parent.easyUI.modalDialog({
		title:'个人资料',
		iconCls:'icon-person',
		width:470,
		height:385,
		url:preCurrentUserInfoEdit,
		buttons:[{
			text:'刷新',
			iconCls:'icon-reload',
			handler:function(){
				userDialog.dialog('refresh');
			}
		},{
			text:'清空',
			iconCls:'icon-chear',
			handler:function(){
				var iframeObj = userDialog.find('iframe').get(0).contentWindow;
			    iframeObj.clearForm();
			}
		},{
			text:'提交',
			iconCls:'icon-ok',
			handler:function(){
				var iframeObj = userDialog.find('iframe').get(0).contentWindow;
				
				if(!iframeObj.validSubmit()){
					 return ;
				}
						  
			    var jsonInfo = iframeObj.serializeForm();
			    
			    jsutil.defaultReq(
			      updateUserById,
			      jsonInfo,
			      function(data){
			        if(data.resultType=="success"){
			            parent.alertBox.showAlert(data.resultMsg,'info');
					    userDialog.dialog('destroy');
			        }else if(data.resultType=="failure"){
			            parent.alertBox.showAlert(data.resultMsg,'warning');
			        }else{
			            parent.alertBox.showAlert(data.resultMsg,'error');
			        }
			      }
			    );
			 }
		 }]
	   });
		    
	 });
		    
	 //密码修改
	 $('#pwdEdit').click(function () {
	     var userPwdDialog = parent.easyUI.modalDialog({
	         title: '密码修改',
	         iconCls: 'icon-pwd-change',
	         width: 475,
	         height: 179,
	         url: preCurrentUserPwdEdit,
	         buttons: [{
	             text: '清空',
	             iconCls: 'icon-chear',
	             handler: function () {
	                 var iframeObj = userPwdDialog.find('iframe').get(0).contentWindow;
	                 iframeObj.clearForm();
	             }
	         }, {
	             text: '提交',
	             iconCls: 'icon-ok',
	             handler: function () {
	                 var iframeObj = userPwdDialog.find('iframe').get(0).contentWindow;

	                 if (!iframeObj.validSubmit()) {
	                     return;
	                 }

	                 var jsonInfo = iframeObj.serializeForm();
	                 jsutil.defaultReq(
						      updateUserPasswordById,
						      jsonInfo,
						      function (data) {
						          if (data.resultType == "success") {
						              parent.alertBox.showAlert(data.resultMsg, 'info');
						              userPwdDialog.dialog('destroy');
						          } else if (data.resultType == "failure") {
						              parent.alertBox.showAlert(data.resultMsg, 'warning');
						          } else {
						              parent.alertBox.showAlert(data.resultMsg, 'error');
						          }
						      }
						   );

	             }
	         }]
	     });
	 });
		    
	//退出系统
	$('#exitSys').click(function() {
		 parent.exitSystem();
	});
}
       
 /**
 * 查看待办
 */    
function taskView(taskUrl,taskId,taskParameter){
  window.location.href=(taskUrl).replace(/\s+/g,"")+"?id="+(taskId).replace(/\s+/g,"")+"&taskParameter="+(taskParameter).replace(/\s+/g,"");
}

      