$(function(){
    $(document).on("click", ".address-button", function(e) {
        e.preventDefault();

        var id = $(this).attr('data-id');
        var url = '/order/get/address/' + id + '/';

        $.ajax({
            type: "GET",
            url: url,

            success: function(data){
                html = '<b>' + data.name + '</b> <br/> \
                        ' + data.address_1 + '<br/> \
                        ' + data.address_2 + '<br/> \
                        ' + data.city + ' - ' + data.zip + '<br/> \
                        ' + data.country;
                $("#address-info").html(html);
            }
        });
    });

    $(document).on("click", ".order-list-item", function(e) {
        e.preventDefault();

        $(".order-list-item").removeClass("active");
        $(this).toggleClass("active");

        var url = $(this).children().attr("href");

        $.ajax({
            type: "GET",
            url: url,

            success: function(data) {
                $("#order-details").html(data);

            }
        });
    });

    $('.pop').on('click', function() {
        $('.imagepreview').attr('src', $(this).find('img').attr('data-src'));
        $('#imagemodal').modal('show');
    });
});
