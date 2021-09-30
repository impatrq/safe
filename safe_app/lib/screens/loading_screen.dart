import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:safe_app/services/safe_app_controller.dart';
import 'package:safe_app/utilities/constants.dart';
import 'package:safe_app/services/auth_controller.dart';
import 'package:safe_app/screens/dashboard_screen.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';

class LoadingScreen extends StatelessWidget {

  final AuthController _authController = AuthController();
  final SafeAppController _safeAppController = Get.find();

  Future<void> load() async {
    bool isLoggedIn = await _authController.checkIfLoggedIn();
    if(isLoggedIn){
      await _safeAppController.initialize();
      var userData = await _authController.getLoggedInUserData();
      Get.offAll(() => DashboardScreen(userData: userData));
    } else {
      Future.delayed(Duration(seconds: 2), () => Get.offAllNamed('/login'));
    }
  }

  @override
  Widget build(BuildContext context) {
    load();
    return Scaffold(
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Hero(
            tag: 'logo',
            child: Image.asset('assets/images/safe_logo.png', width: 150.0, height: 150.0,),
          ),
          Text(
            'SAFE',
            style: kBrandTitleYellowTextStyle,
            textAlign: TextAlign.center,
          ),
          Text(
            'SECURE ACCESS FOR',
            style: kLittleBrandTitleDarkBlueTextStyle,
            textAlign: TextAlign.center,
          ),
          Text(
            'ENVIRONMENTS',
            style: kMediumBrandTitleDarkBlueTextStyle,
            textAlign: TextAlign.center,
          ),
          SizedBox(height: 100.0,),
          SpinKitFadingCircle(
            color: kLogoDarkBlueColor,
          ),
        ],
      ),
    );
  }
}
