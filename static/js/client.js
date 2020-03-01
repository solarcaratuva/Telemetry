var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function() {
  socket.emit('dataEvent', "User Connected")
  getStoredData();
});

socket.on('dataEvent', function(data) {
  console.log(data);
  displayData(data);

  //local storage 
  localStorage.setItem("data", JSON.stringify(data));

  


  if(localStorage.getItem("graphData") != undefined) {
    var gd = JSON.parse(localStorage.getItem("graphData"));
    var val1 = data.socVal;
    gd.push(val1);
    localStorage.setItem("graphData", JSON.stringify(gd));
  }
  else{
    var graphData = [];
    var val1 = data.socVal;
    graphData.push(val1);
    localStorage.setItem("graphData", JSON.stringify(graphData));
  }

  if(localStorage.getItem("time") != undefined) {
    var time = JSON.parse(localStorage.getItem("time"));
    var val1 = data.socTime;
    time.push(val1);
    localStorage.setItem("time", JSON.stringify(time));
  }
  else{
    var time = [];
    var val1 = data.socTime;
    time.push(val1);
    localStorage.setItem("time", JSON.stringify(time));
  }

  
  socket.emit('dataEvent', "Data Received")
})

function displayData(data){
  //Main Dashboard
  $('#current').text(data.ba)
  $('#voltage').text(data.bb)
  $('#soc').text(data.bc)
  $('#max_temperature').text(data.bd)
  $('#temperature').text(data.be)
  $('#charge_limit').text(data.bf)  //charge_limit
  $('#discharge_limit').text(data.bg)  //discharge_limit
  $('#current_limit').text(data.bh)

  $('#disch_bool').text(data.ca)
  $('#charge_bool').text(data.cb)
  $('#safety_bool').text(data.cc)
  $('#malfunction').text(data.cd)
  $('#multi-purpose_out').text(data.ce)
  $('#always_on_signal').text(data.cf)
  $('#ready_signal').text(data.cg)
  $('#charge_signal').text(data.ch)
  
  $('#P0A1F').text(data.fa)
  $('#P0A00').text(data.fb)
  $('#P0A80').text(data.fc)
  $('#P0AFA').text(data.fd)
  $('#U0100').text(data.fe)
  $('#P0A04').text(data.ff)
  $('#P0AC0').text(data.fg)
  $('#P0A01').text(data.fh)
  $('#P0A02').text(data.fi)
  $('#P0A03').text(data.fj)
  $('#P0A81').text(data.fk)
  $('#P0A9C').text(data.fl)
  $('#P0560').text(data.fm)
  $('#P0AA6').text(data.fn)
  $('#P0A05').text(data.fo)
  $('#P0A06').text(data.fp)
  $('#P0A07').text(data.fq)
  $('#P0A08').text(data.fr)
  $('#P0A09').text(data.fs)
  $('#P0A0A').text(data.ft)
  $('#P0A0B').text(data.fu)

  $('#command_status').text(data.kg)
  $('#feedback_status').text(data.kh)

  $('#hall_a').text(data.sa)
  $('#hall_b').text(data.sb)
  $('#hall_c').text(data.sc)
  $('#brake').text(data.sd)
  $('#backward').text(data.se)
  $('#forward').text(data.sf)
  $('#foot').text(data.sg)
  $('#boost').text(data.sh)


  $('#rpm').text(data.ka)
  $('#mph').text(data.ka * 7 * 60 / 5280)
  $('#current_limit_status').text(data.kb)
  $('#voltage').text(data.kc)
  $('#throttle').text(data.kd)
  $('#controller_temp').text(data.ke)
  $('#motor_temp').text(data.kf)

  $('#').text(data.t)

    //state of charge chart
    //addData(myLineChart, data.t, data.bc);


  //old data
  $('#rpm').text(data.rpm);
  $('#mph').text(data.mph);
  addData(myLineChart,data.socTime, data.socVal);
}

function getStoredData(){
    data = JSON.parse(localStorage.getItem("data"));
    displayData(data);

    //update graph
    var soc = JSON.parse(localStorage.getItem("graphData"));
    var time = JSON.parse(localStorage.getItem("time"));
    
    for(var i = 0; i < soc.length; i++){
      addData(myLineChart, time[i], soc[i]);
    }
 
}