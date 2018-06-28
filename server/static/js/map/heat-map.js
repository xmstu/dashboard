var setAbout = {
  init:function(){
      $('.map-menu-about>a').addClass('selected-active');
      $('.map-menu-about>a>i').addClass('select-active');
      layui.use(['form','table','layer'],function(){
          var form = layui.form;
          var table = layui.table;
          var layer = layui.layer;
      })
  }
};
$('#search_btn').click(function(e){
    e.preventDefault();
});
setAbout.init();