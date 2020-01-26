#include <Wire.h>
#include <avr/sleep.h>
#include <avr/power.h>

int humidityValue;
int brightnessValue;
byte lock_read;
byte cmd;

void setup()
{
  Wire.begin(0x04);                // join i2c bus with address #4
  digitalWrite(A4, LOW);
  digitalWrite(A5, LOW);

  Wire.onRequest(requestEvent);
  Wire.onReceive(receiveEvent);
  //Serial.begin(9600);           // start serial for output
  humidityValue = analogRead(A0);
  brightnessValue = analogRead(A1);
  lock_read = 0;
}

void loop()
{
  if ((lock_read & 1) != 1)
  {
      humidityValue = analogRead(A0);
  }
  if ((lock_read & 2) != 2)
  {
    brightnessValue = analogRead(A1);
  }

}

void requestEvent()
{
  if (cmd == 0)
  {
    if ((lock_read & 1) == 0)
    {
      lock_read = lock_read | 1;
      byte h_high = humidityValue >> 8;
      Wire.write(h_high);
    }
    else
    {
      byte h_low = humidityValue;
      Wire.write(h_low);
      lock_read = lock_read & B11111110;
    }
  }
  else if (cmd == 1)
  {
    if ((lock_read & 2) == 0)
    {
      lock_read = lock_read |  2;
      byte h_high = brightnessValue >> 8;
      Wire.write(h_high);
    }
    else
    {
      byte h_low = brightnessValue;
      Wire.write(h_low);
      lock_read = lock_read & B11111101;
    } 
  }
}

void receiveEvent(int buffer)
{
  while (Wire.available())
  {
    cmd = Wire.read();
  }
  if (cmd == 0)
  {
     lock_read = 0;
  }
}


