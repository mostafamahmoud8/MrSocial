$(document).ready(function(){
 
    $('button.login , button.signup').hover(function(){

          $(this).css({'border-color':'#66ff33','background-color':'whitesmoke'});
          $(this).children('a').css({'color':'#66ff33'});
      },
      function(){
          $(this).css({'border-color':'whitesmoke','background-color':'#66ff33'});
          $(this).children('a').css({'color':'whitesmoke'});
      });
    
    $('button.open').click(function(){
        
         $(this).css({'display':'none'});
         $('button.close').css({'display':'block'});
         $('#sidemenu').css({'width':'20%'});
         $('#content').css({'margin-left':'20%'});
         
    });
    $('button.close').click(function(){
        
        $(this).css({'display':'none'});
        $('button.open').css({'display':'block'});
        $('#sidemenu').css({'width':'0%'});
        $('#content').css({'margin-left':'0%'});
        
   });
});