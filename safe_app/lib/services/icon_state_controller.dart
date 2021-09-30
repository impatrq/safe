import 'package:get/get.dart';

class IconController extends GetxController {

  bool showLoginPassword = false;

  void toggleShowLoginPassword(){
    showLoginPassword = !showLoginPassword;
    update();
  }

  bool isFlashOn = false;

  void toggleFlash(){
    isFlashOn = !isFlashOn;
    update();
  }

  bool? keepLoggedIn = false;

  void setKeepLoggedIn(bool? value){
    keepLoggedIn = value;
    update();
  }

}