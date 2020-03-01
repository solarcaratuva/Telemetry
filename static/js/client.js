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
  $('#').text(data.bc)
  $('#maxTemperature').text(data.bd)
  $('#temperature').text(data.be)
  $('#').text(data.bf)  //charge_limit
  $('#').text(data.bg)  //discharge_limit
  $('#').text(data.bh)

  $('#').text(data.ca)
  $('#').text(data.cb)
  $('#').text(data.cc)
  $('#').text(data.cd)
  $('#').text(data.ce)
  $('#').text(data.cf)
  $('#').text(data.cg)
  $('#').text(data.ch)
  
  $('#').text(data.fa)
  $('#').text(data.fb)
  $('#').text(data.fc)
  $('#').text(data.fd)
  $('#').text(data.fe)
  $('#').text(data.ff)
  $('#').text(data.fg)
  $('#').text(data.fh)
  $('#').text(data.fi)
  $('#').text(data.fj)
  $('#').text(data.fk)
  $('#').text(data.fl)
  $('#').text(data.fm)
  $('#').text(data.fn)
  $('#').text(data.fo)
  $('#').text(data.fp)
  $('#').text(data.fq)
  $('#').text(data.fr)
  $('#').text(data.fs)
  $('#').text(data.ft)
  $('#').text(data.fu)

  $('#').text(data.kg)
  $('#').text(data.kh)

  $('#').text(data.sa)
  $('#').text(data.sb)
  $('#').text(data.sc)
  $('#').text(data.sd)
  $('#').text(data.se)
  $('#').text(data.sf)
  $('#').text(data.sg)
  $('#').text(data.sh)


  $('#rpm').text(data.ka)
  $('#mph').text(data.ka * 7 * 60 / 5280)
  $('#').text(data.kb)
  $('#').text(data.kc)
  $('#').text(data.kd)
  $('#').text(data.ke)
  $('#').text(data.kf)

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