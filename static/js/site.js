// Make messages disappear
$('.message').closest('.message.fade').delay(5000).fadeOut(400);
// Make accordions work
$('.ui.accordion').accordion();
// Make tabs work
$('.menu .item').tab();
// Make Stickys work
$('.ui.sticky').sticky({
    context: '#follow',
    offset: 60,
    jitter: 10,
    observeChanges: true,
    pushing: true
});
// Make Login Modal work
$('.modal.login').modal({blurring: true}).modal('attach events', '.login_button', 'show');
// create sidebar and attach to menu open
$('.ui.sidebar').sidebar('attach events', '.toc.item');
// fix menu when passed
$('.masthead').visibility({
    once: false,
    onBottomPassed: function() {
        $('.fixed.menu').transition('fade in');
    },
    onBottomPassedReverse: function() {
        $('.fixed.menu').transition('fade out');
    }
});
