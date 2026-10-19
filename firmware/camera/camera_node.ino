#include "esp_camera.h"
#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include "base64.h"

// ===================
// Select camera model
// ===================
#define CAMERA_MODEL_AI_THINKER  // Has PSRAM
#include "camera_pins.h"
#define LED_BUILTIN 4

// ===========================
// Enter your WiFi credentials
// ===========================
const char *ssid = "YOUR_WIFI_SSID";
const char *password = "YOUR_WIFI_PASSWORD";

AsyncWebServer server(80);
String imageData = "";

void takePicture() {
  camera_fb_t * fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Camera capture failed");
    return;
  }

  delay(50);
  // Convert to base64
  imageData = "data:image/jpeg;base64," + base64::encode(fb->buf, fb->len);

  esp_camera_fb_return(fb);
  Serial.println("Picture taken and encoded");
}

void setup() {
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println();
  pinMode (LED_BUILTIN, OUTPUT);

  uint8_t baseMac[6];

  // Get MAC address of the WiFi station interface
  esp_read_mac(baseMac, ESP_MAC_WIFI_STA);
  Serial.print("Station MAC: ");
  for (int i = 0; i < 5; i++) {
    Serial.printf("%02X:", baseMac[i]);
  }
  Serial.printf("%02X\n", baseMac[5]);

  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  config.frame_size = FRAMESIZE_SVGA;
  config.jpeg_quality = 12;
  config.fb_count = 2; // Use 2 frame buffers


  // Init Camera
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }
  Serial.println("Camera initialized");

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    digitalWrite(LED_BUILTIN, HIGH);
    delay(50);
    digitalWrite(LED_BUILTIN, LOW);
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
  digitalWrite(LED_BUILTIN, HIGH);
  delay(500);
  digitalWrite(LED_BUILTIN, LOW);

  // Start web server
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/html", "<h1>ESP32-CAM Capture</h1><img src='" + imageData + "' />");
  });

  server.on("/capture", HTTP_GET, [](AsyncWebServerRequest *request){
    takePicture();
    request->send(200, "text/plain", "Image captured and encoded");
  });

  server.on("/download", HTTP_GET, [](AsyncWebServerRequest *request){
    if (imageData.length() == 0) {
      Serial.println("No image");
      request->send(500, "text/plain", "No image");
    } else {
      Serial.println("Image captured");
      request->send(200, "text/plain", imageData);
    }
  });

  server.on("/delete", HTTP_GET, [](AsyncWebServerRequest *request){
    imageData = "";  // Clear the image data
    request->send(200, "text/plain", "Image data deleted");
  });

  server.on("/live", HTTP_GET, [](AsyncWebServerRequest *request){
    takePicture();
    request->send(200, "text/html", "<h1>Live Feed</h1><img src='" + imageData + "' />");
    imageData = "";  // Clear the image data
  });

  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  // Nothing to do here
}
