#include<Wire.h>
#include<LiquidCrystal_I2C.h>

const byte joy1_pot1 = A0; // ileri-geri
const byte joy1_pot2 = A1; // saat yönü-saat yönü tersi
const byte joy1_pot3 = A2; // boş

const byte joy2_pot1 = A3; // yukarı-aşağı
const byte joy2_pot2 = A4; //dik sağ-dik sol
const byte joy2_pot3 = A5; //kamera yukarı- asağı

const byte pot_vites = A6; // Vites

const byte switch1 = 8;  // bıçak açma-kapama
const byte switch2 = 31;  // otonom derinlik
const byte switch3 = 32;  //ışık
const byte switch4 = 33;  // gyro
const byte switch5 = 34;  //otonom görev

String paket_veri, ileri1, geri1, bicak1;

int ii=0;
int vites = 180;
int goksen = 31*31;
int ileri, geri, saatyonu, saatyonu_ters, yukari, asagi, diksag, diksol, kamera_yukari, kamera_asagi, bicak, otonom_derinlik, isik, gyro, otonom_gorev;
char paket[250];

LiquidCrystal_I2C lcd (0x27, 16, 2);

const byte sonmillis = 0;
unsigned long yenizaman;
unsigned long eskizaman = 0;

void lcdekran()
{
  yenizaman = millis();
  lcd.setCursor (0, 0);
  lcd.print ("Sicaklik:");
  lcd.print ("y");
  lcd.setCursor (0, 1);
  lcd.print("Derinlik:");
  lcd.print ("x");

  if (yenizaman - eskizaman > 500)
  {
    lcd.clear();
    eskizaman = yenizaman;
  }
}


void setup()
{
  Serial.begin(9600);
  Serial1.begin(9600);

  lcd.begin();
  lcd.setCursor(0, 0);
  lcd.print("   YTU GEMDEK ROV ");
  lcd.setCursor(0, 1);
  lcd.print("    ROBOIK ");
  delay(3000);
  lcd.clear();

  Wire.begin();

  paket_veri = String();

  pinMode(switch1, INPUT);
  pinMode(switch2, INPUT);
  pinMode(switch3, INPUT);
  pinMode(switch4, INPUT);
  pinMode(switch5, INPUT);
}

void loop()
{

  //int vites = map(analogRead(pot_vites), 0, 1023, 0, 178);

  ileri = map(analogRead(joy1_pot1), 540, 1023, 0, vites);//
  geri = map(analogRead(joy1_pot1), 482, 0, 0, vites);//


  saatyonu = map(analogRead(joy1_pot2), 540, 1023, 0, vites);//
  saatyonu_ters = map(analogRead(joy1_pot2), 482, 0, 0, vites);//


  yukari = map(analogRead(joy2_pot1), 540, 1023, 0, vites);//
  asagi = map(analogRead(joy2_pot1), 482, 0, 0, vites);//


  diksag = map(analogRead(joy2_pot2), 540, 1023, 0, vites);//
  diksol = map(analogRead(joy2_pot2), 482, 0, 0, vites);//


  kamera_yukari = map(analogRead(joy2_pot3), 540, 1023, 0, vites);
  kamera_asagi = map(analogRead(joy2_pot3), 482, 0, 0, vites);

  bicak = digitalRead(switch1);
  otonom_derinlik = digitalRead(switch2);
  isik = digitalRead(switch3);
  gyro = digitalRead(switch4);
  otonom_gorev = digitalRead(switch5);

  int tumveri[15] = {ileri, geri, diksag, diksol, yukari, asagi, saatyonu, saatyonu_ters, kamera_yukari, kamera_asagi, otonom_derinlik, isik, gyro, otonom_gorev, goksen};

  paket_veri = "";
  /*
  for(int i = 0 ; i<15 ; i++){
    ii = tumveri[i];
    ii = (abs(ii) + ii)/2;
    
    }*/
  sprintf(paket, "%d//%d//%d//%d//%d//%d//%d//%d//%d//%d//%d//%d//%d//%d//%d//",ileri, geri, diksag, diksol, yukari, asagi, saatyonu, saatyonu_ters, kamera_yukari, kamera_asagi, isik, otonom_derinlik, gyro, otonom_gorev,goksen);
  Serial1.write(paket);
  Serial.println(paket);
  delay(100);
  //paket_veri = ileri1 + '/' + geri1 + '/' + bicak1; // ileri / geri / diksag / diksol / yukari / asagi / saatyonu / saatyonu_ters / kamera_yukari / kamera_asagi / isik / otonom_derinlik / gyro / otonom_gorev / goksen
  

}


