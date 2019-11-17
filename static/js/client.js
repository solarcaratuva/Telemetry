var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on( 'connect', function() {
  socket.emit( 'my event', {
    data: 'User Connected'
  } )
  
} )
socket.on( 'my response', function( msg ) {
  console.log( msg )
  if( typeof msg.speed !== 'undefined' ) {
    $('#mph').text(msg.speed)
    
  }
  if( typeof msg.rpm !== 'undefined' ) {
    $( '#rpm' ).text(msg.rpm)
    socket.emit( 'my event', {'rpm': msg.rpm})
  }
})

