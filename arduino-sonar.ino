boolean estado = true;
int entrada;
int contador = 0;
void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);
  pinMode(9, OUTPUT); /*activación del pin 9 como salida: para el pulso ultrasónico*/
  pinMode(8, INPUT); /*activación del pin 8 como entrada: tiempo del rebote del ultrasonido*/
}

void loop() {
  if (Serial.available() > 0) {
    //leemos la opcion enviada
    entrada = Serial.read();
    if (entrada == 'p') {               //si la raspi manda la p de prendido, el sonar busca
      Serial.flush();
      estado = true;
      while (estado) {

        if (sonar() > 15) {
          contador++;
          delay(100);
          //Serial.println(contador);
          if (contador>= 5) {
            estado = false;
            contador = 0;
            Serial.println('R');
          }
        }
        else {
          contador = 0;
        }
        if (Serial.available() > 0) {
          entrada = Serial.read();
          if (entrada == 'a') {        // si la raspi manda la a de apagado, el sonar se apaga
            estado = false;
          }
        }
      }
    }
  }
}



int sonar() {
  digitalWrite(9, LOW); /* Por cuestión de estabilización del sensor*/
  delayMicroseconds(5);
  digitalWrite(9, HIGH); /* envío del pulso ultrasónico*/
  delayMicroseconds(10);
  int tiempo = pulseIn(8, HIGH);
  int distancia = int(0.017 * tiempo);
  return distancia;
}

