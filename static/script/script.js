$(document).ready(function(){ 
    $('button.login , button.signup').hover(function(){

          $(this).css({'border-color':'#66ff33','background-color':'whitesmoke'});
          $(this).children('a').css({'color':'#66ff33'});
      },
      function(){
          $(this).css({'border-color':'whitesmoke','background-color':'#66ff33'});
          $(this).children('a').css({'color':'whitesmoke'});
    });

    $('button.logout').hover(function(){

        $(this).css({'border-color':'whitesmoke','background-color':'#c93a3a'});
        $(this).children('a').css({'color':'whitesmoke'});
    },
    function(){
        $(this).css({'border-color':'#bf1f1f','background-color':'whitesmoke'});
        $(this).children('a').css({'color':'#c93a3a'});
    });

    $('button.open').click(function(){
        
         $(this).css({'display':'none'});
         $('button.close').css({'display':'block'});
         $('#sidemenu').css({'width':'20%'});
         $('#content').css({'margin-left':'20%'});
         $('#navbar').css({'width':'80%'});
    });
    $('button.close').click(function(){
        
        $(this).css({'display':'none'});
        $('button.open').css({'display':'block'});
        $('#sidemenu').css({'width':'0%'});
        $('#content').css({'margin-left':'0%'});
        $('#navbar').css({'width':'100%'});   
   });
   $('button.sent').click(function(){
        $(this).css({'opacity':'1'})
        $('button.recieved').css({'opacity':'0.7'})
        $('div.recivedrequests').hide();   
        $('div.sentrequests').show();
    });
   $('button.recieved').click(function(){
        $(this).css({'opacity':'1'})
        $('button.sent').css({'opacity':'0.7'})
        $('div.sentrequests').hide();
        $('div.recivedrequests').show();   
    });
   $('span.imgdelete').click(function()
   { 
       $('div.imagepreview').css('display','none');
       $('div.imagepreview img').attr({'src':''});
       $("#imageinput").val(null);
   });
   $('span.profileimgdelete').click(function()
   { 
       var val = $('#sidemenu div.profileimage img').attr('src')
       $('div.profileimagepreview img').attr({'src':val});
       $('span.profileimgdelete').css({'display':'none'});
       $("#profileimageinput").val(null);
   });
   $("#imageinput").change(function() {
       readURL(this,"#imageinput");
    });
    $("#profileimageinput").change(function() {

        $('span.profileimgdelete').css({'display':'block'});
        readURL(this,"#profileimageinput");
    });

   $(' div.profilesetting span.settingicon').click(function()
   {
       $('div.profilesetting  div.options').slideToggle();
   });
   $(' div.groupsetting span.settingicon').click(function()
   {
       $('div.groupsetting  div.options').slideToggle();
   }); 
});

function deleteimage(id,fileinputid,checkbox)
{
    $('#'+id).css('display','none');
    $('#'+fileinputid).val(null);
    $('#'+checkbox).attr('checked',true)
}
function clearfileinput(id,fileinputid,tx=null)
{
    if(tx !== null)
    {
       var val = $('div.group div.groupimage img').attr('src')
       $('div.groupimagepreview img').attr({'src':val});
       $('div.groupimagepreview span.groupimgdelete').css({'display':'none'});
       $("#groupimageinput").val(null);
    }else
    {
        $('#'+id).css('display','none');
        $('#'+fileinputid).val(null);
    }
}
function readURL(input,id) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            if (id =="#imageinput")
            {
                $('div.imagepreview').css('display','block');
                $('div.imagepreview img').attr({'src':e.target.result});
            }
            else
            {
                $('div.profileimagepreview img').attr({'src':e.target.result});
            }
        }
        reader.readAsDataURL(input.files[0]);
   }
}
function readimageURL(input,id)
{
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            if(id == "groupimageinput")
            {
                $('div.groupimagepreview').css('display','block');
                $('div.groupimagepreview img').attr({'src':e.target.result}); 
            }else
            {
                $('#'+id).css('display','block');
                $('#'+id+' img').attr({'src':e.target.result});
            }
        }
        reader.readAsDataURL(input.files[0]);
   }
}
function udpateimageURL(input)
{
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            
            $('div.updategroup span.groupimgdelete').css('display','block');
            $('div.groupimagepreview img').attr({'src':e.target.result}); 
        }
        reader.readAsDataURL(input.files[0]);
   }
}