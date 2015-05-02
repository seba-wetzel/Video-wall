/* Basicamente este es un programa Arduino que se ejecuta cuando recibe por el puerto serie //
// la letra p (de prendido quizas?), se fija si hay un objeto en la distacina especificada  //
// y si esta espera a que alguien lo saque, para mandar la señal R (de reproducir?) por el  //
// puerto serie. Si no hay nada adelante, espera a que lo halla, y despues esperar a que lo //
// saquen para manda la señal. Una vez hecho esto se queda a la espera de la señal p.       */

boolean estado = false;
boolean iniciar = true;
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
    entrada = Serial.read();     //leemos la opcion enviada
    if (entrada == 'p') {       //si la raspi manda la p de prendido, el sonar busca
      Serial.flush();
      while(iniciar){
        if (sonar()<15){
          estado = true;  
          iniciar= false ;
          Serial.flush();
        }
        else if (sonar()>20){
          estado = false;
          iniciar= true;
          Serial.flush();
        }
      }
    }

    while (estado) {
      if (sonar() > 15) {
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
}


int sonar() {               // funcion que devuelve un entero correspondiente a la distancia
  int valor;
  int calculo;
  for(int i=0; i< 3; i++){  // Se usa un bucle para hacer la medicion varias veces y promediar
    digitalWrite(9, LOW); /* Por cuestión de estabilización del sensor*/
    delayMicroseconds(5);
    digitalWrite(9, HIGH); /* envío del pulso ultrasónico*/
    delayMicroseconds(10);
    int tiempo = pulseIn(8, HIGH);
    int distancia = int(0.017 * tiempo);
    calculo= calculo+ distancia;
  }
  valor= calculo/4;
  return valor;
}
