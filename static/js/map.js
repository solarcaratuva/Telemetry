mapboxgl.accessToken = 'pk.eyJ1IjoianRraW0iLCJhIjoiY2tkdHQ2aWs0MDViMzJ3bm9rczFzN2lsMyJ9.XiSAK1bC23g7vzeeQfvKmA';
var map = new mapboxgl.Map({
container: 'map',
style: 'mapbox://styles/mapbox/streets-v11', // stylesheet location
center: [-78.5080, 38.0336], // starting position [lng, lat]
zoom: 11 // starting zoom
});
/*
map.on('load', function () {
        coordinates = [-78.5080, 38.0336]
        

            // start by showing just the first coordinate
            //data.features[0].geometry.coordinates = [coordinates[0]];

            // add it to the map
            map.addSource('trace', { type: 'geojson', data: data });
            map.addLayer({
                'id': 'trace',
                'type': 'line',
                'source': 'trace',
                'paint': {
                    'line-color': 'yellow',
                    'line-opacity': 0.75,
                    'line-width': 5
                }
            });

            // setup the viewport
});
*/
var coordinates = [[-78.5080, 38.0336]]

map.on('load',function() {
map.jumpTo({ 'center': coordinates[0], 'zoom': 14 });
map.setPitch(30);
/*
map.addLayer({
    'id': 'drone',
    'type': 'symbol',
    'source': 'drone',
    'layout': {
    'icon-image': 'rocket-15'
        }
    });
*/
});

var markers = []

function updateCoord(map) {
    coordinates[0][0] += .0001
    coordinates[0][1] += .0001
    removeMarker();
    var marker = new mapboxgl.Marker()
    .setLngLat(coordinates[0])
    .addTo(map);
    markers.push(marker);
    map.panTo(coordinates[0]);
}

function removeMarker() {
    if (markers!==null) {
        for (var i = markers.length - 1; i >= 0; i--) {
          markers[i].remove();
            }
        }   
}