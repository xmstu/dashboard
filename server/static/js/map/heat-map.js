var setAbout = {
  init:function(){
      $('.map-menu-about>a').addClass('selected-active');
      $('.map-menu-about>a>i').addClass('select-active');
      layui.use(['form','table','layer','element'],function(){
          var form = layui.form;
          var table = layui.table;
          var layer = layui.layer;
          var element = layui.element;
      })
  }
};
$('#search_btn').click(function(e){
    e.preventDefault();
});
setAbout.init();