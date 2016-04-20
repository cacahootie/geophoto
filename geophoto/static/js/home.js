
var HomeView = BaseView.extend({
    el: '#main',
    template: $("#home_templ").html(),
    initialize: function (id) {
        BaseView.prototype.initialize.call(this);
    }
});
