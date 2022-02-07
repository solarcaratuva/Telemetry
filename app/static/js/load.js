var socket = io.connect('http://' + document.domain + ':' + location.port);

$(".run_btn").click(function(){
    console.log($(this).attr('id'));
    socket.emit('loadData', $(this).attr('id'));
});

socket.on('loadData', function(data){
  console.log('SOCKETIO LOADGRAPH RECEIVED')
  console.log(data);
  clearGraph(chart);
  for (var i = 0; i < data.length; i++){
    console.log(data[i][0])
    displayData(data[i][0])
    
  }
});

