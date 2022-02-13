var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function() {
  console.log('Connected');
});
socket.on('dataEvent', function(data) {
  console.log(data);
  displayData(data);
});

var rpmWarn = false;
//For numerical values
function checkData(current,ideal,warnText,resolutionText,error) {
  var today = new Date();
  var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
  var br = document.createElement("br");
  var warning = document.createElement("warn")
  warning.style.color = "red";
  warning.textContent = warnText + "\n"
  var resolved = document.createElement("res")
  resolved.style.color = "green";
  resolved.textContent = resolutionText + "\n"
  var warnBox = document.getElementById("warning")
  console.log(warnBox)
  if(warnBox == null){
    return;
  }
  if (current < ideal && window[error] == false) {
    warnBox.appendChild(warning);
    warnBox.appendChild(br);
    window[error] = true
  }
  else if (current > ideal && window[error] == true) {
    warnBox.appendChild(resolved)
    warnBox.appendChild(br);
    window[error] = false
  }
}

//For booleans 
function checkFault(current,ideal,warnText,resolutionText,error) {
  var today = new Date();
  var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
  var br = document.createElement("br");
  var warning = document.createElement("warn")
  warning.style.color = "red";
  warning.textContent = warnText + "\n"
  var resolved = document.createElement("res")
  resolved.style.color = "green";
  resolved.textContent = resolutionText + "\n"
  var warnBox = document.getElementById("warning")
  console.log(warnBox)
  if (current != ideal && window[error] == false) {
    warnBox.appendChild(warning);
    warnBox.appendChild(br);
    window[error] = true
  }
  else if (current == ideal && window[error] == true) {
    warnBox.appendChild(resolved)
    warnBox.appendChild(br);
    window[error] = false
  }
}
socket.on('restoreData', function(data){
  console.log('RESTORING DATA', data);
  clearGraph(chart);

  for (var i = 0; i < data.length; i++){
    displayData(data[i][0])
  }

});

socket.on('toggleRecording', function(){
  console.log('ccccc');
  $("#startBtn, #stopBtn, #recording, #startRecordingBtn, #stopRecordingBtn").toggleClass("d-none")
});

$('form').submit(function(event){
  event.preventDefault();
  console.log("FORM SUBMITTED");

  if($('#stopBtn').hasClass('d-none')){
    socket.emit('new_run', { 
                             title: $('#name').val(),
                             driver: $('#driver').val(),
                             location: $('#location').val(),
                             description: $('#description').val(),
                            });
  }

  else{
    socket.emit('stop_run')
  }
});

var c = 100;

// TODO: This should be constantly called somehow by the frontend (either somehow check if there's an update, or use an interval to constantly update data)
function get_api_data() {
  $.getJSON('http://' + document.domain + ':' + location.port + '/data',
    function(data){
      console.log(data);
      displayData(data);
    })
}

// NOTE: This method shouldn't be used in the final version. It just creates random data
function update_api_data() {
  $.ajax({
    type: "POST",
    url: 'http://' + document.domain + ':' + location.port + '/update',
    data: JSON.stringify({}),
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: function(data){alert(data);},
    error: function(errMsg) {
        alert(errMsg);
    }
  });
}

function read_from_run(run_id){
  socket.emit('connect_run', {
    run_id: run_id,
   });

}