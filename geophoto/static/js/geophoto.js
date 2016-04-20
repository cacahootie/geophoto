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
        "photo/:id":"photo"
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
        this.loadView(HomeView,{
            url:'/photos/'
        });
    },
    photo: function (d) {
        this.loadView(PhotoView, d);
    }
});

var base = new AppView(),
    router = new AppRouter(),
    photo_order = [],
    photos = {};

router.view = base;

$.getJSON('/photos/', function (d) {
    _.each(d.results, function(dd) {
        photo_order.push(dd.id);
        photos[dd.id] = dd;
    });
    $(window).on("hashchange", router.hashChange);
    Backbone.history.start();
});
