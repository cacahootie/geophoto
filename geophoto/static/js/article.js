
var ArticleView = BaseView.extend({
    el: '#main',
    template: $("#article_templ").html(),
    initialize: function (key) {
        $.getJSON('/articles/' + key, _.bind(
        	function (d) {
	        	this.data = d;
	        	BaseView.prototype.initialize.call(this);

                imgix.onready(function() {
                    imgix.fluid({
                        updateOnResizeDown: true,
                        pixelStep: 5,
                        autoInsertCSSBestPractices: true
                    });
                });
                
	        }, this)
        );
    }
});
