from app import db,  runTracker
from .models import Base, BMS, KLS, Runs

#Store data in db
def storeData(data):
    BMS_data = BMS(current=data['b'][0],
                    voltage=data['b'][1],
                    soc=data['b'][2],
                    max_temperature=data['b'][3],
                    temperature=data['b'][4],
                    charge_limit=data['b'][5],
                    discharge_limit=data['b'][6],
                    current_limit=data['b'][7],
                    disch_bool=data['c'][0],
                    charge_bool=data['c'][1],
                    safety_bool=data['c'][2],
                    malfunction=data['c'][3],
                    multi_purpose_out=data['c'][4],
                    always_on_signal=data['c'][5],
                    ready_signal=data['c'][6],
                    charge_signal=data['c'][7],
                    P0A1F=data['f'][0],
                    P0A00=data['f'][1],
                    P0A80=data['f'][2],
                    P0AFA=data['f'][3],
                    U0100=data['f'][4],
                    P0A04=data['f'][5],
                    P0AC0=data['f'][6],
                    P0A01=data['f'][7],
                    P0A02=data['f'][8],
                    P0A03=data['f'][9],
                    P0A81=data['f'][10],
                    P0A9C=data['f'][11],
                    P0560=data['f'][12],
                    P0AA6=data['f'][13],
                    P0A05=data['f'][14],
                    P0A06=data['f'][15],
                    P0A07=data['f'][16],
                    P0A08=data['f'][17],
                    P0A09=data['f'][18],
                    P0A0A=data['f'][19],
                    P0A0B=data['f'][20],
                    run_id = runTracker.getID(),
                    json=data
                    )

    KLS_data = KLS(command_status=data['sa'][0],
                    feedback_status=data['sa'][0],
                    hall_a=data['sa'][0],
                    hall_b=data['sb'][0],
                    hall_c=data['sc'][0],
                    brake=data['sd'][0],
                    backward=data['se'][0],
                    forward=data['sf'][0],
                    foot=data['sg'][0],
                    boost=data['sh'][0],
                    rpm=data['k'][0],
                    current_limit_status=data['k'][1],
                    voltage=data['k'][2],
                    throttle=data['k'][3],
                    controller_temp=data['k'][4],
                    motor_temp=data['k'][5],
                    run_id = runTracker.getID()
                    )

    db.session.add(BMS_data)
    db.session.add(KLS_data)
    db.session.commit()