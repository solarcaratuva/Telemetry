function displayData(data){
    //Main Dashboard
    $('#current').text(data.b[0])
    $('#voltage').text(data.b[1])
    $('#soc').text(data.b[2])
    $('#max_temperature').text(data.b[3])
    $('#temperature').text(data.b[4])
    $('#charge_limit').text(data.b[5])
    $('#discharge_limit').text(data.b[6])
    $('#current_limit').text(data.b[7])
  
    $('#disch_bool').text(data.c[0])
    $('#charge_bool').text(data.c[1])
    $('#safety_bool').text(data.c[2])
    $('#malfunction').text(data.c[3])
    $('#multi-purpose_out').text(data.c[4])
    $('#always_on_signal').text(data.c[5])
    $('#ready_signal').text(data.c[6])
    $('#charge_signal').text(data.c[7])
  
    $('#P0A1F').text(data.f[0])
    $('#P0A00').text(data.f[1])
    $('#P0A80').text(data.f[2])
    $('#P0AFA').text(data.f[3])
    $('#U0100').text(data.f[4])
    $('#P0A04').text(data.f[5])
    $('#P0AC0').text(data.f[6])
    $('#P0A01').text(data.f[7])
    $('#P0A02').text(data.f[8])
    $('#P0A03').text(data.f[9])
    $('#P0A81').text(data.f[10])
    $('#P0A9C').text(data.f[11])
    $('#P0560').text(data.f[12])
    $('#P0AA6').text(data.f[13])
    $('#P0A05').text(data.f[14])
    $('#P0A06').text(data.f[15])
    $('#P0A07').text(data.f[16])
    $('#P0A08').text(data.f[17])
    $('#P0A09').text(data.f[18])
    $('#P0A0A').text(data.f[19])
    $('#P0A0B').text(data.f[20])
  
    $('#command_status').text(data.k[6])
    $('#feedback_status').text(data.k[7])
  
    $('#hall_a').text(data.sa)
    $('#hall_b').text(data.sb)
    $('#hall_c').text(data.sc)
    $('#brake').text(data.sd)
    $('#backward').text(data.se)
    $('#forward').text(data.sf)
    $('#foot').text(data.sg)
    $('#boost').text(data.sh)
    $('#rpm').text(data.k[0])
    $('#mph').text((data.k[0] * 7 * 60 / 5280).toFixed(2))
  
    checkData(data.k[0],12,"Warning: RPM is less than 12","RPM warning resolved","rpmWarn")
  
    $('#current_limit_status').text(data.k[1])
    $('#voltage').text(data.k[2])
    $('#throttle').text(data.k[3])
    $('#controller_temp').text(data.k[4])
    $('#motor_temp').text(data.k[5])
  
    $('#solarCell').text(data.k[5])
    $('#module').text(data.k[5])
    //$('#').text(data.t)
  
    //state of charge chart
    addData(chart, data.b[2]);
  
  }
  