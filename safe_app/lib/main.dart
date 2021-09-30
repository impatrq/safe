import 'package:flutter/material.dart';
import 'package:safe_app/utilities/constants.dart';
import 'package:safe_app/screens/loading_screen.dart';
import 'package:safe_app/screens/login_screen.dart';
import 'package:safe_app/screens/doors_screen.dart';
import 'package:safe_app/screens/workers_screen.dart';
import 'package:safe_app/screens/finder_screen.dart';
import 'package:safe_app/screens/about_us_screen.dart';
import 'package:get/get.dart';
import 'package:flutter/services.dart';
import 'package:safe_app/services/safe_app_controller.dart';

void main(){

  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setPreferredOrientations([DeviceOrientation.portraitUp, DeviceOrientation.portraitDown]);

  Get.put(SafeAppController());

  runApp(
    GetMaterialApp(
      initialRoute: '/',
      getPages: [
        GetPage(name: '/', page: () => LoadingScreen(), transition: Transition.fade),
        GetPage(name: '/login', page: () => LoginScreen(), transition: Transition.fade),
        // GetPage(name: '/dashboard', page: () => DashboardScreen(), transition: Transition.fade),
        GetPage(name: '/doors', page: () => DoorsScreen(), transition: Transition.fade),
        // GetPage(name: '/door', page: () => DoorDetailsScreen(), transition: Transition.fade),
        GetPage(name: '/workers', page: () => WorkersScreen(), transition: Transition.fade),
        GetPage(name: '/finder', page: () => FinderScreen(), transition: Transition.fade),
        GetPage(name: '/about-us', page: () => AboutUsScreen(), transition: Transition.fade),
      ],
      theme: ThemeData.light().copyWith(
        textSelectionTheme: TextSelectionThemeData(
          cursorColor: kLogoDarkBlueColor,
          selectionHandleColor: kLogoDarkBlueColor,
        ),
      ),
      debugShowCheckedModeBanner: false,
    )
  );
}