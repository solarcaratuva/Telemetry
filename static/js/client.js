var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function() {
  socket.emit('dataEvent', "User Connected")
})

socket.on('dataEvent', function(data) {
  $('#mph').text(data.mph)
  $('#rpm').text(data.rpm)
  $('#miles').text(data.miles)
  console.log(data.socTime);
  addData(myLineChart, data.socTime, data.socVal);
  
  socket.emit('dataEvent', "Data Received")
})