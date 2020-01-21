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
  init_timer_1();
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
  power_adc_disable();
  power_spi_disable();
  power_timer0_disable();
  power_timer2_disable();
  sleep_cpu();

  sleep_disable();
  power_all_enable(); 
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
      byte h_high = humidityValue >> 8;
      Wire.write(h_high);
    }
    else
    {
      byte h_low = humidityValue;
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

//Timer_1 initialisieren
void init_timer_1 ()
{
  cli();        // Interrupts ausschalten
  TCCR1A = 0;   // Register Reset
  TCCR1B = 0;
  TIMSK1 = 0;
  TIMSK1 |= (1 << TOIE1); // Overflow Interrupt enable
  //Timer-Counter-Startwert eine Vorladung zuweisen, damit dieser ca. 4 Sekunden hochzaehlt
  //kein Wert zugewiesen heisst,dass es bis zum Overflow ca. 4,19s dauert ( bei 16 MHz und Prescaler 1024 (Overflow bei 65536))
  TCNT1 = 0;
  TCCR1B |= (1 << CS12) | (1 << CS10);  // Prescaler 1024
  sei();        // Interrupts einschalten
}

