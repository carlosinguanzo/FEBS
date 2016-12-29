    $(document).ready(function() {
        $('#Rol').on('change',function(){
                if( $(this).val()==="Tendero"){
                $("#rol_form").show();
                }
                else{
                $("#rol_form").hide();
                }
            });

        $("#titulo-registro").click(function(){
            $(this).hide();
            alert( "Handler for .click() called." );
        });
    });