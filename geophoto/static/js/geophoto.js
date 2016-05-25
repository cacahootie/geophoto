var attrtext = '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors | <a href="http://openflights.org">OpenFlights</a>';

var AppView = BaseView.extend({
    el: '#container',
    template: $("#layout").html(),
    initialize: function() {
    	BaseView.prototype.initialize.call(this);
        this.header = new HeaderView();
    }
});

var AppRouter = Backbone.Router.extend({
    routes: {
        "":"home",
        "map":"map",
        "map/:type/:id":"mapitem",
        "photos/:id":"photo",
        "photos":"photos",
        "articles/:key":"article",
        "articles":"articles"
    },
    loadView: function(view,params,coll) {
        $('#main').empty()
        this.view = new view(params);
    },
    hashChange : function(evt) {
        if(this.cancelNavigate) { // cancel out if just reverting the URL
            evt.stopImmediatePropagation();
            this.cancelNavigate = false;
            return;
        }
        if(this.view && this.view.dirty) {
            var dialog = confirm("You have unsaved changes. To stay on the page, press cancel. To discard changes and leave the page, press OK");
            if(dialog == true)
                return;
            else {
                evt.stopImmediatePropagation();
                this.cancelNavigate = true;
                window.location.href = evt.originalEvent.oldURL;
            }
        }
    },
    home: function () {
        this.loadView(HomeView);
    },
    article: function (key) {
        this.loadView(ArticleView,key);
    },
    articles: function () {
        this.loadView(HomeView);
    },
    map: function () {
        this.loadView(PhotoMapView,{
            url:'/photos/'
        });
    },
    mapitem: function (type, id) {
        this.loadView(PhotoMapView,{
            url:'/photos/',
            type: type,
            id: id
        });
    },
    photo: function (key) {
        this.loadView(PhotoView, key);
    },
    photos: function () {
        this.loadView(HomeView);
    }

});

var base = new AppView(),
    router = new AppRouter(),
    photo_order = [],
    photos = {};

router.view = base;

$.getJSON('/photos/?format=json', function (d) {
    _.each(d.results, function(dd) {
        photo_order.push(dd.id);
        photos[dd.id] = dd;
    });
    $(window).on("hashchange", router.hashChange);
    Backbone.history.start({pushState:true, root: '/'});

    $(document).on("click", "a[href]:not([data-bypass])", function(evt) {
      // Get the absolute anchor href.
      var href = { prop: $(this).prop("href"), attr: $(this).attr("href") };
      // Get the absolute root.
      var root = location.protocol + "//" + location.host + '/';

      // Ensure the root is part of the anchor href, meaning it's relative.
      if (href.prop.slice(0, root.length) === root) {
        // Stop the default event to ensure the link will not cause a page
        // refresh.
        evt.preventDefault();

        // `Backbone.history.navigate` is sufficient for all Routers and will
        // trigger the correct events. The Router's internal `navigate` method
        // calls this anyways.  The fragment is sliced from the root.
        Backbone.history.navigate(href.attr, true);
      }
    });
});
