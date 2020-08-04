#include <Thread.h>
#define NUM_LEDS 60
#include "FastLED.h"
#define PIN 13
CRGB leds[NUM_LEDS];
byte buff[NUM_LEDS*3 + 1];
byte cur_led = 0;
byte old_colors[NUM_LEDS*3];
byte colors[NUM_LEDS*3];
byte old_brightness = 50;
byte brightness = 1;
Thread ledsPrinter = Thread();

void setup() {
  Serial.begin(115200);
  
  FastLED.addLeds<WS2811, PIN, GRB>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip ); //.setCorrection( 0xFFAFAF ); //.setCorrection( TypicalLEDStrip )
  FastLED.setBrightness(1);
  pinMode(PIN, OUTPUT);

  ledsPrinter.onRun(ledsPrint);
  ledsPrinter.setInterval(20);
}

void loop() {
  if (ledsPrinter.shouldRun()) {
    ledsPrinter.run();
  }
  
  while (Serial.available() > 0){
    if (Serial.read() == 255) {
      byte len = 0;
      len = Serial.readBytes(buff, NUM_LEDS*3 + 1);
      if (len==NUM_LEDS*3 + 1) {
        brightness = buff[0];
        for (int i = 1; i < sizeof(buff); i++) {
          colors[i] = buff[i];
        }
      }
    }
    else {
      //Serial.flush();
    }
  }
  //getData();
}
void getData() {
  for (int i = 0; i < NUM_LEDS + 2; i++) {
    while (!Serial.available());
    
    byte chr = Serial.read();
    
    if (chr == 0 && i != 0) {
      break;
    }
    else if (i == 1) {
      brightness = chr;
    }
    else if (i == NUM_LEDS + 1) {
      colors[i-2] = chr;
      break;
    }
    else {
      colors[i-2] = chr;
    }
  }
}
void ledsPrint() {
  if (old_brightness < brightness) {
    old_brightness++;
    FastLED.setBrightness(old_brightness);
  }
  if (old_brightness > brightness) {
    old_brightness = old_brightness - 1;
    FastLED.setBrightness(old_brightness);
  }
  
  byte d;
  for (int i = 0; i < sizeof(old_colors); i++) {
    d = ceil((colors[i] - old_colors[i]) / 20);
    old_colors[i] += d;
  }

  for (int i = 0; i < NUM_LEDS; i++) {
    byte r = old_colors[i*3 + 1];
    byte g = old_colors[i*3 + 2];
    byte b = old_colors[i*3 + 0];
    leds[i] = CRGB(r, g, b);
    //leds[i] = CRGB(colors[i*3 + 0], colors[i*3 + 1], colors[i*3 + 2]);
  }
  FastLED.show();
}
