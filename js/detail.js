function hrefBack() {
    history.go(-1);
}

function decodeQuery() {
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function (result, item) {
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function () {
    var id = decodeQuery()['id'];
    $.get('/api/v1/house/' + id, function (data) {
        var html = template('detail', {house: data.house, facility_list: data.facility_list});
        $('#house_detail').html(html);
        //图片播放
        var mySwiper = new Swiper('.swiper-container', {
            loop: true,
            autoplay: 2000,
            autoplayDisableOnInteraction: false,
            pagination: '.swiper-pagination',
            paginationType: 'fraction'
        });
        //判断是否显示预订按钮
        if(data.booking==1){
            $(".book-house").show();
        }
    });
})