#include <Servo.h>

Servo m1;
Servo m2;
Servo m3;
Servo m4;

int ileri, geri, sag, sol, yukari, asagi, saatyonu, saatyonu_ters, kamera_yukari, kamera_asagi, isik, otonom_derinlik, gyro, otonom_gorev, goksen;
int veriler[15];// ileri / geri / sag / sol / yukari / asagi / saatyonu / saatyonu_ters / kamera_yukari / kamera_asagi / isik / otonom_derinlik / gyro / otonom_gorev / goksen
int m10, m20, m30, m40;
void hasanAli();

void setup() {

  Serial1.begin(9600);
  Serial.begin(9600);

  m1.attach(7);
  m1.write(0);
  delay(1000);
}

void loop() {
  hasanAli();
  
  m10 = -(sol*(ileri-180)*(sag-180)*(geri-180)) + (sol*ileri*(geri-180)*(sag-180)) - (ileri*(sol-180)*(sag-180)*(geri-180)) + (sag*ileri*(geri-180)*(sol-180)) + (sag*geri*(ileri-180)*(sol-180));
  m20 = -(sag*(ileri-180)*(sol-180)*(geri-180)) + (sol*ileri*(geri-180)*(sag-180)) - (ileri*(sol-180)*(sag-180)*(geri-180)) + (sag*ileri*(geri-180)*(sol-180)) + (sol*geri*(ileri-180)*(sag-180));
  m30 = -(sag*(ileri-180)*(sol-180)*(geri-180)) + (sol*ileri*(geri-180)*(sag-180)) - (geri*(sol-180)*(sag-180)*(geri-180)) + (sag*geri*(ileri-180)*(sol-180)) + (sol*geri*(ileri-180)*(sag-180));
  m40 = -(sag*(ileri-180)*(sol-180)*(geri-180)) + (sag*ileri*(geri-180)*(sol-180)) - (geri*(sol-180)*(sag-180)*(ileri-180)) + (sag*geri*(ileri-180)*(sol-180)) + (sol*geri*(ileri-180)*(sag-180));
  m1.write(m10);
  m2.write(m20);
  m3.write(m30);
  m4.write(m40);
  
}

void hasanAli(){
  while(true){
    //Serial.println("OKU");
    for(int i=0; i<15; i++){
      veriler[i] = Serial1.parseInt();
      Serial.print(veriler[i]);
      Serial.print(" / ");
    }
    while(Serial1.available() > 0)
      Serial1.read();
  Serial.println(" ");

    goksen = veriler[14];
    if ( goksen == 31*31 )
      break;
      
  //Serial.print(ileri);
  //Serial.print(" / ");
  //Serial.println(goksen);
    }
  ileri           =   veriler[0];
  geri            =   veriler[1];
  sag          =   veriler[2];
  sol          =   veriler[3];
  yukari          =   veriler[4];
  asagi           =   veriler[5];
  saatyonu        =   veriler[6];
  saatyonu_ters   =   veriler[7];
  kamera_yukari   =   veriler[8];
  kamera_asagi    =   veriler[9];
  isik            =   veriler[10];
  otonom_derinlik =   veriler[11];
  gyro            =   veriler[12];
  otonom_gorev    =   veriler[13];
  goksen          =   veriler[14];
  
  
  }
