$(document).ready(function($) {
    $("#face").click(function(){
        alert('an');
    });

    /* like */
    $(".like").click(function(){
        $.ajax({
            type : "POST",
            url  : '/ajax/like/',
            data : ({
                'csrfmiddlewaretoken' : $('[name="csrfmiddlewaretoken"]').val(),
                'bugurt_id': parseInt(this.id),
                'type': 'like'
            }),
            success:function(data){
                $('#'+data.post).hide();
                alert(data.message);
            }
        });
    });

    /* dislike */
    $(".dislike").click(function(){
        $.ajax({
            type : "POST",
            url  : '/ajax/like/',
            data : ({
                'csrfmiddlewaretoken' : $('[name="csrfmiddlewaretoken"]').val(),
                'bugurt_id': parseInt(this.id),
                'type': 'dislike'
            }),
            success:function(data){
                $('#'+data.post).hide();
                alert(data.message);
            }
        });
    });
});
