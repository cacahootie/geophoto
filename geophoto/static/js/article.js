
var ArticleView = BaseView.extend({
    el: '#main',
    template: $("#article_templ").html(),
    initialize: function (key) {
        $.getJSON('/articles/' + key + "/?format=json", _.bind(
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

                $(this.el).find('div.imgix-fluid').on('click', function (d) {
                    window.location = $(this).data('src');
                });
                
	        }, this)
        );
    }
});
