$(function() {
    $(document).on("click", ".make-default", function(e) {
        e.preventDefault();

        var id = $(this).attr('data-id');
        var url = '/my_account/make/address/' + id + '/default/';

        $.ajax({
            type: "GET",
            url: url,

            success: function(data) {
                $("#panel-" + data.old_id).removeClass("panel-primary").addClass("panel-info");
                $("#default-button-" + data.old_id).addClass("make-default").text("Make Default");

                $("#panel-" + data.new_id).removeClass("panel-info").addClass("panel-primary");
                $("#default-button-" + data.new_id).removeClass("make-default").text("Default");

            }
        });
    });
});