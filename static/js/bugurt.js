$(document).ready(function($) {
    $("#face").click(function(){
        alert('an');
    });

    /* like */
    $(".like").click(function(){
        var id = parseInt(this.id);
        $.ajax({
            type : "POST",
            url  : '/ajax/like/',
            data : ({
                'csrfmiddlewaretoken' : $('[name="csrfmiddlewaretoken"]').val(),
                'bugurt_id': id,
                'type': 'like'
            }),
            success:function(data){
                $('#likes_'+id).html(data.likes);
                alert(data.message);
            }
        });
    });

    /* dislike */
    $(".dislike").click(function(){
        var id = parseInt(this.id);
        $.ajax({
            type : "POST",
            url  : '/ajax/like/',
            data : ({
                'csrfmiddlewaretoken' : $('[name="csrfmiddlewaretoken"]').val(),
                'bugurt_id': id,
                'type': 'dislike'
            }),
            success:function(data){
                $('#likes_'+id).html(data.likes);
                alert(data.message);
            }
        });
    });
});
