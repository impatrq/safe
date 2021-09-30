import 'package:flutter/material.dart';
import 'package:get/get.dart';

class ScrollableRowController extends GetxController {

  final ScrollController scrollController = ScrollController();
  double scrollRatio = 0;

  @override
  void onInit() {
    super.onInit();
    scrollController.addListener(() {
      scrollRatio = scrollController.offset / scrollController.position.maxScrollExtent;
      update();
    });
  }

}