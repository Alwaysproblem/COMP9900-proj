function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function () {
        setTimeout(function () {
            $('.popup_con').fadeOut('fast', function () {
            });
        }, 1000)
    });
}

$(document).ready(function () {
    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        autoclose: true
    });
    $(".input-daterange").on("changeDate", function () {
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();
        var check_in = $(".check_in_date>span").html();
        var check_out = $(".check_out_date>span").html();

        if (startDate && endDate && (startDate < check_in || endDate > check_out)) {
            showErrorMsg();
        } else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd) / (1000 * 3600 * 24) + 1;
            var price = $(".price>span>span").html();
            var amount = days * parseFloat(price);
            var deposit = parseFloat(0.2 * amount);
            $(".order-amount>span").html(amount.toFixed(2) + "(total " + days + " days)");
            $(".order-deposit>span").html(deposit.toFixed(2))
        }
    });
});
