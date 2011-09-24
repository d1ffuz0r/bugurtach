$(document).ready(function($) {
    $("#face").click(function(){
        alert('Problem, officer?');
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
            success: function(data){
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
            success: function(data){
                $('#likes_'+id).html(data.likes);
                alert(data.message);
            }
        });
    });

    /* add comment */
    $("#add_post").click(function(){
        var text = $('#text').val();
        $.ajax({
            type : "POST",
            url  : '/ajax/add_comment/',
            data : ({
                'csrfmiddlewaretoken' : $('[name="csrfmiddlewaretoken"]').val(),
                'bugurt' : $('#bugurt').val(),
                'text' : text
            }),
            success: function(data){
                if(data.message){
                    alert(data.message);
                }
                if(data.comment){
                    var c = data.comment;
                    $('#comments').append('<li>'+c.author+c.text+c.date+'</li>');
                }
            }
        });
    });
});
