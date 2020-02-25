var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function() {
  socket.emit('dataEvent', "User Connected")
})

socket.on('dataEvent', function(data) {
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
  addData(myLineChart, data.t, data.bc);

  //Motor


  


  
  socket.emit('dataEvent', "Data Received")
})