char original_messg;
char final_messg; 
const int len = 15;
const String utf_messg[len] = {"x58","x59","x78","x79","x30","x31","x32","x33","x34","x35","x36","x37","x38","x39","x2D"};
const char converted_messg[len] = {'X','Y','x','y','0','1','2','3','4','5','6','7','8','9','-'};
void setup() {
  //set baud rate
  Serial.begin(9600); 
  //set pins rx and tx for serial communication
  pinMode(0, INPUT);
  pinMode(1, OUTPUT);
}

void loop() {
  while (Serial.available()>0)
  { 
    original_messg = Serial.read();
    for (int i = 0; i < len; i++) {
      if(utf_messg[i] == original_messg)
        final_messg = converted_messg[i];  
    }
  }
  //grbl(final_mssg);

}
