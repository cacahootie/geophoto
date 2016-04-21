var BaseView = Backbone.View.extend({
    initialize: function(){
        this.render();
    },
    data: null,
    render: function () {
        var rendered;
        if (this.data) {    
            try {
                rendered = Mustache.to_html(this.template,this.data.toJSON());
            } catch (e) {
                rendered = Mustache.to_html(this.template,this.data);
            }  
        } else {
            rendered = this.template;
        }
        
        if (this.parent) {
            $(this.parent).append(rendered);
        } else {
            this.$el.html(rendered);
        }

        return this;
    }
});


var HeaderView = BaseView.extend({
    el: '#header',
    template: $("#header_templ").html()
});


var MainView = BaseView.extend({
    el: '#main'
});