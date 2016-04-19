
var PhotoMapView = BaseView.extend({
    el: '#main',
    template: $("#mapview_templ").html(),
    initialize: function (params) {
        this.url = params.url;
        this.photo = params.photo;
        BaseView.prototype.initialize.call(this);
    },
    render: function(){
        BaseView.prototype.render.call(this);
        
        this.map = L.map(
            'map', this.settings
        ).setView([36, 139],4);
        
        L.tileLayer(
            'https://otile1-s.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.png'
        ).addTo(this.map);
        
        d3.json(this.url, this.load_layer.bind(this));
    },
    add_point: function(item, display_layer) {
        var default_style = {
                color: 'red',
                fillColor: 'blue',
                radius: 10,
                weight: 2,
                fillOpacity: 0.5,
            },
            label = '<img src="' + item.src + '" class="map_thumb"></img>',
            mk = L.circleMarker([item.lat, item.lng], default_style)
                .addTo(display_layer);
        
        mk.bindPopup(
            label, {
                offset: L.point(0,-10),
                className: 'custom-popup'
            }
        )
            .on('mouseover', function show_tooltip () { this.openPopup(); })
            .on('mouseout', function hide_tooltip () { this.closePopup(); })
            .on('click', function map_click (e) {
                try {
                    self.last_marker.setStyle(default_style)
                } catch (e) {}
                e.target.setStyle({
                    color: 'orange',
                    fillColor: 'green',
                    radius: 15,
                    weight: 2,
                    fillOpacity: 0.5
                });
                self.last_marker = e.target;
                router.navigate('photo/' + item.id, true);
            });

        return mk;
    },
    load_layer: function(d) {
        var map = this.map,
    	    display_layer = this.display_layer,
            add_point = this.add_point;

    	try {
            map.removeLayer(display_layer);
        } catch (e) {  }
		display_layer = L.markerClusterGroup();

		photo_order.forEach(function(id) {
            add_point(photos[id], display_layer);
		});

		display_layer.addTo(map);
    }
});
