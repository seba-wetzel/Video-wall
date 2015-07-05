/* Basicamente este es un programa Arduino que se ejecuta cuando recibe por el puerto serie //
// la letra p (de prendido quizas?), se fija si hay un objeto en la distacina especificada  //
// y si esta espera a que alguien lo saque, para mandar la señal R (de reproducir?) por el  //
// puerto serie. Si no hay nada adelante, espera a que lo halla, y despues esperar a que lo //
// saquen para manda la señal. Una vez hecho esto se queda a la espera de la señal p.       */

boolean estado = false;
boolean iniciar = true;
bool mandarR = true;
int entrada;
int contador = 0;
int sonar;

void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  pinMode(4,INPUT);
  digitalWrite(4,HIGH);
  digitalWrite(13, HIGH);
  pinMode(9, OUTPUT); /*activación del pin 9 como salida: para el pulso ultrasónico*/
  pinMode(8, INPUT); /*activación del pin 8 como entrada: tiempo del rebote del ultrasonido*/
}

void loop() {
  if (Serial.available() > 0) {
    entrada = Serial.read();     //leemos la opcion enviada
    if (entrada == 'p') {       //si la raspi manda la p de prendido, el sonar busca
      
      
      
      while(iniciar){
        sonar = ultrasonido();
        Serial.println(sonar);
        if (sonar<15){
          estado = true;  
          iniciar= false ;
          
        }
        else if (sonar>20){
          estado = false;
          iniciar= true;
          
        }
      }
    }

    while (estado) {
      sonar = ultrasonido();
      Serial.println(sonar);
      if (sonar > 16) {
        contador++;
        delay(100);
        //Serial.println(contador);
        if (contador>= 5) {
          estado = false;
          iniciar= true ;
          Serial.println('R');      // enviamos R de "reproducir" para que la raspi reprodusca el video
          Serial.flush();
        }
      }
      else {
        contador = 0;
      }
    }
  }
  if(mandarR){
  if (digitalRead(4) == LOW){
    Serial.print("R");
    mandarR= false;
  }
  }
}


int ultrasonido() {               // funcion que devuelve un entero correspondiente a la distancia
  int valor = 0;
  int calculo = 0;
  for(int i=0; i< 10; i++){  // Se usa un bucle para hacer la medicion varias veces y promediar
    digitalWrite(9, LOW); /* Por cuestión de estabilización del sensor*/
    delayMicroseconds(5);
    digitalWrite(9, HIGH); /* envío del pulso ultrasónico*/
    delayMicroseconds(10);
    int tiempo = pulseIn(8, HIGH);
    int distancia = int(0.017 * tiempo);
    calculo= calculo+ distancia;
  }
  valor= calculo/11;
  delay(1000);
  return valor;
}
