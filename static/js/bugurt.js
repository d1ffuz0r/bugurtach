$(document).ready(function($) {
    $("#face").click(function(){
        alert('Problem, officer?');
    });

    /* like */
    $(".like").live('click', function(){
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
    $(".dislike").live('click', function(){
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
    $("#add_post").live('click', function(){
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
                else{
                    var c = data.comment;
                    $('#comments').append('<li>'+c.author+c.text+c.date+'</li>');
                }
            }
        });
    });

    /* delete tag */
    $(".delete_tag").live('click', function(){
        var tag = parseInt(this.id);
        $.ajax({
            type: "POST",
            url: "/ajax/delete_tag/",
            data: ({
                'csrfmiddlewaretoken' : $('[name="csrfmiddlewaretoken"]').val(),
                'bugurt': $('#bugurt').val(),
                'tag': tag
            }),
            success: function(){
                console.log(tag);
                $("#tag_"+tag).remove();
            }
        });
    });

    /* add tag */
    $(".add_tag").live('click', function(){
        $.ajax({
            type: "POST",
            url: "/ajax/add_tag/",
            data: ({
                'csrfmiddlewaretoken' : $('[name="csrfmiddlewaretoken"]').val(),
                'bugurt': $('#bugurt').val(),
                'tag': $('#id_title').val()
            }),
            success: function(data){
                if(data.message){
                    alert(data.message)
                }
                else{
                    $('#id_title').val('');
                    $("#tags").append('<li id="tag_'+data.id+'"><a>'+data.tag+'</a>:\
                    <span id="'+data.id+'" class="delete_tag">удалить</span></li>');
                }
            }
        });
    });
});