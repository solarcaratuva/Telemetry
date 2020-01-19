var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on( 'connect', function() {
  socket.emit( 'my event', {
    data: 'User Connected'
  } )
} )
socket.on( 'my response', function( msg ) {
  console.log( msg )
  if( typeof msg.mph !== 'undefined' ) {
    $('#mph').text(msg.mph)
    
  }
  if( typeof msg.rpm !== 'undefined' ) {
    $( '#rpm' ).text(msg.rpm)
  }
  if( typeof msg.miles !== 'undefined' ) {
    $( '#miles' ).text(msg.miles)
  }
  

  socket.emit( 'my event', {'rpm': msg.rpm})

})