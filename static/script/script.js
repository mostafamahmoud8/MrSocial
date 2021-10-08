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
/********************************Ajax calls goes here*******************/ 

    $('#PostForm').submit(function(e){
        e.preventDefault();
        var formdata =  new FormData(this);
        console.log(formdata);        
        $.ajax({
             url:'posts/create/',
             data:formdata,
             async:true,
             type:'POST',
             success:function(response,st,xml){
                 if(st == 'success' && xml.status == 200)
                 {
                     if(typeof response == 'string')
                     {
                        console.log(response);
                        var numberofposts = $('#sidemenu div.userinfo button.myposts').html()
                        var number = changenumbers(numberofposts,'+');
                        $('#sidemenu div.userinfo button.myposts').html(" "+number +' posts');
                        $('#PostForm div.postdone').fadeIn(1000);
                        $('#PostForm div.postdone').fadeOut(2000); 
                        $('#createdpost').html(response);
                        $('#createdpost').css({'display':'block'});
                        $('div.imagepreview').css('display','none');
                        $('#PostForm')[0].reset();
                     }else
                     {
                         if(! response.status)
                         {
                            console.log(response.errors);
                            $('#PostForm div.posterrors').fadeIn(1000);
                            $('#PostForm div.posterrors').html(response.errors);
                            $('#PostForm div.posterrors').fadeOut(2000); 
                         }
                     }
                }            
             },
             processData: false,
             contentType: false,
        });
    });
});
function changenumbers(word,action)
{
    var numbers = word.match(/(\d+)/);
    if(action == '+')
    {
        var number=parseInt(numbers[0])+1;
    }else
    {
        var number=parseInt(numbers[0])-1;
    }

    return number;
}
function UpdatePost(e,action,formid,postid)
{
    e.preventDefault();
    var form  = $('#'+formid)[0];
    var formdata =  new FormData(form);
    $.ajax({
         url:action,
         data:formdata,
         async:true,
         type:'POST',
         success:function(response,st,xmlhttp){

             if(st == 'success' && xmlhttp.status == 200)
             {
                 if(response.status)
                 { 
                     post = JSON.parse(response.post);
                     if(post.content != '')
                     {
                         $('#'+postid+' div.postcontent p').html(post.content)
                     }else
                     {
                        $('#'+postid+' div.postcontent p').html('');
                     }
                     if(post.image != '')
                     {
                        img = "<img src='"+post.image+"' alt='Post Photo'>";
                        $('#'+postid+' div.postcontent div.postimage').html(img)
                     }else
                     {
                        $('#'+postid+' div.postcontent div.postimage').html('');
                     }
                     editpostid = $('#'+formid).parent().attr('id');
                     showpostaction(id=editpostid,option=null,postid=postid);
                 }else
                 {
                    $('#'+formid+' div.posterrors').fadeIn(1000);
                    $('#'+formid+' div.posterrors').html(response.errors);
                    $('#'+formid+' div.posterrors').fadeOut(2000);      
                }
             }            
         },
         processData: false,
         contentType: false,
    });
}
function DeletePost(event,action,formid,postid)
{
    console.log(action);
    event.preventDefault();
    var form  = $('#'+formid)[0];
    var formdata =  new FormData(form);
    $.ajax({
         url:action,
         data:formdata,
         async:true,
         type:'POST',
         success:function(response,st,xmlhttp){
             if(st == 'success' && xmlhttp.status == 200)
             {
                 if(response.status)
                 {
                    $('#'+postid).parent().slideUp();
                    var numberofposts = $('#sidemenu div.userinfo button.myposts').html()
                    var number = changenumbers(numberofposts,'-');
                    $('#sidemenu div.userinfo button.myposts').html(" "+number +' posts');
                    $('div.profile div.profiledata span.numposts').html(" "+number +' posts');
                 }
             }            
         },
         processData: false,
         contentType: false,
    });
}
function AddComment(event,url,commentformid,postdetailid)
{
    event.preventDefault();
    var form =  $('#'+commentformid)[0];
    var formdata =  new FormData(form);
    console.log(formdata); 
    console.log(url);   
    $.ajax({
             url:url,
             data:formdata,
             async:true,
             type:'POST',
             success:function(response,st,xml){
                 if(st == 'success' && xml.status == 200)
                 {
                     if(typeof response == 'string')
                     {
                        console.log(response);
                        var numberofcomment = $('#'+postdetailid+' div.postreach div.right span.commentcount').html()
                        var number = changenumbers(numberofcomment,'+');
                        $('#'+postdetailid+' div.postreach div.right span.commentcount').html(' '+number+' comment')
                        var comments=$('#'+postdetailid+' div.comments div.comment').html()
                        $('#'+postdetailid+' div.comments div.comment').html(response+comments)

                        $('#'+commentformid)[0].reset()
                
                     }else
                     {
                         if(! response.status)
                         {
                            console.log(response.errors);
                            $('#'+commentformid).nextAll('div.commenterror').fadeIn(1000);
                            $('#'+commentformid).nextAll('div.commenterror').html(response.errors);
                            $('#'+commentformid).nextAll('div.commenterror').fadeOut(2000); 
                         }
                     }
                }            
             },
             processData: false,
             contentType: false,
    });
}
function UpdateComment(event,url,commentformid)
{
    event.preventDefault();
    var form =  $('#'+commentformid)[0];
    var formdata =  new FormData(form);
    console.log(formdata); 
    console.log(url);   
    $.ajax({
             url:url,
             data:formdata,
             async:true,
             type:'POST',
             success:function(response,st,xml){
                 if(st == 'success' && xml.status == 200)
                 {
                     if(response.status)
                     {
                        console.log(response);
                        updateid = $('#'+commentformid).parent().parent().attr('id');
                        detail = $('#'+updateid).parent().attr('id');
                        $('#'+detail+' div.commentcontent p').html(response.message);
                        content = $('#'+detail+' div.content').attr('id');
                        showcommentaction(updateid,options=null,content);  
                     }else
                     {
                        console.log(response.errors);
                        $('#'+commentformid).parent().nextAll('div.commenterror').fadeIn(1000);
                        $('#'+commentformid).parent().nextAll('div.commenterror').html(response.errors);
                        $('#'+commentformid).parent().nextAll('div.commenterror').fadeOut(2000); 
                     }
                }            
             },
             processData: false,
             contentType: false,
    });

}
function DeleteComment(event,url,commentformid)
{
    event.preventDefault();
    var form =  $('#'+commentformid)[0];
    var formdata =  new FormData(form);
    console.log(formdata); 
    console.log(url);   
    $.ajax({
             url:url,
             data:formdata,
             async:true,
             type:'POST',
             success:function(response,st,xml){
                 if(st == 'success' && xml.status == 200)
                 {
                     if(response.status)
                     {
                        console.log(response);
                        deleteid = $('#'+commentformid).parent().parent().attr('id');
                        detail = $('#'+deleteid).parent().attr('id');
                        $('#'+detail).remove();  
                     }
                }            
             },
             processData: false,
             contentType: false,
    });

}
function AddLike(event,url,formid,postdetailid)
{
    event.preventDefault();
    var form =  $('#'+formid)[0];
    var formdata =  new FormData(form);
    console.log(url);   
    $.ajax({
             url:url,
             data:formdata,
             async:true,
             type:'POST',
             success:function(response,st,xml){
                 if(st == 'success' && xml.status == 200)
                 {
                     if(typeof response == 'string')
                     {
                        console.log(response);
                        $('#'+postdetailid+' div.showlikes').html(response);
                        var likesnumber = $('#'+postdetailid+' div.postreach div.left span.likecount').html();
                        var number = changenumbers(likesnumber,'+');
                        $('#'+postdetailid+' div.postreach div.left span.likecount').html(number+' like');
                        $('#'+formid+' button.addlike').css({'display':'none'});
                        $('#'+formid+' button.removelike').css({'display':'block'});
                     }
                }            
             },
             processData: false,
             contentType: false,
    });
}
function RemoveLike(event,url,formid,postdetailid)
{
    event.preventDefault();
    var form =  $('#'+formid)[0];
    var formdata =  new FormData(form);
    console.log(url);   
    $.ajax({
             url:url,
             data:formdata,
             async:true,
             type:'POST',
             success:function(response,st,xml){
                 if(st == 'success' && xml.status == 200)
                 {
                     if(typeof response == 'string')
                     {
                        console.log(response);
                        $('#'+postdetailid+' div.showlikes').html(response);
                        var likesnumber = $('#'+postdetailid+' div.postreach div.left span.likecount').html();
                        var number = changenumbers(likesnumber,'-');
                        $('#'+postdetailid+' div.postreach div.left span.likecount').html(number+' like');
                        $('#'+formid+' button.addlike').css({'display':'block'});
                        $('#'+formid+' button.removelike').css({'display':'none'});
                     }
                }            
             },
             processData: false,
             contentType: false,
    });
}
function Share(event,url,formid,postdetailid,postshares)
{
    event.preventDefault();
    var form =  $('#'+formid)[0];
    var formdata =  new FormData(form);
    console.log(url);   
    $.ajax({
             url:url,
             data:formdata,
             async:true,
             type:'POST',
             success:function(response,st,xml){
                 if(st == 'success' && xml.status == 200)
                 {
                     if(typeof response == 'string')
                     {
                        console.log(response);
                        $('#'+postshares).html(response);
                        var sharesnumber = $('#'+postdetailid+' div.postreach div.right span.sharecount').html();
                        var number = changenumbers(sharesnumber,'+');
                        $('#'+postdetailid+' div.postreach div.right span.sharecount').html(number+' share');
                        $('#'+formid+' button.addshare').css({'display':'none'});
                        $('#'+formid+' button.removeshare').css({'display':'block'});
                     }
                }            
             },
             processData: false,
             contentType: false,
    });
}

function RemoveShare(event,url,formid,postdetailid,postshares)
{
    event.preventDefault();
    var form =  $('#'+formid)[0];
    var formdata =  new FormData(form);
    console.log(url);   
    $.ajax({
             url:url,
             data:formdata,
             async:true,
             type:'POST',
             success:function(response,st,xml){
                 if(st == 'success' && xml.status == 200)
                 {
                     if(typeof response == 'string')
                     {
                        console.log(response);
                        $('#'+postshares).html(response);
                        var sharesnumber = $('#'+postdetailid+' div.postreach div.right span.sharecount').html();
                        var number = changenumbers(sharesnumber,'-');
                        $('#'+postdetailid+' div.postreach div.right span.sharecount').html(number+' share');
                        $('#'+formid+' button.addshare').css({'display':'block'});
                        $('#'+formid+' button.removeshare').css({'display':'none'});
                     }
                }            
             },
             processData: false,
             contentType: false,
    });
}
function getgroupcreateform(url)
{
  console.log(url);
  $.get(url, function(data, statustext){
      if(statustext == 'success')
      {
          $('div.optionsresult').html(data);
          $('div.optionsresult').slideDown();
      }
  });
}
function CreateGroup(event,form,url)
{
    event.preventDefault();
    var form = $('#'+form)[0];
    var formdata = new FormData(form);
    console.log(url);
    $.ajax({
        url:url,
        data:formdata,
        async:true,
        type:'POST',
        success:function(response,st,xml){
            if(st == 'success' && xml.status == 200)
            {
                if(typeof response == 'string')
                {
                   console.log(response);
                    $('#groupform div.groupdone').fadeIn();
                    $('#groupform div.groupdone').fadeOut(); 
                    $('div.optionsresult').slideUp(2000);
                   
                }else
                {
                    if(! response.status)
                    {
                       console.log(response.errors);
                       $('#groupform div.grouperrors').fadeIn(1000);
                       $('#groupform div.grouperrors').html(response.errors);
                    }
                }
           }            
        },
        processData: false,
        contentType: false,
   });
}
function showprofileaction(proid,options=null,prodetail)
{
    if(options)
    {
        $('div.'+options).slideToggle();
    }
    $('div.'+prodetail).slideToggle();
    $('#'+proid).slideToggle();
}
function showpostoptions(id)
{
    console.log('#'+id);
    $('#'+id).slideToggle();
}
function showcommentoptions(id)
{
    console.log('#'+id);
   $('#'+id).slideToggle();
}
function showpostaction(id,option=null,postid=null)
{
    if(option)
    {
        showpostoptions(option);
    }
    if(postid)
    {
        $('#'+postid+' '+'div.postcontent p').slideToggle();
    }
    $('#'+id).slideToggle();
}

function showcommentaction(updateid,options=null,content)
{
   if(options)
   {
    $('#'+options).slideToggle();
   }
    $('#'+content).slideToggle();
    $('#'+updateid).slideToggle();
}
function showpostlikes(id)
{
    console.log(id);
    $('#'+id).slideToggle();
}
function showpostshares(id)
{
    $('#'+id).slideToggle();
}
function commentfocus(id)
{
    $('#'+id).focus();
}
function deleteimage(id,fileinputid,checkbox)
{
    $('#'+id).css('display','none');
    $('#'+fileinputid).val(null);
    $('#'+checkbox).attr('checked',true)
}
function clearfileinput(id,fileinputid)
{
    $('#'+id).css('display','none');
    $('#'+fileinputid).val(null);
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
            if(id == "#groupimageinput")
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