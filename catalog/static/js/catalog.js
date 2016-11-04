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
                            <div class='text-center' style='position: absolute; top: 0px;'>" + obj.fields.name + "</div> \
                        </div> \
                        <a href='/product/" + obj.fields.slug + "/'> \
                            <div class='list-item-details-button text-center'> \
                                <b>DETAILS</b> \
                            </div> \
                        </a> \
                        <div class='list-item-details text-center'> \
                            <p><b>Tk. " + obj.fields.price + "</b></p> \
                        </div> \
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