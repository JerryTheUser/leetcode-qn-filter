$(document).ready(function(){

    data = { "likes" : 0 , "limits" : 10};

    $("#likes").change(function(e){
        data['likes'] = $('#likes').val();
        $.ajax({
            url:"{{ url_for('filter') }}",
            type:'POST',
            data: data,
            success:function(reponse){
            alert("Success");
            $('#replacement').html(reponse);
            },
            error:function(e){
            alert("Fail");
            }
        })
    });

    $("#limits").change(function(e){
        data['limits'] = $('#limits').val();
        $.ajax({
        url: "{{ url_for('filter') }}",
        type: 'POST',
        data: data,
        success:function(reponse){
            alert("Success");
            $('#replacement').html(reponse);
        },
        error:function(e){
            alert("Fail");
        }
        });
    });

});