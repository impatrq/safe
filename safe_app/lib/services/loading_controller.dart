import 'package:get/get.dart';

class LoadingController extends GetxController {

  bool isLoading = false;

  void toggleLoadingState(){
    isLoading = !isLoading;
    update();
  }

}