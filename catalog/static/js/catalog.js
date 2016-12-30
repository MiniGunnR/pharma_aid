$(function() {
    $(window).scroll(function () {

    var pathname = window.location.pathname;

    if (($(window).scrollTop() + $(window).height() == $(document).height()) && (pathname == '/category/medicine/')) {
        $.getJSON( "/more/items/medicine/", function(data) {
            for (var i = 0; i < data.length; i++) {
                var obj = data[i];
                $(
                    "<div class='list-item'> \
                        <div class='list-item-image text-center'> \
                            <a href=" + obj.fields.slug + ">\
                                <img src='/static/img/default.jpg' style='position: relative;' height='130'/>\
                            </a>\
                        </div>\
                        \
                        <div class='text-center list-item-name'>" + obj.fields.name + "</div> \
                        \
                        <div class='list-item-details text-center'> \
                            <p><b>Tk. " + obj.fields.price + "</b></p> \
                        </div> \
                        \
                        <div class='list-item-button text-center' data-slug='" + obj.fields.slug + "'> \
                            <b>ADD TO BAG</b> \
                        </div> \
                    </div>"
                ).appendTo("#items");
            }
        });
    }
    });
});
