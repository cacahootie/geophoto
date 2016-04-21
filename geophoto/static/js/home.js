
var HomeView = BaseView.extend({
    el: '#main',
    template: $("#home_templ").html(),
    initialize: function () {
        BaseView.prototype.initialize.call(this);
        var subviews = [];
        $.getJSON('/articles/', function (d) {
        	_.forEach(d['results'], function (dd) {
        		subviews.push(new HomeItem('#home-items', dd));
        	});
        });
    }
});

var HomeItem = BaseView.extend({
	template: $("#home_item_templ").html(),
    initialize: function (parent, data) {
    	this.parent = parent;
    	this.data = data;
        BaseView.prototype.initialize.call(this);
    }
})