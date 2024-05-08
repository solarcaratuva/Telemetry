#include <FlexCAN.h>
#include <cstdint>

// Define CAN0 pins
#define CAN_TX_PIN 3
#define CAN_RX_PIN 4

// Create a CAN object
FlexCAN CANbus;
int motor_commands_rate_divisor = 30;
int curr_motor_commands_ct = 0;

static inline uint16_t unpack_right_shift_u16(
    uint8_t value,
    uint8_t shift,
    uint8_t mask)
{
    return (uint16_t)((uint16_t)(value & mask) >> shift);
}

static inline uint16_t unpack_left_shift_u16(
    uint8_t value,
    uint8_t shift,
    uint8_t mask)
{
    return (uint16_t)((uint16_t)(value & mask) << shift);
}

static inline uint8_t unpack_right_shift_u8(
    uint8_t value,
    uint8_t shift,
    uint8_t mask)
{
    return (uint8_t)((uint8_t)(value & mask) >> shift);
}

static inline uint8_t unpack_left_shift_u8(
    uint8_t value,
    uint8_t shift,
    uint8_t mask)
{
    return (uint8_t)((uint8_t)(value & mask) << shift);
}

void setup() {
  Serial.begin(9600);
  while (!Serial); // Wait for Serial Monitor to open
  Serial.print("starting\n");
  // Initialize CAN bus
  Can0.begin(250000); // Set baud rate to 250 kbps
}

void loop() {
  CAN_message_t msg;

  // Check if a CAN message is available
  while (Can0.available()) {
    // Read the CAN message
    Can0.read(msg);

    // Print message ID and data
    // Serial.print("ID: ");
    // Serial.print(msg.id, DEC);
    // Serial.print("  Data: ");
    // for (int i = 0; i < msg.len; i++) {
    //   Serial.print(msg.buf[i], DEC);
    //   Serial.print(" ");
    // }
    // Serial.println();
    switch(msg.id) {
    case (1030): {
      int pack_voltage = ((msg.buf[1]<<8) | msg.buf[0]);
      Serial.printf("pack_voltage %d\n", pack_voltage);
      int pack_current = ((msg.buf[3]<<8) | msg.buf[2]);
      Serial.printf("pack_current %d\n", pack_current);
      break;
    }
    case (805): {
      int motor_rpm = unpack_right_shift_u16(msg.buf[4], 3u, 0xf8u);
      motor_rpm |= unpack_left_shift_u16(msg.buf[5], 5u, 0x7fu);
      Serial.printf("motor_rpm %d\n", motor_rpm);
      break;
    }
    case (1062): {
      int high_cell_tmp = msg.buf[2];
      Serial.printf("tmp %d\n", high_cell_tmp);
      break;
    }
    case(513): {
      ++curr_motor_commands_ct;
      if(curr_motor_commands_ct < motor_commands_rate_divisor) {
        break;
      }
      curr_motor_commands_ct = 0;
      // int throttle = unpack_right_shift_u16(msg.buf[0], 0u, 0xffu);
      // throttle |= unpack_left_shift_u16(msg.buf[1], 8u, 0x01u);
      // Serial.printf("throttle %d\n", throttle);
      int regen = unpack_right_shift_u16(msg.buf[1], 1u, 0xfeu);
      regen |= unpack_left_shift_u16(msg.buf[2], 7u, 0x03u);
      Serial.printf("regen %d\n", regen);
      int cruise_control_speed = unpack_right_shift_u8(msg.buf[2], 2u, 0xfcu);
      cruise_control_speed |= unpack_left_shift_u8(msg.buf[3], 6u, 0x03u);
      Serial.printf("cc_speed %d\n-", cruise_control_speed);
      int cruise_control_en = unpack_right_shift_u8(msg.buf[3], 2u, 0x04u);
      Serial.printf("cc_en %d\n", cruise_control_en);
      break;
    }
    case(262): {
      uint32_t bms_out = msg.buf[2];
      bms_out = (bms_out<<8) | msg.buf[1];
      bms_out = (bms_out<<8) | msg.buf[0];
      Serial.printf("bms_fault %d\n", bms_out);
      break;
    }
    case(769): {
      uint8_t left_turn = (msg.buf[0]>>3)&1;
      Serial.printf("left_turn %d\n", left_turn);
      uint8_t right_turn = (msg.buf[0]>>4)&1;
      Serial.printf("right_turn %d\n", right_turn);
      break;
    }
    }
  }
}