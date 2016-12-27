$(function() {
    $(document).on("click", "#bag", function(e) {
        e.preventDefault();

        $("#bag").attr('hidden', 'hidden');
        $("#main").css({'padding-right': 300});
        $("#big-bag").removeAttr('hidden');
    });

    $(document).on("click", "#big-bag-header", function(e) {
        e.preventDefault();

        $("#big-bag").attr('hidden', 'hidden');
        $("#main").css({'padding-right': 10});
        $("#bag").removeAttr('hidden');
    });

    $("#category_menu").on('click', function(e) {
        e.preventDefault();

        $("#sidebar").toggle().css({"z-index": "20"});
    });

    $("#mobile_menu").on('click', function(e) {
        e.preventDefault();

        $("#mobile_right_menu").toggle();
    });
});

