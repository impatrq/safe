import 'package:flutter/animation.dart';
import 'package:get/get.dart';

class SpinningController extends GetxController with SingleGetTickerProviderMixin {

  AnimationController? animationController;

  void startSpin(){
    animationController!.repeat();
  }

  void stopSpin(){
    animationController!.stop();
  }

  @override
  void onInit() {
    super.onInit();

    animationController = AnimationController(vsync: this, duration: Duration(milliseconds: 1500));

    animationController!.addListener(() => update());

  }

  @override
  void dispose() {
    super.dispose();
    animationController!.dispose();
  }

}