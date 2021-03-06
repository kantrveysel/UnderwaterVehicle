int mpoz(int a);


void setup() {

  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  Serial.begin(9600);
}

int sagsol,sag,sol, igeri, ileri, geri;
int tol = 10;
void loop() {
  sagsol = map(analogRead(A0), 0, 1023, 0, 190-tol);
  sag = map(sagsol<90+tol ? 0:sagsol, 90+tol, 190-tol, 0 , 190-tol);
  sol = map(sagsol>90-tol ? 0:190-tol-2*sagsol, 20, 190-tol, 0, 190-tol);
  igeri = map(analogRead(A1), 0, 1023, 0, 190-tol);
  ileri = map(igeri<90+tol ? 0:igeri, 90+tol, 190-tol, 0 , 190-tol);
  geri = map(igeri>90-tol ? 0:190-tol-2*igeri, 20, 190-tol, 0, 190-tol);

  sag = mpoz(sag);
  sol = mpoz(sol);
  ileri = mpoz(ileri);
  geri = mpoz(geri);
  
  Serial.print(sol);
  Serial.print(" / ");
  Serial.println(sag);
  Serial.print(ileri);
  Serial.print(" / ");
  Serial.println(geri);
  
  Serial.println(" - - - - - ");
  delay(500);

}
int mpoz(int a){ return a<0 ? 0:a; }
