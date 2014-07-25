#include <WiFi.h>
#include <avr/io.h>
#include <avr/interrupt.h>

boolean trigger;

char ssid[] = "wicip";
char pass[] = "wicipwifi";

int del;
int status = WL_IDLE_STATUS;
int led = 13;
int csens_volt = A5;
int vsens2 = A3;
int vsens1 = A1;

uint8_t serverip[4] = {192,241,246,131};
uint8_t servport = 80;

WiFiClient client;

void setup(){
  Serial.begin(9600);
  pinMode(led, OUTPUT);
  pinMode(A3, INPUT);
  pinMode(A1, INPUT);
  pinMode(A5, INPUT);
  del = 0;
  trigger = true;
  cli();
  TCCR1A = 0; // set TCCR1A register to 00000000
  TCCR1B = 0; // set TCCR1B register to 00000000
  OCR1A = 15624; // set compare match register; should be 1 sec delay
  TCCR1B |= (1 << WGM12); // Set WGM12 bit to 1, turns on CTC mode:
  TCCR1B |= (1 << CS12)|(1 << CS10); // Set CS10 and CS12 bits to 1
  TIMSK1 |= (1 << OCIE1A); // enable timer compare interrupt:
  sei();
  
  status = WiFi.begin(ssid,pass);
  if (status != WL_CONNECTED) {
    Serial.println("Attempting to connect to wifi...");
    while(true);
  }
  
  else {
    Serial.print("Connected to wifi.");
  }
  
}

ISR (TIMER1_COMPA_vect){
  del = del + 1;
}

void loop(){
  int i;
  if (del >= 900) {
    digitalWrite(led, !digitalRead(led));
    delay(2);
    del = 0;
    Serial.println("Current:");
    
    double csv = analogRead(csens_volt)*5.0/1023.0;
    double vs1 = analogRead(vsens1)*11.0*5.0/1023.0;
    double vstot = analogRead(vsens2)*11.0*5.0/1023.0;
    double vs2 = vstot - vs1;

    double current = csv*89.40/3.30;
    
    Serial.print("VS1: ");
    Serial.println(vs1);
    Serial.print("VS2: ");
    Serial.println(vs2);
    Serial.print("VSTotal: ");
    Serial.println(vstot);
    Serial.print("CS: ");
    Serial.println(current);
    
    for (i=0;i<10;i++) {
     if (sendData(vs1, vs2, vstot, current)) {
      break;
     }
    } 
  }
  
  
}

boolean sendData(double v1, double v2, double v3, double c){
  boolean con = false;
  int i = 0;

  client.connect(serverip, servport);

  
  if (!client.connected()) {
    Serial.println("Failed to connect to server");
    return false;
  }
  
//  if (!client.available()){
//    Serial.println("Server not available");
//    return false;
//  }
  Serial.println("Sending http req");
  client.print("GET /pull.php?");

  client.print("v1=");
  client.print(v1);
  client.print("&&v2=");
  client.print(v2);
  client.print("&&v3=");
  client.print(v3);
  client.print("&&c1=");
  client.print(c);
  client.println(" HTTP/1.0\r\n");
  client.println("Host:192.241.246.131\r\n");
  client.println("User-Agent: Arduino\r\n");
  client.println("Accept: text/html\r\n");
  client.println("Connection: close\r\n");
  client.println();

  Serial.println("Data pushed!");
  
  while (client.connected() && client.available()) {
    char c = client.read();
    Serial.print(c);
  }
  
  client.flush();
  client.stop();
  return true;
  
}


  
