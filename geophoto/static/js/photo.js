
var PhotoView = BaseView.extend({
    el: '#main',
    template: $("#photoview_templ").html(),
    initialize: function (id) {
        BaseView.prototype.initialize.call(this);
        $('img#photo').attr('src',photos[id].src);
    },
    render: function(){
        BaseView.prototype.render.call(this);
    }
});
