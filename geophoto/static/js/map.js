
var MapState = Backbone.Model.extend({
    defaults: {
        mapCenter: [33, -112],
        mapZoom: 4
    }
});


var MapState = new MapState();
var MapView = BaseView.extend({
    el: '#main',
    template: $("#mapview_templ").html(),
    set_state: function (e) {
        MapState.set('mapCenter', this.map.getCenter());
        MapState.set('mapZoom', this.map.getZoom());
    },
    initialize: function (params) {
        this.url = params.url;
        this.photo = params.photo;
        BaseView.prototype.initialize.call(this);
    },
    render: function(){
        BaseView.prototype.render.call(this);
        var mapCenter = MapState.get('mapCenter');
        var mapZoom = MapState.get('mapZoom');
        this.map = L.map(
            'map', this.settings
        ).setView(mapCenter, mapZoom);
        
        underlay = L.tileLayer(
            'https://otile1-s.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.png'
        ).addTo(this.map);
        
        var self = this;
        this.map.on('dragend', function (e) {
            self.set_state(e);
        });

        d3.json(this.url, function(d){
            self.load_layer(d);
            if (self.photo) {
                self.photo_selected(self.photo);
            } else {
                self.photo_selected(d.results[0])
            }
        });
        return this;
    },
    display_layer: false,
    source_layer: false,
    photo_selected: function(d) {
        if (d.src) {
            $('#gallery-photo').attr('src',d.src);
        } else {
            $('#gallery-photo').attr('src',this.photos[d].src);
        }
    },
    load_layer: function(d) {
        var map = this.map;
        var photos = this.photos = {};
    	var display_layer = this.display_layer;
    	try {
            map.removeLayer(display_layer);
        } catch (e) {  }
		display_layer = L.markerClusterGroup();

		d["results"].forEach(function(dd) {
            photos[dd.id] = dd;
			var mk = L.circleMarker([dd.lat, dd.lng], {
				color: 'red',
				fillColor: 'blue',
				radius: 5,
				weight: 2,
				fillOpacity: 0.5
			}).addTo(display_layer);
			
            var self = this;
            mk.bindPopup(dd.id, {offset: L.point(0,-10)})
				.on('mouseover', function show_tooltip () { this.openPopup(); })
				.on('mouseout', function hide_tooltip () { this.closePopup(); })
				.on('click', function map_click () {
					router.navigate('photo/' + dd.id, true)
				})
		})

		display_layer.addTo(map);
        this.display_layer = display_layer;
    }
});
