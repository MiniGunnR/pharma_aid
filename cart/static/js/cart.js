$(function() {
    $(document).on("click", ".list-item-button", function(e) {
        e.preventDefault();

        var slug = $(this).attr('data-slug');
        var url = '/cart/add/' + slug + '/';

        $.ajax({
            type: "GET",
            url: url,

            success: function(data) {
                $("#" + slug + "_quantity_in_bag").text(data.quantity);
                $("#" + slug + "_total").text(data.total);

                $("#bag-item-number").html(data.total_item);
                $("#bag-taka-number").html(data.total_taka);
                $("#big-bag-item-number").html(data.total_item);
                $("#big-bag-taka-number").html(data.total_taka);

                if ($("#cart-item-" + data.cart_item_id).length == 0) {
                    $("#big-bag-body").append('<div class="bag-item" id="cart-item-' + data.cart_item_id + '"> \
                                                    <div class="left-control"> \
                                                        <div class="qty_up" data-slug="' + slug + '"><center><i class="fa fa-sort-up left-control-button"></i></center></div> \
                                                        <div class="quantity"><center id="' + slug + '_quantity_in_bag">' + data.quantity + '</center></div> \
                                                        <div class="qty_down" data-slug="' + slug + '"><center><i class="fa fa-sort-down left-control-button"></i></center></div> \
                                                    </div> \
                                                    <div class="product_img"><img src="https://placeholdit.imgix.net/~text?&w=30&h=30"/></div> \
                                                    <div class="product_details"> \
                                                        <div class="product_name">' + data.cart_item_name + '</div> \
                                                        <div class="product_price"> \
                                                            <small>Tk. ' + data.cart_item_price + ' / box</small> \
                                                        </div> \
                                                    </div> \
                                                    <div class="total" id="' + slug + '_total">' + data.total + '</div> \
                                                    <div class="remove cart-item-remove" data-slug="' + slug + '"> \
                                                        <i class="fa fa-close"></i> \
                                                    </div> \
                                                </div>');
                    }
            }
        });
    });

    $(document).on("click", ".qty_up", function(e) {
        e.preventDefault();

        var slug = $(this).attr('data-slug');
        var url = '/cart/add/' + slug + '/';

        $.ajax({
            type: "GET",
            url: url,

            success: function(data) {
                $("#" + slug + "_quantity_in_bag").text(data.quantity);
                $("#" + slug + "_total").text(data.total);

                $("#bag-item-number").html(data.total_item);
                $("#bag-taka-number").html(data.total_taka);
                $("#big-bag-item-number").html(data.total_item);
                $("#big-bag-taka-number").html(data.total_taka);
            }
        })
    });

    $(document).on("click", ".qty_down", function(e) {
        e.preventDefault();

        var slug = $(this).attr('data-slug');
        var url = '/cart/remove/' + slug + '/';

        $.ajax({
            type: "GET",
            url: url,

            success: function(data) {
                $("#" + slug + "_quantity_in_bag").text(data.quantity);
                $("#" + slug + "_total").text(data.total);

                $("#bag-item-number").html(data.total_item);
                $("#bag-taka-number").html(data.total_taka);
                $("#big-bag-item-number").html(data.total_item);
                $("#big-bag-taka-number").html(data.total_taka);
            }
        })
    });

    $(document).on("click", ".cart-item-remove", function(e) {
        e.preventDefault();

        var slug = $(this).attr('data-slug');
        var url = '/cart/delete/' + slug + '/';

        $.ajax({
            type: "GET",
            url: url,

            success: function(data) {
                $("#cart-item-" + data.item_id).remove();

                $("#bag-item-number").html(data.total_item);
                $("#bag-taka-number").html(data.total_taka);
                $("#big-bag-item-number").html(data.total_item);
                $("#big-bag-taka-number").html(data.total_taka);
            }
        })
    });

    $(document).on("click", ".add-to-bag", function(e) {
        e.preventDefault();

        var slug = $(this).attr('data-slug');
        var url = '/cart/add/' + slug + '/';

        $.ajax({
            type: "GET",
            url: url,

            success: function(data) {
                $("#" + slug + "_quantity_in_bag").text(data.quantity);
                $("#" + slug + "_total").text(data.total);

                $("#bag-item-number").html(data.total_item);
                $("#bag-taka-number").html(data.total_taka);
                $("#big-bag-item-number").html(data.total_item);
                $("#big-bag-taka-number").html(data.total_taka);

                if ($("#cart-item-" + data.cart_item_id).length == 0) {
                    $("#big-bag-body").append('<div class="bag-item" id="cart-item-' + data.cart_item_id + '"> \
                                                    <div class="left-control"> \
                                                        <div class="qty_up" data-slug="' + slug + '"><center><i class="fa fa-sort-up left-control-button"></i></center></div> \
                                                        <div class="quantity"><center id="' + slug + '_quantity_in_bag">' + data.quantity + '</center></div> \
                                                        <div class="qty_down" data-slug="' + slug + '"><center><i class="fa fa-sort-down left-control-button"></i></center></div> \
                                                    </div> \
                                                    <div class="product_img"><img src="https://placeholdit.imgix.net/~text?&w=30&h=30"/></div> \
                                                    <div class="product_details"> \
                                                        <div class="product_name">' + data.cart_item_name + '</div> \
                                                        <div class="product_price"> \
                                                            <small>Tk. ' + data.cart_item_price + ' / box</small> \
                                                        </div> \
                                                    </div> \
                                                    <div class="total" id="' + slug + '_total">' + data.total + '</div> \
                                                    <div class="remove cart-item-remove" data-slug="' + slug + '"> \
                                                        <i class="fa fa-close"></i> \
                                                    </div> \
                                                </div>');
                    }
            }
        });
    });

    $(document).on("click", ".add-to-monthly-btn", function(e) {
        e.preventDefault();

        var slug = $(this).attr('data-slug');
        var url = '/cart/add/to/monthly/' + slug + '/';

        $.ajax({
            type: "GET",
            url: url,

            success: function(data) {
                $("#added_msg").toggle().fadeOut(800);
            }
        });
    });

    $(document).on("click", ".add-to-monthly", function(e) {
        e.preventDefault();

        var slug = $(this).attr('data-slug');
        var url = $(this).attr('href');

        $.ajax({
            type: "GET",
            url: url,

            success: function(data) {
                $("#" + data.id + "_quantity").text(data.quantity);
                $("#" + data.id + "_total").text(data.total);
                $("#all_total").text(data.all_total);
            }
        });
    });

    $(document).on("click", ".remove-from-monthly", function(e) {
        e.preventDefault();

        var slug = $(this).attr('data-slug');
        var url = $(this).attr('href');

        $.ajax({
            type: "GET",
            url: url,

            success: function(data) {
                $("#" + data.id + "_quantity").text(data.quantity);
                $("#" + data.id + "_total").text(data.total);
                $("#all_total").text(data.all_total);
            }
        });
    });

    $(document).on("click", ".delete-from-monthly", function(e) {
        e.preventDefault();

        var slug = $(this).attr('data-slug');
        var url = $(this).attr('href');

        $.ajax({
            type: 'GET',
            url: url,

            success: function(data) {
                $("#monthly-item-" + data.id).remove();
                $("#all_total").html(data.all_total);
            }
        });
    });

    $(document).on('click', '#order_now', function(e) {
        e.preventDefault();

        var url = $(this).attr('href');

        $.ajax({
            type: "GET",
            url: url,

            success: function(data) {
                $("#bag-item-number").html(data.cart_items);
                $("#bag-taka-number").html(data.cart_total);
                $("#big-bag-item-number").html(data.cart_items);
                $("#big-bag-taka-number").html(data.cart_total);

                $.each(data.array, function(index, value) {
                    if ($("#cart-item-" + value.cart_item_id).length == 0) {
                        $("#big-bag-body").append('<div class="bag-item" id="cart-item-' + value.cart_item_id + '"> \
                                                        <div class="left-control"> \
                                                            <div class="qty_up" data-slug="' + value.slug + '"><center><i class="fa fa-sort-up left-control-button"></i></center></div> \
                                                            <div class="quantity"><center id="' + value.slug + '_quantity_in_bag">' + value.qty + '</center></div> \
                                                            <div class="qty_down" data-slug="' + value.slug + '"><center><i class="fa fa-sort-down left-control-button"></i></center></div> \
                                                        </div> \
                                                        <div class="product_img"><img src="https://placeholdit.imgix.net/~text?&w=30&h=30"/></div> \
                                                        <div class="product_details"> \
                                                            <div class="product_name">' + value.name + '</div> \
                                                            <div class="product_price"> \
                                                                <small>Tk. ' + value.price + ' / box</small> \
                                                            </div> \
                                                        </div> \
                                                        <div class="total" id="' + value.slug + '_total">' + value.total + '</div> \
                                                        <div class="remove cart-item-remove" data-slug="' + value.slug + '"> \
                                                            <i class="fa fa-close"></i> \
                                                        </div> \
                                                    </div>');
                        }
                    else {
                        $("#" + value.slug + "_quantity_in_bag").text(value.qty);
                        $("#" + value.slug + "_total").text(value.total);
                    }
                });
            }
        });
    });
});
